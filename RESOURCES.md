# Ressources — Module 2

## Papiers fondateurs (dans `papers/`)

### Gebru et al. — *Datasheets for Datasets* (2018, v8 2021)
`papers/Gebru_2021_Datasheets_for_Datasets.pdf`
Proposition d'un format standardisé pour documenter un dataset : motivation, composition, collecte, prétraitements, usages, maintenance. **Base du livrable `docs/datasheet.md` du Brief 1.**

### Wei & Zou — *EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks* (2019)
`papers/Wei_Zou_2019_EDA_Easy_Data_Augmentation.pdf`
Quatre techniques simples d'augmentation textuelle : synonym replacement, random insertion, random swap, random deletion. **Point d'entrée pour le Brief 3 (techniques de substitution contrôlée).**

### Hu et al. — *LoRA: Low-Rank Adaptation of Large Language Models* (2021)
`papers/Hu_2021_LoRA.pdf`
Référence pour rappel — utilisé en Module 1. Utile pour contextualiser "pourquoi la qualité du dataset compte autant", puisque LoRA fige les poids de base et ne peut compenser que partiellement un dataset biaisé.

---

## Cadre réglementaire — à consulter en ligne

- **RGPD — texte consolidé** : <https://www.cnil.fr/fr/reglement-europeen-protection-donnees>
- **CNIL — IA et données personnelles** : <https://www.cnil.fr/fr/intelligence-artificielle>
- **AI Act — vue d'ensemble (Commission européenne)** : <https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai>
- **AI Act — texte officiel (EUR-Lex, règlement 2024/1689)** : <https://eur-lex.europa.eu/eli/reg/2024/1689/oj>

Livrable `docs/risques_ethiques.md` du Brief 2 : croiser les risques identifiés dans le dataset FastIA avec ces deux textes.

---

## Documentation technique

### Pandas & analyse
- Pandas user guide : <https://pandas.pydata.org/docs/user_guide/>
- missingno (visualisation des valeurs manquantes) : <https://github.com/ResidentMario/missingno>
- ydata-profiling (rapports HTML) : <https://docs.profiling.ydata.ai/>

### NLP
- spaCy — modèles français : <https://spacy.io/models/fr>
- NLTK WordNet — substitution de synonymes : <https://www.nltk.org/howto/wordnet.html>

### Stockage
- SQLAlchemy Core : <https://docs.sqlalchemy.org/en/20/core/>
- psycopg 3 (PostgreSQL) : <https://www.psycopg.org/psycopg3/docs/>
- Alembic (migrations) : <https://alembic.sqlalchemy.org/>

### Outillage
- Loguru : <https://loguru.readthedocs.io>
- Pytest : <https://docs.pytest.org>

---

## Dataset (dans `data/raw/`)

`data/raw/dataset_fastia_module1.jsonl` — copie du dataset du Module 1. Entrée de l'ensemble de la pipeline M2.
