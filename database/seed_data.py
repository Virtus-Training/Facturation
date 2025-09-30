"""
Script pour initialiser la base de données avec des données de test
"""
from database.init_db import get_session
from models import Client, Prestation


def seed_clients():
    """Insère des clients de test dans la base de données"""
    session = get_session()

    # Vérifier si des clients existent déjà
    existing_count = session.query(Client).count()
    if existing_count > 0:
        print(f"[INFO] {existing_count} client(s) deja present(s) dans la base")
        session.close()
        return

    clients_data = [
        {
            'type': 'particulier',
            'nom': 'Dupont',
            'prenom': 'Marie',
            'adresse': '15 Rue de la République',
            'code_postal': '75001',
            'ville': 'Paris',
            'email': 'marie.dupont@email.fr',
            'telephone': '0612345678',
            'notes': 'Cliente régulière, préfère les séances matinales',
            'actif': True
        },
        {
            'type': 'particulier',
            'nom': 'Martin',
            'prenom': 'Pierre',
            'adresse': '28 Avenue des Champs',
            'code_postal': '69001',
            'ville': 'Lyon',
            'email': 'pierre.martin@gmail.com',
            'telephone': '0623456789',
            'notes': 'Objectif : perte de poids',
            'actif': True
        },
        {
            'type': 'entreprise',
            'raison_sociale': 'FitnessPro Lyon',
            'siret': '12345678901234',
            'adresse': '45 Boulevard Jean Jaurès',
            'code_postal': '69003',
            'ville': 'Lyon',
            'email': 'contact@fitnesspro-lyon.fr',
            'telephone': '0478123456',
            'notes': 'Salle de sport partenaire - Cours collectifs',
            'actif': True
        },
        {
            'type': 'particulier',
            'nom': 'Bernard',
            'prenom': 'Sophie',
            'adresse': '12 Rue Victor Hugo',
            'code_postal': '33000',
            'ville': 'Bordeaux',
            'email': 'sophie.bernard@outlook.fr',
            'telephone': '0634567890',
            'notes': 'Coaching nutrition + sport',
            'actif': True
        },
        {
            'type': 'entreprise',
            'raison_sociale': 'Wellness Center Paris',
            'siret': '98765432109876',
            'adresse': '78 Rue de Rivoli',
            'code_postal': '75004',
            'ville': 'Paris',
            'email': 'admin@wellness-paris.com',
            'telephone': '0142567890',
            'notes': 'Centre de bien-être - Contrat annuel',
            'actif': True
        },
        {
            'type': 'particulier',
            'nom': 'Petit',
            'prenom': 'Jean',
            'adresse': '5 Place du Marché',
            'code_postal': '31000',
            'ville': 'Toulouse',
            'email': 'jean.petit@wanadoo.fr',
            'telephone': '0645678901',
            'notes': 'Préparation marathon',
            'actif': True
        },
        {
            'type': 'particulier',
            'nom': 'Dubois',
            'prenom': 'Isabelle',
            'adresse': '33 Rue Nationale',
            'code_postal': '59000',
            'ville': 'Lille',
            'email': 'isabelle.dubois@free.fr',
            'telephone': '0656789012',
            'notes': 'Séances à domicile uniquement',
            'actif': False
        },
        {
            'type': 'entreprise',
            'raison_sociale': 'GymClub Toulouse',
            'siret': '45678901234567',
            'adresse': '92 Avenue de la Libération',
            'code_postal': '31500',
            'ville': 'Toulouse',
            'email': 'info@gymclub-toulouse.fr',
            'telephone': '0561234567',
            'notes': 'Partenariat cours collectifs mardi/jeudi',
            'actif': True
        },
        {
            'type': 'particulier',
            'nom': 'Moreau',
            'prenom': 'Thomas',
            'adresse': '18 Rue du Commerce',
            'code_postal': '13001',
            'ville': 'Marseille',
            'email': 'thomas.moreau@hotmail.com',
            'telephone': '0667890123',
            'notes': 'Client depuis 2 ans - Très assidu',
            'actif': True
        },
        {
            'type': 'particulier',
            'nom': 'Laurent',
            'prenom': 'Caroline',
            'adresse': '7 Impasse des Lilas',
            'code_postal': '44000',
            'ville': 'Nantes',
            'email': 'caroline.laurent@orange.fr',
            'telephone': '0678901234',
            'notes': 'Post-natal fitness',
            'actif': True
        }
    ]

    print("[INFO] Insertion de clients de test...")

    for client_data in clients_data:
        client = Client(**client_data)
        session.add(client)

    session.commit()
    print(f"[OK] {len(clients_data)} clients de test inseres avec succes")
    session.close()


