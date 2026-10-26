# Paquets macOS — Portable Ruby et tmux

## tmux autonome pour Apple Silicon

[tmux 3.8 avec ses bibliothèques incluses](TMUX.md) — téléchargement direct et commandes pour Mac M4 Pro / Tahoe, sans installation Homebrew.

## Version 4.0.9

Archives officielles Homebrew, copiées sans modification et vérifiées avec les SHA-256 de [l’API Homebrew](https://formulae.brew.sh/api/formula/portable-ruby.json). Les fichiers sont directement à la racine du dépôt.

| Mac | Téléchargement direct |
| --- | --- |
| Apple Silicon (ARM64) | [portable-ruby-4.0.9.arm64_big_sur.bottle.tar.gz](https://raw.githubusercontent.com/simonherlin/portable-ruby/main/portable-ruby-4.0.9.arm64_big_sur.bottle.tar.gz) |
| Intel (x86_64) | [portable-ruby-4.0.9.big_sur.bottle.tar.gz](https://raw.githubusercontent.com/simonherlin/portable-ruby/main/portable-ruby-4.0.9.big_sur.bottle.tar.gz) |

Empreintes : `SHA256SUMS`. Origine : `provenance-4.0.9.json`. Également disponibles dans la [release 4.0.9](https://github.com/simonherlin/portable-ruby/releases/tag/4.0.9).

Si Homebrew demande précisément `4.0.9` :

```sh
HOMEBREW_BOTTLE_DOMAIN="https://raw.githubusercontent.com/simonherlin/portable-ruby/main" brew --version
```

Le workflow macOS vérifie le démarrage de Ruby 4.0.9 et ses extensions natives sur macOS 15 ARM64 et Intel. Les deux tests ont [réussi sur macOS 15 ARM64 et Intel](https://github.com/simonherlin/portable-ruby/actions/runs/40298095883). Ce test ne constitue pas une certification Apple.

## Version 4.0.7_1 conservée

Miroir non officiel des archives binaires officielles Homebrew, téléchargées sans modification depuis GHCR et vérifiées avec les SHA-256 publiés dans [Homebrew/brew #24211](https://github.com/Homebrew/brew/pull/24211).

Les deux fichiers `.tar.gz` sont présents directement à la racine de ce dépôt Git, ainsi que dans la [release 4.0.7_1](https://github.com/simonherlin/portable-ruby/releases/tag/4.0.7_1).

| Mac | Archive |
| --- | --- |
| Apple Silicon (ARM64) | [portable-ruby-4.0.7_1.arm64_big_sur.bottle.tar.gz](https://raw.githubusercontent.com/simonherlin/portable-ruby/main/portable-ruby-4.0.7_1.arm64_big_sur.bottle.tar.gz) |
| Intel (x86_64) | [portable-ruby-4.0.7_1.big_sur.bottle.tar.gz](https://raw.githubusercontent.com/simonherlin/portable-ruby/main/portable-ruby-4.0.7_1.big_sur.bottle.tar.gz) |

Ces bouteilles ciblent macOS Big Sur ou ultérieur. Avec Homebrew exécuté sous Rosetta, utiliser l'archive Intel.

## Débloquer le téléchargement Homebrew

Si Homebrew demande précisément `4.0.7_1`, ce domaine de téléchargement permet à Homebrew de choisir l'architecture et de vérifier lui-même l'empreinte officielle :

```sh
HOMEBREW_BOTTLE_DOMAIN="https://github.com/simonherlin/portable-ruby/releases/download/4.0.7_1" brew --version
```

Si un `HOMEBREW_ARTIFACT_DOMAIN` personnalisé bloque déjà les téléchargements, le retirer pour cette commande :

```sh
env -u HOMEBREW_ARTIFACT_DOMAIN -u HOMEBREW_ARTIFACT_DOMAIN_NO_FALLBACK HOMEBREW_BOTTLE_DOMAIN="https://github.com/simonherlin/portable-ruby/releases/download/4.0.7_1" brew --version
```

Cette release contient uniquement Portable Ruby 4.0.7_1 ; ne pas configurer ce domaine globalement pour les autres bouteilles Homebrew.

## Vérifier une archive téléchargée manuellement

Télécharger `SHA256SUMS` depuis le dépôt ou la release et lancer, dans le dossier contenant l'archive :

```sh
shasum -a 256 portable-ruby-4.0.7_1.*.bottle.tar.gz
```

Comparer le résultat avec `SHA256SUMS` et `provenance.json`. L'archive contient notamment `portable-ruby/4.0.7_1/bin/ruby`.

Les archives conservent les fichiers et notices de licence de leur distribution d'origine. Ce dépôt n'est pas affilié à Homebrew ni au projet Ruby. Les empreintes et la structure des archives ont été vérifiées sous Linux ; leur exécution a également réussi sur les runners GitHub macOS 15 ARM64 et Intel.

## Validation macOS

Le workflow de validation de la version 4.0.7_1 [Validate macOS](https://github.com/simonherlin/portable-ruby/actions/workflows/validate-macos.yml) vérifie les empreintes, extrait les archives et exécute Ruby 4.0.7 ainsi que ses extensions OpenSSL, YAML, zlib et Fiddle sur macOS 15 ARM64 et Intel. Les deux tests ont [réussi le 26 octobre 2026](https://github.com/simonherlin/portable-ruby/actions/runs/40295746887). Cela ne constitue pas une certification ou notarisation Apple.
