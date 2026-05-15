# Stratégie d'Augmentation des Données (Objectif : 150 lignes)

## 1. Analyse des cibles d'augmentation
L'objectif est de passer de 96 à environ 150 exemples en corrigeant les déséquilibres majeurs :

* **Rééquilibrage des priorités :** Passer de 29% à environ 40% de priorité haute.
* **Casser la corrélation "Information = Normal" :** Créer des exemples d'Information générale avec une priorité haute.
* **Neutralisation du biais de longueur :** Allonger les textes de la catégorie Information générale.
* **Anonymisation native :** Tous les nouveaux exemples utiliseront des tokens `[NOM]`, `[PRENOM]`, `[TEL]`, `[EMAIL]`, et `[ADRESSE]`.

## 2. Plan opérationnel

| Cible | Volume | Technique | Description & Consignes |
| :--- | :--- | :--- | :--- |
| **Information générale x Haute** | +20 | Gabarits | Créer des demandes d'info urgentes (ex: "Besoin [NOM] du catalogue avant mon RDV de 14h"). |
| **Toutes catégories x Haute** | +24 | Paraphrase (Llama-3.2) | Transformer des messages normaux existants en messages urgents en ajoutant du stress lexical. |
| **Information générale (Long)** | +10 | Paraphrase (Llama-3.2) | Étendre des messages courts existants pour atteindre ~150-200 caractères. |