# Parseur d'articles scientifiques

Projet du sprint 2 de Genie logiciel/Scrum 2026.

Le programme prend un dossier contenant des fichiers PDF, extrait leur texte, detecte des informations principales, puis cree un sous-dossier de sortie contenant un fichier `.txt` par PDF.

Chaque fichier de sortie contient exactement 4 lignes :

1. Le nom du fichier PDF d'origine
2. Le titre detecte
3. Le ou les auteurs detectes
4. Le resume detecte

Si une information n'est pas trouvee, la ligne reste vide.

## Choix technique

Le projet est implemente en Python 3 :

- langage rapide a developper pour l'equipe
- execution simple en ligne de commande sous GNU/Linux
- bibliotheque `pypdf` suffisante pour extraire du texte depuis des PDF textuels

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
python3 parse_articles.py /chemin/vers/dossier_pdf
```

Par defaut, le programme cree un sous-dossier `parsed_output` dans le dossier d'entree. Si ce sous-dossier existe deja, il est supprime puis recree.

Pour changer le nom du sous-dossier :

```bash
python3 parse_articles.py /chemin/vers/dossier_pdf --output-subdir resultats
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

## Limites

- Le projet fonctionne correctement sur les PDF contenant du vrai texte.
- Les PDF scannes sans couche texte necessitent un OCR, qui n'est pas inclus ici.
- L'extraction du titre, des auteurs et du resume repose sur des heuristiques. Le resultat peut varier selon la mise en page des articles.