def seed_prestations():
    """Insère des prestations de test dans la base de données"""
    session = get_session()

    # Vérifier si des prestations existent déjà
    existing_count = session.query(Prestation).count()
    if existing_count > 0:
        print(f"[INFO] {existing_count} prestation(s) deja presente(s) dans la base")
        session.close()
        return

    prestations_data = [
        {
            'libelle': 'Séance coaching individuel',
            'description': 'Séance de coaching sportif personnalisé (1h)',
            'prix_unitaire_ht': 50.00,
            'unite': 'séance',
            'categorie': 'Coaching individuel',
            'actif': True
        },
        {
            'libelle': 'Forfait 10 séances',
            'description': 'Forfait de 10 séances de coaching individuel',
            'prix_unitaire_ht': 450.00,
            'unite': 'forfait',
            'categorie': 'Coaching individuel',
            'actif': True
        },
        {
            'libelle': 'Cours collectif',
            'description': 'Cours de fitness en groupe (1h)',
            'prix_unitaire_ht': 20.00,
            'unite': 'séance',
            'categorie': 'Cours collectif',
            'actif': True
        },
        {
            'libelle': 'Bilan nutritionnel',
            'description': 'Consultation et établissement d\'un programme nutritionnel personnalisé',
            'prix_unitaire_ht': 80.00,
            'unite': 'consultation',
            'categorie': 'Suivi nutritionnel',
            'actif': True
        },
        {
            'libelle': 'Suivi nutritionnel mensuel',
            'description': 'Suivi nutritionnel avec adaptation du programme (rencontre mensuelle)',
            'prix_unitaire_ht': 60.00,
            'unite': 'mois',
            'categorie': 'Suivi nutritionnel',
            'actif': True
        },
        {
            'libelle': 'Préparation physique sportif',
            'description': 'Programme de préparation physique spécifique (compétition, marathon, etc.)',
            'prix_unitaire_ht': 70.00,
            'unite': 'séance',
            'categorie': 'Préparation physique',
            'actif': True
        },
        {
            'libelle': 'Coaching à domicile',
            'description': 'Séance de coaching au domicile du client (déplacement inclus)',
            'prix_unitaire_ht': 65.00,
            'unite': 'séance',
            'categorie': 'Coaching individuel',
            'actif': True
        },
        {
            'libelle': 'Programme remise en forme',
            'description': 'Programme complet de remise en forme sur 3 mois (12 séances + suivi)',
            'prix_unitaire_ht': 550.00,
            'unite': 'programme',
            'categorie': 'Coaching individuel',
            'actif': True
        }
    ]

    print("[INFO] Insertion de prestations de test...")

    for prestation_data in prestations_data:
        prestation = Prestation(**prestation_data)
        session.add(prestation)

    session.commit()
    print(f"[OK] {len(prestations_data)} prestations de test inserees avec succes")
    session.close()


def seed_all():
    """Insère toutes les données de test"""
    print("\n=== Initialisation des donnees de test ===\n")
    seed_clients()
    seed_prestations()
    print("\n=== Donnees de test inserees avec succes ===\n")


if __name__ == "__main__":
    seed_all()