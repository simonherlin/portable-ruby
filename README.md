# Portable Ruby 4.0.7_1 pour Homebrew sur macOS

Miroir non officiel des archives binaires officielles Homebrew, téléchargées sans modification depuis GHCR et vérifiées avec les SHA-256 publiés dans [Homebrew/brew #24211](https://github.com/Homebrew/brew/pull/24211).

Les fichiers sont disponibles dans la [release 4.0.7_1](https://github.com/simonherlin/portable-ruby/releases/tag/4.0.7_1).

| Mac | Archive |
| --- | --- |
| Apple Silicon (ARM64) | [portable-ruby-4.0.7_1.arm64_big_sur.bottle.tar.gz](https://github.com/simonherlin/portable-ruby/releases/download/4.0.7_1/portable-ruby-4.0.7_1.arm64_big_sur.bottle.tar.gz) |
| Intel (x86_64) | [portable-ruby-4.0.7_1.big_sur.bottle.tar.gz](https://github.com/simonherlin/portable-ruby/releases/download/4.0.7_1/portable-ruby-4.0.7_1.big_sur.bottle.tar.gz) |

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

Ce miroir contient uniquement Portable Ruby 4.0.7_1 ; ne pas configurer ce domaine globalement pour les autres bouteilles Homebrew.

## Vérifier une archive téléchargée manuellement

Télécharger `SHA256SUMS` depuis la release et lancer, dans le dossier contenant l'archive :

```sh
shasum -a 256 portable-ruby-4.0.7_1.*.bottle.tar.gz
```

Comparer le résultat avec `SHA256SUMS` et `provenance.json`. L'archive contient notamment `portable-ruby/4.0.7_1/bin/ruby`.

Les archives conservent les fichiers et notices de licence de leur distribution d'origine. Ce dépôt n'est pas affilié à Homebrew ni au projet Ruby. Les empreintes et la structure des archives ont été vérifiées sous Linux ; leur exécution sur macOS n'a pas été testée ici.
