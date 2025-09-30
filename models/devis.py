"""
Modèles Devis et DevisLigne
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Devis(Base):
    """Modèle représentant un devis"""
    __tablename__ = 'devis'

    # Clé primaire
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Numéro unique du devis
    numero = Column(String(50), unique=True, nullable=False)

    # Relation avec le client
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    client = relationship('Client', back_populates='devis')

    # Dates
    date_emission = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_validite = Column(DateTime, nullable=False)

    # Statut
    statut = Column(String(20), nullable=False, default='en_attente')
    # 'en_attente', 'accepte', 'refuse', 'expire'

    # Montant
    montant_total_ht = Column(Numeric(10, 2), nullable=False, default=0)

    # Conditions particulières
    conditions = Column(Text)

    # Métadonnées
    date_creation = Column(DateTime, default=datetime.utcnow, nullable=False)
    date_modification = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relations
    lignes = relationship('DevisLigne', back_populates='devis', cascade='all, delete-orphan', order_by='DevisLigne.ordre')
    factures = relationship('Facture', back_populates='devis')

    def __repr__(self):
        """Représentation textuelle du devis"""
        return f"<Devis(id={self.id}, numero='{self.numero}', montant={self.montant_total_ht}€)>"


class DevisLigne(Base):
    """Modèle représentant une ligne de devis"""
    __tablename__ = 'devis_lignes'

    # Clé primaire
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relation avec le devis
    devis_id = Column(Integer, ForeignKey('devis.id'), nullable=False)
    devis = relationship('Devis', back_populates='lignes')

    # Référence optionnelle à une prestation du catalogue
    prestation_id = Column(Integer, ForeignKey('prestations.id'), nullable=True)

    # Informations de la ligne
    libelle = Column(String(200), nullable=False)
    description = Column(Text)
    quantite = Column(Numeric(10, 2), nullable=False, default=1)
    prix_unitaire_ht = Column(Numeric(10, 2), nullable=False)
    montant_total_ligne_ht = Column(Numeric(10, 2), nullable=False)

    # Ordre d'affichage
    ordre = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        """Représentation textuelle de la ligne de devis"""
        return f"<DevisLigne(id={self.id}, libelle='{self.libelle}', montant={self.montant_total_ligne_ht}€)>"