"""
Modèles Avoir et AvoirLigne
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from .base import Base


class Avoir(Base):
    """Modèle représentant un avoir (note de crédit)"""
    __tablename__ = 'avoirs'

    # Clé primaire
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Numéro unique de l'avoir
    numero = Column(String(50), unique=True, nullable=False)

    # Relation avec la facture d'origine
    facture_id = Column(Integer, ForeignKey('factures.id'), nullable=False)
    facture = relationship('Facture', back_populates='avoirs')

    # Date d'émission
    date_emission = Column(Date, nullable=False)

    # Montant total (négatif)
    montant_total = Column(Numeric(10, 2), nullable=False)

    # Motif de l'avoir
    motif = Column(Text, nullable=False)

    # Métadonnées
    date_creation = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relations
    lignes = relationship('AvoirLigne', back_populates='avoir', cascade='all, delete-orphan', order_by='AvoirLigne.ordre')

    def __repr__(self):
        """Représentation textuelle de l'avoir"""
        return f"<Avoir(id={self.id}, numero='{self.numero}', montant={self.montant_total}€)>"


class AvoirLigne(Base):
    """Modèle représentant une ligne d'avoir"""
    __tablename__ = 'avoirs_lignes'

    # Clé primaire
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relation avec l'avoir
    avoir_id = Column(Integer, ForeignKey('avoirs.id'), nullable=False)
    avoir = relationship('Avoir', back_populates='lignes')

    # Référence optionnelle à une prestation
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
        """Représentation textuelle de la ligne d'avoir"""
        return f"<AvoirLigne(id={self.id}, libelle='{self.libelle}', montant={self.montant_total_ligne_ht}€)>"