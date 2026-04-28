# Module 2 - brief 2 FastIA Data Pipeline 

Ce dépôt contient la pipeline d'audit, de nettoyage et d'anonymisation du dataset client de **FastIA**. L'objectif est de transformer un dataset "artisanal" en un actif de données industriel, auditable et conforme au RGPD pour le fine-tuning de modèle.

## Sommaire
1. [Architecture du Projet](#architecture-du-projet)
2. [Installation et Utilisation](#installation-et-utilisation)
3. [Pipeline de Traitement](#pipeline-de-traitement)
4. [Résultats de l'Audit (V1 vs V2)](#résultats-de-laudit-v1-vs-v2)
5. [Conformité et Éthique](#conformité-et-éthique)

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
│   └── pipeline/     # Code source de la pipeline (Load, Clean, Bias, Anonymize)
├── tests/            # Tests unitaires Pytest
└── README.md
```

## Installation et Utilisation

### 1. Prérequis
* **Python 3.9+**
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

## 📊 Résultats de l'Audit (V1 vs V2)

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


## Auteur
Brice Gandon