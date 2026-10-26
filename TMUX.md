# tmux 3.8 autonome — Mac Apple Silicon

[Télécharger tmux-3.8-macos-arm64.tar.gz](https://raw.githubusercontent.com/simonherlin/portable-ruby/main/tmux-3.8-macos-arm64.tar.gz)

Pour les Mac Apple Silicon, dont M4 Pro, sous macOS 15 ou ultérieur (y compris Tahoe 26). Le paquet contient tmux et ses bibliothèques : aucune installation Homebrew, Ruby, compilation ou commande sudo n'est nécessaire.

Dans Terminal, ces commandes téléchargent, vérifient, extraient puis lancent tmux :

```sh
mkdir -p "$HOME/Applications/tmux-portable"
cd "$HOME/Applications/tmux-portable"
curl -fLO https://raw.githubusercontent.com/simonherlin/portable-ruby/main/tmux-3.8-macos-arm64.tar.gz
curl -fLO https://raw.githubusercontent.com/simonherlin/portable-ruby/main/tmux-3.8-macos-arm64.tar.gz.sha256
shasum -a 256 -c tmux-3.8-macos-arm64.tar.gz.sha256 &&
tar -xzf tmux-3.8-macos-arm64.tar.gz &&
./tmux-3.8-macos-arm64/bin/tmux
```

Pour le relancer :

```sh
"$HOME/Applications/tmux-portable/tmux-3.8-macos-arm64/bin/tmux"
```

Conserver le dossier extrait entier. Ne pas déplacer seulement `bin/tmux` : c'est le lanceur qui trouve les bibliothèques et les données terminal incluses. Pour quitter une session : `exit`. Pour la détacher : `Ctrl+B`, puis `D`.

## Contenu et validation

Les bouteilles officielles Homebrew sont vérifiées avant assemblage. Les bibliothèques de libevent, ncurses, utf8proc, jemalloc et OpenSSL sont incluses, ainsi que la base terminfo de ncurses. Les chemins des bibliothèques sont relocalisés et les binaires signés ad hoc. Le paquet conserve les bibliothèques système fournies par macOS comme seules dépendances externes de chargement.

Les sources et empreintes sont dans [packaging/tmux-bottles.json](packaging/tmux-bottles.json), et les notices de licence dans l'archive. Ce paquet assemblé n'est ni une distribution officielle Homebrew/tmux ni un paquet notarisé par Apple.

Test macOS 15 ARM64 : [réussi](https://github.com/simonherlin/portable-ruby/actions/runs/40321206235), avec déplacement du dossier, démarrage du serveur, exécution d'une commande dans une session et capture de son résultat.

Test Tahoe ARM64 : [consulter le workflow](https://github.com/simonherlin/portable-ruby/actions/workflows/test-tmux-tahoe.yml).
