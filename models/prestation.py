"""
Modèle Prestation
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Text
from .base import Base


class Prestation(Base):
    """Modèle représentant une prestation type du catalogue"""
    __tablename__ = 'prestations'

    # Clé primaire
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Informations de la prestation
    libelle = Column(String(200), nullable=False)
    description = Column(Text)

    # Tarification
    prix_unitaire_ht = Column(Numeric(10, 2), nullable=False)  # Prix en euros
    unite = Column(String(50), nullable=False)  # 'séance', 'heure', 'forfait', 'mois', etc.

    # Catégorisation
    categorie = Column(String(100))  # 'coaching individuel', 'cours collectif', etc.

    # Statut
    actif = Column(Boolean, default=True, nullable=False)

    # Métadonnées
    date_creation = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        """Représentation textuelle de la prestation"""
        return f"<Prestation(id={self.id}, libelle='{self.libelle}', prix={self.prix_unitaire_ht}€)>"