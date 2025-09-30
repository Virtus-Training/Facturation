"""
Controller pour la gestion des clients
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from database import get_session
from models import Client, Facture, Devis
from utils.validators import (
    validate_email, validate_siret, validate_code_postal,
    validate_telephone, validate_required_field
)


class ClientController:
    """Contrôleur pour gérer les opérations CRUD sur les clients"""

    def __init__(self):
        """Initialise le contrôleur"""
        self.session: Session = get_session()

    def get_all_clients(self, actif_only: bool = False) -> list[Client]:
        """
        Récupère tous les clients.

        Args:
            actif_only: Si True, ne retourne que les clients actifs

        Returns:
            list[Client]: Liste des clients
        """
        try:
            query = self.session.query(Client)

            if actif_only:
                query = query.filter(Client.actif == True)

            return query.order_by(Client.nom, Client.prenom).all()

        except Exception as e:
            print(f"[ERREUR] get_all_clients: {e}")
            return []

    def get_client_by_id(self, client_id: int) -> Client | None:
        """
        Récupère un client par son ID.

        Args:
            client_id: ID du client

        Returns:
            Client | None: Le client trouvé ou None
        """
        try:
            return self.session.query(Client).filter(Client.id == client_id).first()

        except Exception as e:
            print(f"[ERREUR] get_client_by_id: {e}")
            return None

    def search_clients(
        self,
        query: str,
        type_client: str | None = None,
        actif: bool | None = None
    ) -> list[Client]:
        """
        Recherche des clients par nom, email ou SIRET.

        Args:
            query: Texte de recherche
            type_client: Filtre par type ('particulier', 'entreprise', ou None)
            actif: Filtre par statut actif (True, False, ou None)

        Returns:
            list[Client]: Liste des clients correspondants
        """
        try:
            db_query = self.session.query(Client)

            # Recherche textuelle
            if query:
                search_filter = or_(
                    Client.nom.ilike(f"%{query}%"),
                    Client.prenom.ilike(f"%{query}%"),
                    Client.raison_sociale.ilike(f"%{query}%"),
                    Client.email.ilike(f"%{query}%"),
                    Client.siret.ilike(f"%{query}%")
                )
                db_query = db_query.filter(search_filter)

            # Filtre par type
            if type_client:
                db_query = db_query.filter(Client.type == type_client)

            # Filtre par statut actif
            if actif is not None:
                db_query = db_query.filter(Client.actif == actif)

            return db_query.order_by(Client.nom, Client.prenom).all()

        except Exception as e:
            print(f"[ERREUR] search_clients: {e}")
            return []

    def create_client(self, data: dict) -> tuple[bool, str, Client | None]:
        """
        Crée un nouveau client avec validation.

        Args:
            data: Dictionnaire contenant les données du client

        Returns:
            tuple: (success: bool, message: str, client: Client | None)
        """
        try:
            # Validation des champs obligatoires selon le type
            type_client = data.get('type', 'particulier')

            if type_client == 'entreprise':
                valid, msg = validate_required_field(data.get('raison_sociale', ''), "La raison sociale")
                if not valid:
                    return False, msg, None

                # Valider SIRET
                valid, msg = validate_siret(data.get('siret', ''))
                if not valid:
                    return False, msg, None

            else:  # particulier
                valid, msg = validate_required_field(data.get('nom', ''), "Le nom")
                if not valid:
                    return False, msg, None

            # Valider adresse
            valid, msg = validate_required_field(data.get('adresse', ''), "L'adresse")
            if not valid:
                return False, msg, None

            # Valider code postal
            if not validate_code_postal(data.get('code_postal', '')):
                return False, "Le code postal doit contenir 5 chiffres", None

            # Valider ville
            valid, msg = validate_required_field(data.get('ville', ''), "La ville")
            if not valid:
                return False, msg, None

            # Valider email
            if not validate_email(data.get('email', '')):
                return False, "L'adresse email n'est pas valide", None

            # Valider téléphone (optionnel)
            telephone = data.get('telephone', '')
            if telephone and not validate_telephone(telephone):
                return False, "Le numéro de téléphone n'est pas valide (10 chiffres)", None

            # Créer le client
            client = Client(
                type=type_client,
                nom=data.get('nom', '').strip(),
                prenom=data.get('prenom', '').strip(),
                raison_sociale=data.get('raison_sociale', '').strip(),
                adresse=data.get('adresse', '').strip(),
                code_postal=data.get('code_postal', '').strip(),
                ville=data.get('ville', '').strip(),
                email=data.get('email', '').strip(),
                telephone=telephone.strip() if telephone else None,
                siret=data.get('siret', '').replace(' ', '').replace('-', '') if data.get('siret') else None,
                notes=data.get('notes', '').strip(),
                actif=data.get('actif', True)
            )

            self.session.add(client)
            self.session.commit()
            self.session.refresh(client)

            return True, "Client créé avec succès", client

        except Exception as e:
            self.session.rollback()
            print(f"[ERREUR] create_client: {e}")
            return False, f"Erreur lors de la création du client: {str(e)}", None

    def update_client(self, client_id: int, data: dict) -> tuple[bool, str, Client | None]:
        """
        Met à jour un client existant.

        Args:
            client_id: ID du client à modifier
            data: Dictionnaire contenant les nouvelles données

        Returns:
            tuple: (success: bool, message: str, client: Client | None)
        """
        try:
            client = self.get_client_by_id(client_id)

            if not client:
                return False, "Client introuvable", None

            # Validation des champs obligatoires selon le type
            type_client = data.get('type', client.type)

            if type_client == 'entreprise':
                valid, msg = validate_required_field(data.get('raison_sociale', ''), "La raison sociale")
                if not valid:
                    return False, msg, None

                # Valider SIRET
                valid, msg = validate_siret(data.get('siret', ''))
                if not valid:
                    return False, msg, None

            else:  # particulier
                valid, msg = validate_required_field(data.get('nom', ''), "Le nom")
                if not valid:
                    return False, msg, None

            # Valider adresse
            valid, msg = validate_required_field(data.get('adresse', ''), "L'adresse")
            if not valid:
                return False, msg, None

            # Valider code postal
            if not validate_code_postal(data.get('code_postal', '')):
                return False, "Le code postal doit contenir 5 chiffres", None

            # Valider ville
            valid, msg = validate_required_field(data.get('ville', ''), "La ville")
            if not valid:
                return False, msg, None

            # Valider email
            if not validate_email(data.get('email', '')):
                return False, "L'adresse email n'est pas valide", None

            # Valider téléphone (optionnel)
            telephone = data.get('telephone', '')
            if telephone and not validate_telephone(telephone):
                return False, "Le numéro de téléphone n'est pas valide (10 chiffres)", None

            # Mettre à jour les champs
            client.type = type_client
            client.nom = data.get('nom', '').strip()
            client.prenom = data.get('prenom', '').strip()
            client.raison_sociale = data.get('raison_sociale', '').strip()
            client.adresse = data.get('adresse', '').strip()
            client.code_postal = data.get('code_postal', '').strip()
            client.ville = data.get('ville', '').strip()
            client.email = data.get('email', '').strip()
            client.telephone = telephone.strip() if telephone else None
            client.siret = data.get('siret', '').replace(' ', '').replace('-', '') if data.get('siret') else None
            client.notes = data.get('notes', '').strip()

            if 'actif' in data:
                client.actif = data['actif']

            self.session.commit()
            self.session.refresh(client)

            return True, "Client modifié avec succès", client

        except Exception as e:
            self.session.rollback()
            print(f"[ERREUR] update_client: {e}")
            return False, f"Erreur lors de la modification du client: {str(e)}", None

    def delete_client(self, client_id: int) -> tuple[bool, str]:
        """
        Supprime un client.
        Refuse la suppression si le client a des factures ou devis associés.

        Args:
            client_id: ID du client à supprimer

        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            client = self.get_client_by_id(client_id)

            if not client:
                return False, "Client introuvable"

            # Vérifier s'il y a des factures
            nb_factures = self.session.query(func.count(Facture.id)).filter(
                Facture.client_id == client_id
            ).scalar()

            if nb_factures > 0:
                return False, f"Impossible de supprimer: le client a {nb_factures} facture(s) associée(s)"

            # Vérifier s'il y a des devis
            nb_devis = self.session.query(func.count(Devis.id)).filter(
                Devis.client_id == client_id
            ).scalar()

            if nb_devis > 0:
                return False, f"Impossible de supprimer: le client a {nb_devis} devis associé(s)"

            # Supprimer le client
            self.session.delete(client)
            self.session.commit()

            return True, "Client supprimé avec succès"

        except Exception as e:
            self.session.rollback()
            print(f"[ERREUR] delete_client: {e}")
            return False, f"Erreur lors de la suppression du client: {str(e)}"

    def toggle_active(self, client_id: int) -> tuple[bool, str, bool]:
        """
        Active ou désactive un client.

        Args:
            client_id: ID du client

        Returns:
            tuple: (success: bool, message: str, new_status: bool)
        """
        try:
            client = self.get_client_by_id(client_id)

            if not client:
                return False, "Client introuvable", False

            client.actif = not client.actif
            self.session.commit()

            status_text = "activé" if client.actif else "désactivé"
            return True, f"Client {status_text} avec succès", client.actif

        except Exception as e:
            self.session.rollback()
            print(f"[ERREUR] toggle_active: {e}")
            return False, f"Erreur lors du changement de statut: {str(e)}", False

    def get_client_statistics(self, client_id: int) -> dict:
        """
        Retourne les statistiques d'un client.

        Args:
            client_id: ID du client

        Returns:
            dict: Dictionnaire avec nb_factures, nb_devis, ca_total
        """
        try:
            # Nombre de factures
            nb_factures = self.session.query(func.count(Facture.id)).filter(
                Facture.client_id == client_id
            ).scalar() or 0

            # Nombre de devis
            nb_devis = self.session.query(func.count(Devis.id)).filter(
                Devis.client_id == client_id
            ).scalar() or 0

            # CA total (somme des factures payées)
            ca_total = self.session.query(func.sum(Facture.montant_total_ht)).filter(
                Facture.client_id == client_id,
                Facture.statut == 'payee'
            ).scalar() or 0

            return {
                'nb_factures': nb_factures,
                'nb_devis': nb_devis,
                'ca_total': float(ca_total)
            }

        except Exception as e:
            print(f"[ERREUR] get_client_statistics: {e}")
            return {
                'nb_factures': 0,
                'nb_devis': 0,
                'ca_total': 0.0
            }

    def __del__(self):
        """Ferme la session à la destruction du contrôleur"""
        if hasattr(self, 'session'):
            self.session.close()