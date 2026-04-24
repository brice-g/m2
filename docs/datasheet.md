# Datasheet : Dataset d’Entraînement FastIA (Support & Requêtes)

Ce document détaille les caractéristiques du dataset de 96 exemples utilisé pour le fine-tuning du modèle de réponse client.

---

## 1. Motivation
* **Pourquoi le dataset a-t-il été créé ?** Pour entraîner un modèle de langage à classifier les requêtes clients et à suggérer des réponses adaptées.
* **Pour quelle tâche ?** Classification multi-classe (catégorie), classification binaire (priorité) et génération de texte (réponse suggérée).

## 2. Composition
* **Volumétrie :** 96 exemples uniques.
* **Structure des données :** Le dataset contient 4 colonnes principales :

| Champ | Type | Description | Valeurs possibles |
| :--- | :--- | :--- | :--- |
| `input` | String | La requête brute du client | Moyenne de 100 caractères |
| `categorie` | String | Type de demande | Support technique, Information générale, Demande commerciale, Demande de transformation, Réclamation |
| `priorite` | String | Niveau d'urgence | `normale`, `haute` |
| `reponse_suggeree` | String | Proposition de réponse | Moyenne de 158 caractères |

**Distributions clés :**
* **Catégories :** Distribution relativement équilibrée (entre 17 et 22 exemples par classe).
* **Priorités :** Déséquilibre marqué avec 71% de priorité normale (68/96) contre 29% de priorité haute (28/96).
* **Contenu sensible :** L'audit a révélé la présence de **Données Identifiables (PII)** (noms, numéros de téléphone, emails) dans environ 11,5% des lignes (11/96).

## 3. Collecte
* **Comment les données ont-elles été collectées ?** Pas d'information. A voir avec le client.
* **Qui a collecté les données ?** Pas d'information. A voir avec le client.
* **Période de collecte :** Pas d'information. A voir avec le client.

## 4. Prétraitements
Aucune étape de nettoyage ou de normalisation n'a été documentée sur les données brutes.
* **État des doublons :** 0 doublon exact détecté sur le champ `input`.
* **Qualité :** 0 ligne vide, 0 valeur hors schéma.

## 5. Usages recommandés et déconseillés

### Usages recommandés
* Exercices de fine-tuning.

### Usages déconseillés
* **Mise en production immédiate :** À cause de la présence de PII.
* **Entraînement de modèles critiques :** La taille du dataset (96 lignes) est insuffisante pour garantir une bonne généralisation.
* **Décisions automatiques de priorité :** Le déséquilibre des classes de priorité pourrait biaiser le modèle.

## 6. Considérations éthiques
* **Risques identifiés (PII) :** Le dataset contient des informations réelles ou réalistes de clients (ex: Mme Dupont, M. Martin). L'utilisation de ce dataset sans anonymisation préalable présente un risque de fuite de données privées via le modèle entraîné.
* **Biais :** Le modèle pourrait favoriser les catégories "Support technique" et "Information générale" qui sont légèrement plus représentées. Aucun exemple de priorité Haute pour la catégorie "Information générale", pour le modèle une information générale ne pourra jamais avoir de priorité Haute (à confirmer avec le client)

## 7. Maintenance
* **Maintenance :** Dataset statique créé pour un exercice. Mise à jour prévue dans le prochain exercice.
* **Signalement d'erreurs :** A la personne qui a réalisée l'exercice.
* **Version :** 1.0.0