"""Build a relocatable macOS ARM64 bundle from checksum-pinned Homebrew bottles."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import urllib.request

def run(*args):
    return subprocess.check_output(args, text=True).strip()

assert run('uname', '-m') == 'arm64'
root = Path.cwd()
manifest = json.loads((root / 'packaging/tmux-bottles.json').read_text())
version = manifest['tmux']['version']
work = root / 'build-tmux'
work.mkdir()
bundle = work / f'tmux-{version}-macos-arm64'
for directory in ['bin', 'libexec', 'lib', 'share', 'licenses']:
    (bundle / directory).mkdir(parents=True, exist_ok=True)

for name, info in manifest.items():
    scope = info['url'].split('/blobs/')[0].split('/v2/')[1]
    token_url = f'https://ghcr.io/token?service=ghcr.io&scope=repository:{scope}:pull'
    token = json.load(urllib.request.urlopen(token_url))['token']
    request = urllib.request.Request(info['url'], headers={'Authorization': 'Bearer ' + token})
    data = urllib.request.urlopen(request, timeout=120).read()
    assert hashlib.sha256(data).hexdigest() == info['sha256'], name
    archive = work / (name + '.tar.gz')
    archive.write_bytes(data)
    dest = work / ('source-' + name)
    with tarfile.open(archive) as tar:
        tar.extractall(dest, filter='tar')
    prefix = next((dest / name).iterdir())
    for library in (prefix / 'lib').glob('*.dylib'):
        target = bundle / 'lib' / library.name
        assert not target.exists(), library.name
        shutil.copy2(library, target)
    notices = bundle / 'licenses' / name
    notices.mkdir()
    for path in prefix.rglob('*'):
        if path.is_file() and any(word in path.name.upper() for word in ['LICENSE', 'COPYING', 'COPYRIGHT', 'AUTHORS']):
            target = notices / path.relative_to(prefix)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    if name == 'tmux':
        shutil.copy2(prefix / 'bin/tmux', bundle / 'libexec/tmux')
        shutil.copytree(prefix / 'share', bundle / 'share', dirs_exist_ok=True)
    if name == 'ncurses':
        shutil.copytree(prefix / 'share/terminfo', bundle / 'share/terminfo', symlinks=True)

binaries = [bundle / 'libexec/tmux', *sorted((bundle / 'lib').glob('*.dylib'))]
for binary in binaries:
    assert 'arm64' in run('lipo', '-archs', str(binary))
    if binary.suffix == '.dylib':
        subprocess.check_call(['install_name_tool', '-id', '@loader_path/' + binary.name, str(binary)])
    for line in run('otool', '-L', str(binary)).splitlines()[1:]:
        dependency = line.strip().split(' (')[0]
        if dependency.startswith(('/usr/lib/', '/System/Library/')):
            continue
        basename = Path(dependency).name
        assert (bundle / 'lib' / basename).exists(), (binary, dependency)
        relative = '@loader_path/' + ('../lib/' if binary.parent.name == 'libexec' else '') + basename
        subprocess.check_call(['install_name_tool', '-change', dependency, relative, str(binary)])
    subprocess.check_call(['codesign', '--force', '--sign', '-', str(binary)])
    subprocess.check_call(['codesign', '--verify', '--strict', str(binary)])
    for line in run('otool', '-L', str(binary)).splitlines()[1:]:
        dependency = line.strip().split(' (')[0]
        assert dependency.startswith(('/usr/lib/', '/System/Library/', '@loader_path/')), dependency

(bundle / 'bin/tmux').write_text('''#!/bin/sh
bundle_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd) || exit 1
export TERMINFO_DIRS="$bundle_dir/share/terminfo${TERMINFO_DIRS:+:$TERMINFO_DIRS}:/usr/share/terminfo"
exec "$bundle_dir/libexec/tmux" "$@"
''')
(bundle / 'bin/tmux').chmod(0o755)
shutil.copy2(root / 'packaging/tmux-bottles.json', bundle / 'provenance.json')
(bundle / 'README.txt').write_text(f'''tmux {version} portable pour macOS 15+ Apple Silicon (ARM64).
Lancer bin/tmux depuis le dossier extrait. Aucun brew install nécessaire.
Conserver le dossier entier : bin, libexec, lib et share sont nécessaires.
Bibliothèques issues des bouteilles Homebrew, chemins relocalisés et signature ad hoc.
Ce paquet n'est pas notarisé par Apple. Licences dans licenses/.
''')

# Test after relocation into a path containing spaces, with no Homebrew PATH.
relocated = work / 'relocated bundle'
shutil.copytree(bundle, relocated, symlinks=True)
env = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'HOME': os.environ['HOME'], 'TERM': 'xterm-256color'}
tmux = str(relocated / 'bin/tmux')
assert subprocess.check_output([tmux, '-V'], env=env, text=True).strip() == 'tmux ' + version
socket = '/tmp/tmux-portable-' + str(os.getpid())
command = [tmux, '-S', socket, '-f', '/dev/null']
try:
    subprocess.check_call(command + ['new-session', '-d', '-s', 'portable-test', '/bin/sh'], env=env)
    subprocess.check_call(command + ['send-keys', '-t', 'portable-test', 'printf "PORTABLE_TMUX_OK\\n"', 'Enter'], env=env)
    import time
    for attempt in range(20):
        capture = subprocess.check_output(command + ['capture-pane', '-p', '-t', 'portable-test'], env=env, text=True)
        if 'PORTABLE_TMUX_OK' in capture.splitlines():
            break
        time.sleep(0.25)
    else:
        raise RuntimeError(capture)
finally:
    subprocess.run(command + ['kill-server'], env=env, check=False)

output = root / (bundle.name + '.tar.gz')
with tarfile.open(output, 'w:gz') as tar:
    tar.add(bundle, arcname=bundle.name)
Path(str(output) + '.sha256').write_text(hashlib.sha256(output.read_bytes()).hexdigest() + '  ' + output.name + '\n')
print('PASS: relocated tmux version, native dependencies, server, shell and pane capture')
