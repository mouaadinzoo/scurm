# Parseur d'articles scientifiques

Projet du sprint 2 de Genie logiciel/Scrum 2026.

Le parseur prend un dossier contenant des fichiers `.txt` deja convertis depuis des PDFs par un convertisseur separe. Il detecte les informations principales, puis cree un sous-dossier de sortie contenant un fichier `.txt` par article.

Chaque fichier de sortie contient exactement 4 lignes :

1. Le nom du fichier PDF d'origine reconstitue a partir du nom du fichier texte
2. Le titre detecte
3. Le ou les auteurs detectes
4. Le resume detecte

Si une information n'est pas trouvee, la ligne reste vide.

## Choix technique

Le projet est implemente en Python 3 :

- langage rapide a developper pour l'equipe
- execution simple en ligne de commande sous GNU/Linux
- aucune dependance externe necessaire pour parser les fichiers texte convertis

## Choix du langage

L'equipe a compare Python 3 avec le langage C en utilisant la commande `time` sur deux types de mesures :

- des boucles imbriquees allant de `0` a `10000`
- l'ecriture puis la lecture de gros fichiers contenant des donnees aleatoires

Python 3 a ete retenu pour la version finale, car il est maitrise par l'equipe et ses performances ont ete jugees satisfaisantes pour le parseur demande dans ce sprint.

## Structure

- `parse_articles.py` : script principal
- `benchmark.py` : petit benchmark CPU/I/O pour justifier le choix du langage
- `requirements.txt` : dependance Python
- `tests/test_parser.py` : tests unitaires de base

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

```bash
python3 parse_articles.py /chemin/vers/dossier_txt
```

Par defaut, le programme cree un sous-dossier `parsed_output` dans le dossier d'entree. Si ce sous-dossier existe deja, il est supprime puis recree.

Pour changer le nom du sous-dossier :

```bash
python3 parse_articles.py /chemin/vers/dossier_txt --output-subdir resultats
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Benchmark

```bash
python3 benchmark.py
```

Le benchmark mesure :

- une boucle imbriquee
- une ecriture/lecture de fichier binaire

Exemple d'utilisation avec `time` :

```bash
time python3 benchmark.py
```

## Limites

- Le parseur suppose que la conversion PDF -> texte a deja ete faite en amont.
- Les PDF scannes sans couche texte necessitent un OCR dans le convertisseur amont, ce qui n'est pas inclus ici.
- L'extraction du titre, des auteurs et du resume repose sur des heuristiques. Le resultat peut varier selon la mise en page des articles.
