# Cahier des Charges - Logiciel de Facturation pour Coach Sportif

## 1. CONTEXTE ET OBJECTIFS

### 1.1 Présentation du projet
Développement d'un logiciel de facturation local en Python destiné à un coach sportif en auto-entreprise, permettant la gestion complète du cycle de facturation (devis, factures, avoirs) en conformité avec la réglementation française.

### 1.2 Objectifs principaux
- Automatiser la création de documents comptables conformes
- Garantir le respect des obligations légales françaises
- Offrir une interface intuitive et professionnelle
- Centraliser la gestion clients et prestations
- Générer des livrables PDF de haute qualité

### 1.3 Utilisateur cible
Un utilisateur unique (le coach) utilisant le logiciel en local, sans besoin de connexion internet pour les fonctionnalités principales.

---

## 2. CONFORMITÉ RÉGLEMENTAIRE FRANÇAISE

### 2.1 Mentions obligatoires sur les factures

**Informations émetteur :**
- Nom et prénom (ou raison sociale)
- Adresse complète du siège social
- Numéro SIRET (14 chiffres)
- Forme juridique : "Auto-entrepreneur" ou "Micro-entrepreneur"
- Mention "TVA non applicable, art. 293 B du CGI" (franchise en base de TVA)
- Numéro de téléphone et email

**Informations client :**
- Nom/Prénom ou raison sociale
- Adresse complète de facturation
- Pour les entreprises : numéro SIRET

