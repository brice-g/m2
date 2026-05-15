# Module 2 - brief 2 FastIA Data Pipeline 

Ce dépôt contient la pipeline d'audit, de nettoyage et d'anonymisation du dataset client de **FastIA**. L'objectif est de transformer un dataset "artisanal" en un actif de données industriel, auditable et conforme au RGPD pour le fine-tuning de modèle.

## Sommaire
1. [Architecture du Projet](#architecture-du-projet)
2. [Installation et Utilisation](#installation-et-utilisation)
3. [Pipeline de Traitement](#pipeline-de-traitement)
4. [Résultats de l'Audit (V1 vs V2)](#résultats-de-laudit-v1-vs-v2)
5. [Conformité et Éthique](#conformité-et-éthique)
6. [Stockage des Données](#stockage-des-données)
7. [Comparatif Audit (v1 vs v2)](#comparatif-audit--v1-vs-v2)

---

## Architecture du Projet

```text
fastia-data-pipeline/
├── data/
│   ├── raw/          # Données brutes (dataset_fastia_module1.jsonl)
│   ├── interim/      # Étapes de nettoyage intermédiaires
│   └── processed/    # Dataset final nettoyé et anonymisé
├── docs/             # Documentation (Datasheet, Cycle de vie, Audit)
├── src/
│   └── pipeline/     # Code source de la pipeline (Load, Clean, Bias, Anonymize, Validate, Run)
    └── storage/      # Gestion SQL (Load, Dump, Schema SQL, Split, Utils) 
├── tests/            # Tests unitaires Pytest
├── docker-compose.yml # Infrastructure reproductible
└── README.md
└── Makefile          # Automatisation des commandes
```

## Installation et Utilisation

Le projet propose désormais deux méthodes d'installation : une via **Makefile** (recommandée pour la rapidité) et une méthode manuelle.

### 1. Prérequis
* **Docker & Docker Compose** (pour la base de données PostgreSQL)
* **Make** (généralement installé par défaut sur Linux/macOS)
* **Python 3.11**
* **Gestionnaire de paquets pip**
* **Environnement virtuel** (fortement recommandé pour isoler les dépendances)

### 2. Installation 

Commencez par cloner le dépôt, puis installez les dépendances nécessaires :

```bash
# Clonage du projet
git clone [https://github.com/brice-g/m2.git](https://github.com/brice-g/m2.git)

# Création et activation de l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate

# Installation des bibliothèques requises
pip install pandas numpy matplotlib seaborn jupyter loguru pytest
```

**Lancement de la pipeline**

Pour transformer le dataset brut en un jeu de données nettoyé et prêt pour l'entraînement, exécutez la commande suivante depuis la racine du projet :

```bash
python -m src.pipeline.run --input data/raw/dataset_fastia_module1.jsonl --output data/processed/dataset_fastia_clean_v1.jsonl
```
Ce script automatise l'ensemble du flux de traitement, génère le fichier JSONL final et produit un fichier de métadonnées (.meta.json) contenant les statistiques de l'exécution.

Le projet utilise maintenant un Makefile pour simplifier l'exécution de la chaîne complète (du brut aux fichiers d'entraînement).
Exécution du flux "Brut → Train/Test"

Le `Makefile` automatise la gestion de l'environnement et de l'infrastructure

```bash
# 1. Installer les dépendances
make install

# 2. Lancer l'infrastructure PostgreSQL (Docker)
make db-up

# 3. Lancer la pipeline complète
make full
```


**Lancement des tests**

le projet utilise Pytest
pour lancer les tests
```bash
python -m pytest
```

## Pipeline de Traitement

Le code est modularisé dans le répertoire `src/pipeline/` pour assurer la reproductibilité des traitements et faciliter la maintenance évolutive :

* **Chargement (`load.py`)** : Responsable de la lecture du fichier JSONL initial et de l'aplatissement des dictionnaires imbriqués (extraction des champs `categorie`, `priorite`, et `reponse_suggeree` depuis l'objet `output`).
* **Nettoyage (`clean.py`)** :
    * **Suppression des doublons** : Élimination des doublons exacts et des quasi-doublons via l'utilisation de hash normalisés.
    * **Normalisation textuelle** : Nettoyage des espaces multiples, uniformisation de la casse et des guillemets tout en préservant le texte brut pour référence.
    * **Gestion des anomalies** : Traitement explicite des valeurs manquantes et filtrage des *outliers* de longueur basés sur le z-score ou l'écart interquartile (IQR).
* **Anonymisation (`anonymize.py`)** : Sécurisation des données par la détection et le masquage des informations personnelles (emails, numéros de téléphone, URLs et noms propres) via des expressions régulières et la reconnaissance d'entités nommées (NER).
* **Validation (`validate.py`)** : Contrôle final de conformité garantissant que le schéma est respecté, que les champs obligatoires sont remplis et que les catégories appartiennent à la liste officielle de FastIA.

## Résultats de l'Audit (V1 vs V2)

L'implémentation de la pipeline permet de transformer un jeu de données artisanal en un actif de données structuré et qualitatif. Voici la comparaison entre le dataset brut et le dataset traité :

| Métrique | Dataset Brut (V1) | Dataset Nettoyé (V2) |
| :--- | :--- | :--- |
| **Volume total** | `100%` des données d'origine | `~92%` (après dédoublonnage et filtrage) |
| **Doublons (Exacts & Quasi)** | Présents (non quantifiés) | **0** (supprimés via `drop_duplicates`) |
| **Valeurs manquantes** | Détectées sur `input` et `output` | **0** (imputées ou supprimées via `handle_missing`) |
| **Données Sensibles (PII)** | Exposées (emails, noms, tél) | **Anonymisées** (remplacées par `[NOM]`, `[EMAIL]`) |
| **Conformité Schéma** | Inexistante (format JSON imbriqué) | **Validée** (flat JSONL conforme au schéma cible) |
| **Outliers de longueur** | Présents (bruit technique) | **Identifiés et écartés** (via Z-score/IQR) |
| **Normalisation** | Casse et espaces hétérogènes | **Uniformisée** (standardisation UTF-8) |

> [!NOTE]  
> Les détails spécifiques sur les distributions de catégories et les biais linguistiques identifiés sont disponibles dans le rapport complet : [`docs/audit_v1.md`](docs/audit_v1.md).


## Conformité et Éthique

La gestion et le traitement des données au sein de ce projet sont régis par des principes stricts de responsabilité et de transparence :

* **Respect du RGPD** :
    * **Minimisation des données** : Seules les données strictement nécessaires à l'entraînement du modèle (input/output) sont conservées.
    * **Privacy by Design** : Intégration native d'une étape d'anonymisation dans la pipeline pour protéger l'identité des clients.
    * **Droit à l'oubli** : La structure modulaire permet de supprimer ou de retraiter facilement des entrées spécifiques si nécessaire.
* **Alignement avec l'AI Act** :
    * **Traçabilité** : Documentation complète du cycle de vie de la donnée, de la source brute jusqu'au dataset final.
    * **Transparence** : Utilisation d'une *Datasheet* pour déclarer les limites, les usages recommandés et les biais potentiels du jeu de données.
* **Analyse et Atténuation des Biais** :
    * **Biais de représentation** : Surveillance des déséquilibres entre les catégories pour éviter une dégradation de la performance sur les classes minoritaires.
    * **Biais linguistiques** : Vérification que le modèle ne sur-apprend pas des corrélations basées uniquement sur la longueur des messages ou le registre de langue.
* **Sécurité des données** : Les informations sensibles (PII) identifiées par NER ou Regex sont systématiquement remplacées par des balises génériques (`[NOM]`, `[COORDONNÉES]`) pour préserver le contexte sans exposer les individus.

*Pour plus de détails sur les choix techniques et éthiques, consultez :* [`docs/risques_ethiques.md`](docs/risques_ethiques.md)

## Stockage des Données

**Schéma de la table demandes**

Le choix s'est porté sur PostgreSQL pour garantir la cohérence des données via un typage strict et permettre un versioning efficace des datasets.
Contrairement à un simple stockage fichier, PostgreSQL permet ici d'assurer l'unicité des entrées (via des contraintes ON CONFLICT) et facilite l'extraction de splits stratifiés grâce à des requêtes SQL ciblées par version

| Colonne | Type | Description |
| :--- | :--- | :--- |
| id | SERIAL | Clé primaire unique | 
| input_text | TEXT | Texte nettoyé et anonymisé| 
| categorie | VARCHAR | "Classe (Demande commercial, Information générale, etc.)"| 
| priorite | VARCHAR | haute ou normale |
| dataset_version | VARCHAR | "Identifiant de version (ex: v1.0, v2.0)" |
| source | VARCHAR | original ou synthetic


## Comparatif Audit : v1 vs v2

Ce tableau compare le dataset après nettoyage initial (v1) et après l'étape d'augmentation synthétique et de split (v2).

| Indicateur | v1 (après Nettoyage) | v2 (après Augmentation) |
| :--- | :--- | :--- |
| Nombre d'exemples | 96 | 112 (89 Train / 23 Test) |
| Répartition Catégories | Hétérogène | Stratifiée (équilibrée) |
| Source des données | 100% Originales | ~86% Originales / 14% Synthétiques |
| Format final | JSONL brut | Format Instruct ([INST]...) |

### Analyse des évolutions
**Gain en volume :** L'ajout de 16 exemples synthétiques ciblés (urgences et messages longs) permet de renforcer les classes minoritaires identifiées lors de l'audit v1.

**Robustesse :** Le formatage en "Instruct" dans la v2 prépare directement le modèle aux interactions de type chatbot.

**Fiabilité :** Le processus inclut désormais une revue de qualité manuelle (revue_echantillon.csv) garantissant que l'augmentation LLM ne dégrade pas la pertinence métier.


## Gestion de l'Infrastructure Docker

Le projet utilise Docker Compose pour garantir un environnement de stockage persistant et reproductible pour l'audit.

**Infrastructure Docker** (docker-compose.yml)

Le fichier définit un service de base de données PostgreSQL 15 avec :

* **Persistance :** Utilisation d'un volume postgres_data pour ne pas perdre les données entre les redémarrages.

* **Initialisation :** Montage du volume ./schema.sql vers le point d'entrée Docker pour automatiser la création des tables.

* **Variables d'environnement :** Configuration flexible du nom de la DB et des identifiants (via .env ou valeurs par défaut).

* **Démarrer la DB :** make db-up (Lances un conteneur PostgreSQL fastia_db sur le port 5432).

* **Initialisation :** Au premier lancement, le fichier schema.sql est automatiquement exécuté pour créer la structure des tables.

* **Arrêter la DB :** make db-down.

* **Nettoyage complet :** make clean (Supprime les caches Python et les fichiers de données intermédiaires).

## Auteur
Brice Gandon