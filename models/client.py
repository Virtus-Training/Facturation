"""
Modèle Client
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from .base import Base


class Client(Base):
    """Modèle représentant un client (particulier ou entreprise)"""
    __tablename__ = 'clients'

    # Clé primaire
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Type de client
    type = Column(String(20), nullable=False)  # 'particulier' ou 'entreprise'

    # Informations d'identité
    nom = Column(String(100))  # Obligatoire pour particulier, vide pour entreprise
    prenom = Column(String(100))
    raison_sociale = Column(String(200))  # Obligatoire pour entreprise, vide pour particulier

    # Coordonnées
    adresse = Column(String(200))
    code_postal = Column(String(10))
    ville = Column(String(100))
    email = Column(String(100))
    telephone = Column(String(20))

    # Informations légales
    siret = Column(String(14))  # 14 chiffres pour SIRET

    # Notes
    notes = Column(Text)

    # Statut
    actif = Column(Boolean, default=True, nullable=False)

    # Métadonnées
    date_creation = Column(DateTime, default=datetime.utcnow, nullable=False)
    date_modification = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relations
    devis = relationship('Devis', back_populates='client', cascade='all, delete-orphan')
    factures = relationship('Facture', back_populates='client', cascade='all, delete-orphan')

    def __repr__(self):
        """Représentation textuelle du client"""
        if self.type == 'entreprise':
            return f"<Client(id={self.id}, raison_sociale='{self.raison_sociale}')>"
        else:
            return f"<Client(id={self.id}, nom='{self.nom}', prenom='{self.prenom}')>"

    @property
    def nom_complet(self):
        """Retourne le nom complet du client selon son type"""
        if self.type == 'entreprise':
            return self.raison_sociale or ''
        else:
            return f"{self.prenom or ''} {self.nom}".strip()

    @property
    def adresse_complete(self):
        """Retourne l'adresse complète formatée"""
        parties = []
        if self.adresse:
            parties.append(self.adresse)
        if self.code_postal and self.ville:
            parties.append(f"{self.code_postal} {self.ville}")
        return '\n'.join(parties)