**Informations document :**
- Numéro de facture unique et séquentiel (ex: FACT-2025-001)
- Date d'émission
- Date de la prestation ou période de prestation
- Désignation précise des prestations
- Quantité et prix unitaire HT
- Total HT
- Mention "TVA non applicable, art. 293 B du CGI"
- Total TTC (= Total HT en auto-entreprise)
- Conditions de paiement
- Date limite de paiement
- Pénalités de retard (taux légal : 3 fois le taux d'intérêt légal)
- Indemnité forfaitaire de recouvrement : 40€

### 2.2 Règles de numérotation
- Numérotation chronologique continue sans rupture
- Pas de doublon ni de numéro manquant
- Format recommandé : FACT-AAAA-XXX ou FACT-AAAA-MM-XXX
- Séquence annuelle ou continue selon choix

### 2.3 Conservation
- Obligation de conservation : 10 ans
- Format PDF/A recommandé pour l'archivage

### 2.4 Devis
Mentions obligatoires similaires aux factures, avec :
- Numéro de devis unique
- Date de validité du devis (généralement 3 mois)
- Mention "Devis gratuit"
- Signature client pour acceptation

---

## 3. SPÉCIFICATIONS FONCTIONNELLES

### 3.1 Gestion des clients

**Création/Modification de fiches clients :**
- Type de client : Particulier / Entreprise (salle de sport)
- Nom/Prénom ou Raison sociale
- Adresse complète (rue, code postal, ville)
- Email
- Téléphone
- SIRET (optionnel pour particuliers, obligatoire pour entreprises)
- Notes/Commentaires libres
- Historique des documents associés

**Fonctionnalités :**
- Recherche rapide (nom, SIRET, email)
- Tri et filtres
- Import/Export CSV
- Archivage des clients inactifs
- Suppression avec protection (impossible si factures existantes)

### 3.2 Gestion des prestations

**Catalogue de prestations :**
- Libellé de la prestation
- Description détaillée
- Prix unitaire HT par défaut
- Unité (séance, heure, forfait, mois)
- Catégorie (coaching individuel, cours collectif, suivi nutritionnel, etc.)
- Statut actif/inactif

**Fonctionnalités :**
- Création de prestations types personnalisables
- Modification des prix par document (sans modifier le catalogue)
- Duplication de prestations
- Historique d'utilisation

### 3.3 Création de devis

**Workflow :**
1. Sélection du client
2. Ajout de prestations (avec possibilité de modifier quantité, libellé, prix)
3. Calculs automatiques
4. Prévisualisation
5. Génération PDF
6. Enregistrement en base

**Champs spécifiques :**
- Numéro auto-généré
- Date d'émission
- Date de validité (par défaut : +3 mois)
- Conditions particulières (zone texte libre)
- Statut : En attente / Accepté / Refusé / Expiré

**Fonctionnalités :**
- Conversion devis → facture en un clic
- Duplication de devis
- Envoi par email (optionnel)
- Export PDF

### 3.4 Création de factures

**Workflow similaire aux devis :**
1. Création manuelle ou conversion depuis devis
2. Sélection du client
3. Ajout de prestations
4. Choix des conditions de paiement
5. Génération PDF

**Champs spécifiques :**
- Numéro auto-généré séquentiel
- Date d'émission
- Date/période de prestation
- Mode de paiement (espèces, chèque, virement, CB, Stripe, PayPal, etc.)
- Échéance de paiement (par défaut : à réception, ou +15/30 jours)
- Statut : Brouillon / Émise / Payée / Partiellement payée / En retard / Annulée

**Fonctionnalités :**
- Suivi des paiements (date, montant, moyen)
- Relances automatiques pour factures impayées
- Génération d'avoirs
- Export comptable (CSV compatible expert-comptable)
- Statistiques (CA mensuel/annuel)

### 3.5 Gestion des avoirs

**Création :**
- Lié obligatoirement à une facture existante
- Numéro auto-généré (AV-AAAA-XXX)
- Montant total ou partiel
- Motif de l'avoir

**Mentions obligatoires :**
- Référence à la facture d'origine
- Même mentions légales qu'une facture
- Total négatif

### 3.6 Tableau de bord

**Vue d'ensemble :**
- Chiffre d'affaires du mois/trimestre/année
- Factures en attente de paiement
- Factures en retard (liste et montant)
- Prochaines échéances
- Graphiques : évolution CA, répartition par type de prestation
- Alertes : plafond auto-entrepreneur (77 700€ en 2025 pour prestations de services)

### 3.7 Paramètres et configuration

**Informations légales (coach) :**
- Identité complète
- SIRET
- Adresse
- Contacts (téléphone, email, site web)
- Logo (upload image, PNG/JPG)
- RIB pour paiements par virement

**Paramètres de facturation :**
- Préfixes de numérotation (FACT-, DEV-, AV-)
- Format de numérotation
- Conditions de paiement par défaut
- Mentions légales personnalisées
- Pied de page personnalisé

**Paramètres techniques :**
- Répertoire de sauvegarde des PDF
- Paramètres d'email (SMTP) - optionnel
- Thème de l'interface (clair/sombre)
- Langue (prévoir FR uniquement phase 1)

---

## 4. SPÉCIFICATIONS TECHNIQUES

### 4.1 Technologies recommandées

**Langage et framework :**
- Python 3.11+
- Interface graphique : **PyQt6** (moderne, puissant) ou **CustomTkinter** (plus simple)
- Base de données : **SQLite** (local, léger, intégré)
- Génération PDF : **ReportLab** ou **WeasyPrint** (pour HTML→PDF)
- ORM : **SQLAlchemy** (gestion BDD élégante)

### 4.2 Architecture logicielle

**Structure MVC (Model-View-Controller) :**
```
/facturation_coach/
│
├── /models/           # Modèles de données (Client, Facture, Prestation...)
├── /views/            # Interfaces graphiques (fenêtres, widgets)
├── /controllers/      # Logique métier
├── /utils/            # Fonctions utilitaires (PDF, validations...)
├── /database/         # Gestion BDD et migrations
├── /templates/        # Templates PDF
├── /resources/        # Images, icônes, styles CSS
├── /tests/            # Tests unitaires
├── config.py          # Configuration globale
├── main.py            # Point d'entrée
└── requirements.txt   # Dépendances Python
```

### 4.3 Base de données

**Tables principales :**

**clients**
- id (PK, auto-increment)
- type (particulier/entreprise)
- nom
- prenom
- raison_sociale
- adresse
- code_postal
- ville
- email
- telephone
- siret
- notes
- actif (boolean)
- date_creation
- date_modification

**prestations**
- id (PK)
- libelle
- description
- prix_unitaire_ht
- unite
- categorie
- actif (boolean)
- date_creation

**devis**
- id (PK)
- numero (unique)
- client_id (FK)
- date_emission
- date_validite
- statut
- montant_total_ht
- conditions
- date_creation
- date_modification

**devis_lignes**
- id (PK)
- devis_id (FK)
- prestation_id (FK nullable)
- libelle
- description
- quantite
- prix_unitaire_ht
- montant_total_ligne_ht
- ordre

**factures**
- id (PK)
- numero (unique)
- client_id (FK)
- devis_id (FK nullable)
- date_emission
- date_prestation_debut
- date_prestation_fin
- date_echeance
- statut
- montant_total_ht
- mode_paiement
- conditions_paiement
- notes
- date_creation
- date_modification

**factures_lignes** (même structure que devis_lignes)

**paiements**
- id (PK)
- facture_id (FK)
- date_paiement
- montant
- moyen_paiement
- reference
- notes

**avoirs**
- id (PK)
- numero (unique)
- facture_id (FK)
- date_emission
- montant_total
- motif
- date_creation

**avoirs_lignes**

**parametres**
- id (PK)
- cle (unique)
- valeur
- type

### 4.4 Génération de PDF

**Spécifications design :**
- Format A4 (210 × 297 mm)
- Marges : 20mm minimum
- Police professionnelle : Helvetica, Arial ou similaire
- Taille : 10-12pt pour le corps, 14-16pt pour les titres
- Logo en en-tête (max 150px hauteur)
- Couleurs : palette sobre et professionnelle (bleu/gris recommandé)

**Structure du template facture :**
1. En-tête : Logo + informations coach (gauche) / Infos client (droite)
2. Titre : "FACTURE" en grand
3. Informations document : numéro, dates
4. Tableau prestations (lignes séparées)
5. Totaux (HT, mention TVA, TTC)
6. Conditions de paiement et mentions légales
7. Pied de page : coordonnées bancaires, contacts

**Fonctionnalités :**
- Génération en mémoire (prévisualisation)
- Sauvegarde automatique dans /documents/factures/AAAA/
- Nommage : FACT-2025-001_NomClient.pdf
- Métadonnées PDF (titre, auteur, sujet)
- Protection contre modification (optionnel)

### 4.5 Sécurité et sauvegarde

**Sécurité :**
- Validation des entrées utilisateur (anti-injection SQL)
- Hachage des données sensibles si nécessaire
- Logs des opérations critiques (création facture, modification numéro)

**Sauvegarde :**
- Sauvegarde automatique de la BDD (daily, weekly)
- Export complet BDD + PDF (fonction backup)
- Restauration depuis backup

### 4.6 Performance

**Optimisations :**
- Indexation BDD sur champs recherchés (numéro facture, client, dates)
- Pagination des listes (50-100 éléments)
- Lazy loading des documents
- Cache des calculs lourds

---

## 5. SPÉCIFICATIONS INTERFACE UTILISATEUR (GUI)

### 5.1 Principes de design

**Standards modernes :**
- Design épuré, professionnel
- Palette de couleurs cohérente (2-3 couleurs principales max)
- Typographie lisible et hiérarchisée
- Espacement généreux entre éléments
- Feedback visuel immédiat (boutons, champs)
- Icônes explicites (Material Design ou Font Awesome)

**Accessibilité :**
- Contraste suffisant (WCAG AA minimum)
- Tailles de police ajustables
- Navigation clavier possible
- Messages d'erreur clairs et constructifs

### 5.2 Navigation principale

**Menu latéral ou barre supérieure :**
- 🏠 Tableau de bord
- 👥 Clients
- 📋 Prestations
- 📄 Devis
- 🧾 Factures
- 💰 Avoirs
- ⚙️ Paramètres

**Barre de recherche globale** (en haut) :
- Recherche rapide clients, factures, devis par numéro/nom

### 5.3 Écrans principaux

#### 5.3.1 Tableau de bord
- Cartes métriques (CA mois, factures impayées, alertes)
- Graphiques interactifs (évolution CA, répartition prestations)
- Liste des actions récentes
- Accès rapides (nouvelle facture, nouveau client)

#### 5.3.2 Liste des clients
- Tableau avec colonnes : Nom, Type, Email, Téléphone, Nb factures, Statut
- Filtres : Type, Statut (actif/inactif), Recherche
- Actions par ligne : ✏️ Modifier / 🗑️ Supprimer / 👁️ Voir détail
- Bouton : ➕ Nouveau client

#### 5.3.3 Fiche client (popup ou nouvelle page)
- Formulaire clair avec sections : Informations générales / Coordonnées / Informations légales
- Validation en temps réel (SIRET, email, code postal)
- Onglet historique : liste des documents associés
- Boutons : 💾 Enregistrer / ❌ Annuler

#### 5.3.4 Liste des factures
- Tableau : Numéro, Client, Date, Montant TTC, Statut, Échéance
- Filtres : Statut, Période, Client
- Indicateur visuel statut (couleur : vert=payé, orange=en attente, rouge=retard)
- Actions : 👁️ Voir / ✏️ Modifier / 📄 PDF / 💳 Enregistrer paiement / 🔁 Créer avoir
- Bouton : ➕ Nouvelle facture / 📊 Exporter (CSV)

#### 5.3.5 Création/Modification de facture
**Wizard en étapes ou formulaire unique :**

**Section 1 : Informations générales**
- Client (dropdown avec recherche)
- Date d'émission (datepicker)
- Période de prestation (datepicker range)
- Numéro (auto, affiché en lecture seule)

**Section 2 : Prestations**
- Tableau dynamique : Prestation / Description / Quantité / Prix unitaire / Total ligne
- Bouton ➕ Ajouter ligne (depuis catalogue ou ligne libre)
- Bouton ➖ Supprimer ligne
- Calcul automatique du total

**Section 3 : Conditions de paiement**
- Mode de paiement (dropdown)
- Échéance (dropdown : À réception / +15j / +30j / Date personnalisée)
- Notes internes (optionnel)

**Section 4 : Prévisualisation**
- Aperçu PDF directement dans l'interface
- Bouton : 💾 Enregistrer / 📧 Enregistrer et envoyer / 🖨️ Imprimer

#### 5.3.6 Paramètres
**Onglets :**
- **Mon entreprise** : formulaire infos légales + upload logo
- **Facturation** : préfixes, numérotation, conditions par défaut
- **Apparence** : thème, couleurs (optionnel phase 1)
- **Sauvegarde** : boutons backup/restauration, emplacement fichiers

### 5.4 Composants réutilisables

**Éléments standards :**
- Boutons primaires / secondaires / danger (styles cohérents)
- Champs de formulaire avec labels et validation inline
- Tableaux triables et filtrables
- Modales de confirmation (suppression, actions critiques)
- Notifications toast (succès, erreur, info)
- Datepickers cohérents
- Dropdowns avec recherche (clients, prestations)

### 5.5 Responsive (optionnel phase 1)
- Application desktop, résolution minimale : 1280×720
- Adaptation future tablette possible avec PyQt6

---

## 6. FONCTIONNALITÉS AVANCÉES (Phase 2 - Optionnelles)

### 6.1 Email intégré
- Paramétrage SMTP
- Envoi automatique factures/devis par email
- Templates emails personnalisables
- Historique des envois

### 6.2 Relances automatiques
- Configuration des règles (J+7, J+15, J+30 après échéance)
- Génération automatique d'emails de relance
- Historique des relances par facture

### 6.3 Export comptable
- Export CSV format expert-comptable (FEC)
- Récapitulatif annuel (déclaration CA)
- Journal des recettes

### 6.4 Multi-devises (si clients internationaux)
- Gestion EUR et autres devises
- Taux de change (API ou manuel)

### 6.5 Récurrence
- Factures récurrentes (abonnements mensuels)
- Génération automatique selon planning

### 6.6 Statistiques avancées
- Analyse clients (top clients, CA par client)
- Analyse prestations (best sellers)
- Prévisionnel CA
- Export Excel/PDF rapports

### 6.7 Synchronisation cloud (très optionnel)
- Backup automatique Dropbox/Google Drive
- Accès multi-appareils (avec prudence sécurité)

---

## 7. PARCOURS UTILISATEUR TYPES

### 7.1 Créer une première facture (nouveau client)
1. Lancer l'application
2. Aller dans "Clients" → "Nouveau client"
3. Remplir le formulaire client → Enregistrer
4. Aller dans "Factures" → "Nouvelle facture"
5. Sélectionner le client créé
6. Ajouter des prestations depuis le catalogue (ou créer à la volée)
7. Ajuster quantités/prix si besoin
8. Choisir mode et échéance de paiement
9. Prévisualiser → Enregistrer
10. PDF généré et sauvegardé automatiquement

**Temps estimé : 3-5 minutes**

### 7.2 Convertir un devis accepté en facture
1. Aller dans "Devis"
2. Ouvrir le devis accepté
3. Cliquer sur "Convertir en facture"
4. Vérifier les informations pré-remplies
5. Ajuster si nécessaire (dates, conditions)
6. Enregistrer → Facture créée automatiquement

**Temps estimé : 30 secondes**

### 7.3 Enregistrer un paiement
1. Aller dans "Factures"
2. Trouver la facture (filtre "En attente")
3. Cliquer sur "Enregistrer paiement"
4. Renseigner date, montant, moyen de paiement
5. Valider → Statut facture passe à "Payée"

**Temps estimé : 30 secondes**

### 7.4 Créer un avoir
1. Ouvrir la facture concernée
2. Cliquer sur "Créer un avoir"
3. Sélectionner lignes à rembourser (total ou partiel)
4. Indiquer le motif
5. Générer → PDF avoir créé, lié à la facture

**Temps estimé : 1 minute**

---

## 8. TESTS ET VALIDATION

### 8.1 Tests unitaires
- Calculs (totaux, taxes si applicable)
- Numérotation séquentielle
- Validations (SIRET, email, dates)
- Génération PDF (conformité mentions légales)

### 8.2 Tests d'intégration
- Workflow complet : création client → devis → facture → paiement
- Conversion devis → facture
- Génération avoir

### 8.3 Tests utilisateur
- Tests d'utilisabilité (facilité de navigation)
- Tests de performance (temps de génération PDF, chargement listes)
- Tests sur différentes résolutions écran

### 8.4 Checklist de conformité légale
- ✅ Toutes mentions obligatoires présentes
- ✅ Numérotation continue sans rupture
- ✅ Conservation des documents (backup)
- ✅ Mentions TVA correctes
- ✅ Pénalités de retard présentes

---

## 9. LIVRABLES ATTENDUS

### 9.1 Logiciel
- Application exécutable (Windows/macOS/Linux selon besoins)
- Base de données SQLite initialisée
- Templates PDF configurables
- Documentation technique (README, installation, architecture)

### 9.2 Documentation utilisateur
- Guide de prise en main (PDF)
- Tutoriels vidéo (optionnel)
- FAQ
- Aide contextuelle intégrée

### 9.3 Support
- Changelog (suivi des versions)
- Procédure de mise à jour
- Contact support (toi-même, mais anticiper futures questions)

---

## 10. PLANNING DE DÉVELOPPEMENT SUGGÉRÉ

### Phase 1 : Fondations (2-3 semaines)
- ✅ Architecture projet
- ✅ Base de données (models + migrations)
- ✅ Interface de base (navigation, thème)
- ✅ CRUD clients
- ✅ CRUD prestations

### Phase 2 : Facturation core (3-4 semaines)
- ✅ Création factures
- ✅ Génération PDF conforme
- ✅ Numérotation automatique
- ✅ Liste et gestion factures
- ✅ Enregistrement paiements

### Phase 3 : Devis et avoirs (2 semaines)
- ✅ Gestion devis
- ✅ Conversion devis → facture
- ✅ Création avoirs

### Phase 4 : Tableau de bord et stats (1-2 semaines)
- ✅ Métriques CA
- ✅ Graphiques
- ✅ Alertes impayés

### Phase 5 : Paramètres et finitions (1 semaine)
- ✅ Configuration entreprise
- ✅ Personnalisation templates
- ✅ Backup/restauration
- ✅ Logs

### Phase 6 : Tests et documentation (1 semaine)
- ✅ Tests complets
- ✅ Corrections bugs
- ✅ Documentation utilisateur
- ✅ Packaging application

**Total estimé : 10-13 semaines** (à temps plein, ajuster selon ton rythme)

---

## 11. RISQUES ET POINTS D'ATTENTION

### 11.1 Risques techniques
- **Complexité génération PDF** : prévoir temps d'apprentissage ReportLab/WeasyPrint
- **Numérotation séquentielle** : attention aux concurrences (peu probable en local mono-utilisateur)
- **Performance BDD** : anticiper avec indexation dès le début

### 11.2 Risques légaux
- **Non-conformité mentions** : valider avec un expert-comptable ou juriste
- **Évolution réglementation** : prévoir veille et mises à jour (ex: taux pénalités)

### 11.3 Risques métier
- **Dépassement plafond auto-entrepreneur** : intégrer alerte dès conception
- **Changement statut juridique** : anticiper migration future (TVA, EURL...)

### 11.4 Recommandations
- **Valider les templates PDF** avec un expert-comptable avant utilisation réelle
- **Tester avec données réelles** (anonymisées) avant mise en production
- **Backup régulier** : crucial pour données comptables (obligation 10 ans)

---

## 12. ÉVOLUTIONS FUTURES POSSIBLES

### 12.1 Court terme (6 mois)
- Ajout récurrence factures
- Relances automatiques
- Export comptable (FEC)
- Statistiques avancées

### 12.2 Moyen terme (1 an)
- Intégration paiement en ligne (Stripe, PayPal)
- Application mobile (consultation, relances)
- Multi-utilisateurs (assistant, secrétaire)

### 12.3 Long terme (2 ans+)
- Synchronisation cloud sécurisée
- API pour intégration avec autres outils (planning, nutrition)
- Module de gestion de trésorerie
- Intégration bancaire (réconciliation automatique)

---

## CONCLUSION

Ce cahier des charges couvre l'ensemble des besoins pour un logiciel de facturation professionnel, conforme et intuitif. L'approche modulaire permet de développer par phases, en priorisant les fonctionnalités essentielles avant d'ajouter les options avancées.
