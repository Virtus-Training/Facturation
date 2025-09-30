"""
Modèle Paiement
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from .base import Base


class Paiement(Base):
    """Modèle représentant un paiement associé à une facture"""
    __tablename__ = 'paiements'

    # Clé primaire
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relation avec la facture
    facture_id = Column(Integer, ForeignKey('factures.id'), nullable=False)
    facture = relationship('Facture', back_populates='paiements')

    # Informations du paiement
    date_paiement = Column(Date, nullable=False)
    montant = Column(Numeric(10, 2), nullable=False)
    moyen_paiement = Column(String(50), nullable=False)  # 'especes', 'cheque', 'virement', etc.
    reference = Column(String(100))  # Numéro de chèque, référence virement, etc.

    # Notes
    notes = Column(Text)

    # Métadonnées
    date_creation = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        """Représentation textuelle du paiement"""
        return f"<Paiement(id={self.id}, montant={self.montant}€, moyen='{self.moyen_paiement}')>"