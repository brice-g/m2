# Brief 1 — Audit et documentation du dataset FastIA

## Contexte du projet

Votre modèle Llama 3.2 1B fine-tuné est en production chez FastIA et traite les demandes clients entrantes. Mais côté amont, la chaîne d'alimentation en données est restée artisanale : le dataset d'entraînement a été constitué à la main par un ancien stagiaire, sans documentation, sans script de préparation, sans traçabilité. L'équipe data doit maintenant l'industrialiser : plusieurs briefs d'entraînement sont prévus dans les mois à venir, et chaque itération doit pouvoir s'appuyer sur un processus reproductible et auditable.

Votre manager vous confie la première mission de ce chantier : **reprendre le dataset existant, l'auditer sous l'angle qualité et conformité, et produire la documentation qui manque**. Avant de nettoyer quoi que ce soit, il faut comprendre ce qu'on a entre les mains.

---

## Objectif principal

Produire une datasheet complète du dataset FastIA, documenter le cycle de vie de la donnée, et remonter un diagnostic argumenté sur la qualité du jeu de données et les biais potentiels à investiguer au Brief 2.

---

## Prérequis

- Module 1 complété : dataset `dataset_fastia_module1.jsonl` disponible
- Environnement Python avec Pandas, Matplotlib/Seaborn, Jupyter

---

## Dataset

Vous reprenez le fichier utilisé en Module 1 :

```
dataset_fastia_module1.jsonl
```

Chaque ligne :

```json
{
  "input": "texte de la demande client",
  "output": {
    "categorie": "...",
    "priorite": "...",
    "reponse_suggeree": "..."
  }
}
```

Catégories : `Support technique`, `Demande commerciale`, `Demande de transformation`, `Réclamation`, `Information générale`
Priorités : `haute`, `normale`

---

## Étapes du projet

### 1. Mise en place

- Créer un nouveau dépôt GitHub `fastia-data-pipeline` ou une branche `module-2` du dépôt existant
- Créer un environnement virtuel, installer :

```bash
pip install pandas numpy matplotlib seaborn jupyter
```

- Versionner le dataset dans `data/raw/dataset_fastia_module1.jsonl`

### 2. Audit quantitatif

Charger le dataset dans un notebook `notebook_brief1_module2.ipynb` et produire :

- Nombre total d'exemples
- Distribution des catégories (effectifs + pourcentages)
- Distribution des priorités (globale et par catégorie)
- Distribution des longueurs de `input` (en caractères et en tokens approximatifs)
- Distribution des longueurs de `reponse_suggeree`
- Détection de doublons exacts ou quasi-exacts sur `input`
- Détection de valeurs manquantes ou vides sur chaque champ

Chaque chiffre doit être accompagné d'une visualisation claire (histogramme, barplot ou heatmap selon la question).

### 3. Audit qualitatif

Échantillonner 20 exemples (4 par catégorie, tirés aléatoirement) et pour chacun, noter :

- La cohérence entre `input` et `categorie`
- La cohérence entre le ton de la demande et la `priorite` assignée
- La pertinence et le style de la `reponse_suggeree`
- La présence d'éléments potentiellement sensibles dans `input` (noms, coordonnées, identifiants techniques)

Consigner les observations dans un tableau dans le notebook.

### 4. Datasheet du dataset

Produire un fichier `docs/datasheet.md` inspiré du format *Datasheets for Datasets* (Gebru et al.) couvrant a minima :

- **Motivation** — pourquoi ce dataset a été créé, pour quelle tâche
- **Composition** — structure, volumétrie, types de champs, valeurs possibles
- **Collecte** — qui a collecté, comment, sur quelle période (à reconstituer au mieux)
- **Prétraitements** — ce qui a déjà été fait sur les données brutes (aujourd'hui : rien de documenté)
- **Usages recommandés et déconseillés**
- **Considérations éthiques** — risques identifiés, données sensibles potentielles
- **Maintenance** — qui maintient, comment signaler un problème, versioning

### 5. Documentation du flux de traitement

Produire un fichier `docs/data_lifecycle.md` qui décrit :

- **Chaîne d'approvisionnement actuelle** — d'où viennent les demandes (canaux imaginés : email, formulaire web, chat), comment elles ont été converties en JSONL
- **Cycle de vie actuel** — de l'ingestion jusqu'à l'utilisation par le fine-tuning
- **Schéma du flux** — un diagramme simple (Mermaid ou ASCII) montrant : sources → ingestion → stockage → préparation → entraînement → modèle
- **Points de rupture identifiés** — étapes non reproductibles, non versionnées, non monitorées

### 6. Diagnostic de qualité

Rédiger une synthèse d'une page (`docs/audit_v1.md`) répondant à :

- Le dataset est-il équilibré ? Sur quelles dimensions ?
- Quels problèmes de qualité sont déjà visibles à l'audit (doublons, incohérences, valeurs suspectes) ?
- Quels biais sont à investiguer plus sérieusement au Brief 2 ?
- Quelles données du dataset relèvent de données personnelles ou sensibles au sens du RGPD ?
- Quelles actions correctives prioriser pour le Brief 2 ?

Ce diagnostic est le point d'entrée du Brief 2.

---

## Livrables

- **Dépôt GitHub** versionné avec :
  - `data/raw/dataset_fastia_module1.jsonl`
  - `notebook_brief1_module2.ipynb`
  - `docs/datasheet.md`
  - `docs/data_lifecycle.md`
  - `docs/audit_v1.md`
- **README.md** décrivant la structure du dépôt, la procédure d'installation et de lancement du notebook

---

## Charge de travail estimée

5 à 6 heures

---

## Ressources

- Gebru et al. — *Datasheets for Datasets* (2018)
- [Pandas — Data profiling](https://pandas.pydata.org/docs/user_guide/)
- [CNIL — Données personnelles et RGPD](https://www.cnil.fr/fr/rgpd-de-quoi-parle-t-on)

---

## Bonus

- Produire une matrice catégorie × priorité avec effectifs et comparaison à la distribution attendue
- Calculer une distance de Jaccard ou de Levenshtein sur les `input` pour détecter les quasi-doublons au-delà de la correspondance exacte
