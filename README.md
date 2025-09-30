# Facturation Coach Pro

Logiciel de facturation pour coach sportif en auto-entreprise, conforme à la réglementation française.

## 🎯 Description

Application desktop développée en Python avec PyQt6 pour la gestion complète du cycle de facturation :
- Gestion des clients (particuliers et entreprises)
- Catalogue de prestations
- Création de devis
- Génération de factures conformes
- Suivi des paiements
- Création d'avoirs
- Tableau de bord et statistiques

## 📋 Prérequis

- Python 3.11 ou supérieur
- pip (gestionnaire de paquets Python)

## 🚀 Installation

### 1. Cloner ou télécharger le projet

```bash
cd c:\Users\Eric\Documents\Facturation
```

### 2. Créer un environnement virtuel (recommandé)

```bash
python -m venv venv
```

### 3. Activer l'environnement virtuel

**Windows :**
```bash
venv\Scripts\activate
```

**macOS/Linux :**
```bash
source venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

## ▶️ Lancement de l'application

```bash
python main.py
```

## 📁 Structure du projet

```
facturation_coach/
│
├── models/              # Modèles de données SQLAlchemy
│   ├── client.py        # Modèle Client
│   ├── prestation.py    # Modèle Prestation
│   ├── devis.py         # Modèles Devis et DevisLigne
│   ├── facture.py       # Modèles Facture et FactureLigne
│   ├── paiement.py      # Modèle Paiement
│   ├── avoir.py         # Modèles Avoir et AvoirLigne
│   └── parametre.py     # Modèle Parametre
│
├── views/               # Interfaces graphiques PyQt6
│   └── main_window.py   # Fenêtre principale
│
├── controllers/         # Logique métier
├── utils/              # Fonctions utilitaires
├── database/           # Gestion BDD
│   ├── init_db.py      # Initialisation de la base de données
│   └── facturation.db  # Base de données SQLite (générée)
│
├── templates/          # Templates PDF
├── resources/          # Images, icônes, styles
├── documents/          # Documents PDF générés
│   ├── factures/
│   ├── devis/
│   └── avoirs/
│
├── tests/              # Tests unitaires
├── config.py           # Configuration globale
├── main.py             # Point d'entrée
└── requirements.txt    # Dépendances Python
```

## 🗄️ Base de données

La base de données SQLite est créée automatiquement au premier lancement dans :
```
database/facturation.db
```

### Tables créées :
- `clients` - Informations clients
- `prestations` - Catalogue de prestations
- `devis` et `devis_lignes` - Devis
- `factures` et `factures_lignes` - Factures
- `paiements` - Suivi des paiements
- `avoirs` et `avoirs_lignes` - Avoirs (notes de crédit)
- `parametres` - Configuration de l'application

## 🎨 Interface

L'application dispose d'une interface moderne avec :
- **Menu latéral** : Navigation entre les sections
- **Tableau de bord** : Vue d'ensemble du CA et statistiques
- **Gestion clients** : CRUD complet
- **Prestations** : Catalogue personnalisable
- **Devis** : Création et suivi
- **Factures** : Génération conforme à la réglementation française
- **Avoirs** : Notes de crédit
- **Paramètres** : Configuration de l'entreprise

## ⚡ Fonctionnalités actuelles (Phase 1)

- ✅ Architecture MVC complète
- ✅ Base de données SQLite avec tous les modèles
- ✅ Interface PyQt6 avec navigation
- ✅ Structure de projet propre et extensible
- ✅ Vues placeholder pour toutes les sections

## 🔜 Prochaines étapes

1. **CRUD Clients** : Formulaires d'ajout/modification/suppression
2. **CRUD Prestations** : Gestion du catalogue
3. **Génération de factures PDF** : ReportLab avec mentions légales
4. **Suivi des paiements** : Enregistrement et statuts
5. **Tableau de bord** : Statistiques et graphiques
6. **Génération de devis** : Workflow complet
7. **Avoirs** : Création depuis factures

## 📝 Conformité réglementaire

L'application respecte les obligations légales françaises pour les factures :
- Mentions obligatoires (SIRET, TVA, etc.)
- Numérotation séquentielle continue
- Pénalités de retard et indemnité de recouvrement
- Conservation des documents (10 ans)

## 🛠️ Technologies utilisées

- **Python 3.11+**
- **PyQt6** - Interface graphique
- **SQLAlchemy** - ORM pour la base de données
- **SQLite** - Base de données locale
- **ReportLab** - Génération de PDF (à venir)

## 📄 Licence

Usage personnel - Développé pour coach sportif en auto-entreprise.

## 👤 Auteur

Développé avec ❤️ pour simplifier la gestion de facturation des coachs sportifs.

---

**Version :** 1.0.0
**Date :** 2025