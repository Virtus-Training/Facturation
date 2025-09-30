"""
Modèles Facture et FactureLigne
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from .base import Base


class Facture(Base):
    """Modèle représentant une facture"""
    __tablename__ = 'factures'

    # Clé primaire
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Numéro unique de la facture
    numero = Column(String(50), unique=True, nullable=False)

    # Relation avec le client
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    client = relationship('Client', back_populates='factures')

    # Référence optionnelle au devis d'origine
    devis_id = Column(Integer, ForeignKey('devis.id'), nullable=True)
    devis = relationship('Devis', back_populates='factures')

    # Dates
    date_emission = Column(Date, nullable=False)
    date_prestation_debut = Column(Date, nullable=True)
    date_prestation_fin = Column(Date, nullable=True)
    date_echeance = Column(Date, nullable=False)

    # Statut
    statut = Column(String(30), nullable=False, default='brouillon')
    # 'brouillon', 'emise', 'payee', 'partiellement_payee', 'en_retard', 'annulee'

    # Montant
    montant_total_ht = Column(Numeric(10, 2), nullable=False, default=0)

    # Paiement
    mode_paiement = Column(String(50))  # 'especes', 'cheque', 'virement', 'cb', 'stripe', 'paypal'
    conditions_paiement = Column(Text)

    # Notes
    notes = Column(Text)

    # Métadonnées
    date_creation = Column(DateTime, default=datetime.utcnow, nullable=False)
    date_modification = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relations
    lignes = relationship('FactureLigne', back_populates='facture', cascade='all, delete-orphan', order_by='FactureLigne.ordre')
    paiements = relationship('Paiement', back_populates='facture', cascade='all, delete-orphan')
    avoirs = relationship('Avoir', back_populates='facture', cascade='all, delete-orphan')

    def __repr__(self):
        """Représentation textuelle de la facture"""
        return f"<Facture(id={self.id}, numero='{self.numero}', montant={self.montant_total_ht}€)>"

    @property
    def montant_paye(self):
        """Calcule le montant total payé pour cette facture"""
        return sum(p.montant for p in self.paiements)

    @property
    def montant_restant(self):
        """Calcule le montant restant à payer"""
        return float(self.montant_total_ht) - float(self.montant_paye)


class FactureLigne(Base):
    """Modèle représentant une ligne de facture"""
    __tablename__ = 'factures_lignes'

    # Clé primaire
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relation avec la facture
    facture_id = Column(Integer, ForeignKey('factures.id'), nullable=False)
    facture = relationship('Facture', back_populates='lignes')

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
        """Représentation textuelle de la ligne de facture"""
        return f"<FactureLigne(id={self.id}, libelle='{self.libelle}', montant={self.montant_total_ligne_ht}€)>"