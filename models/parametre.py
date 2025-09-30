"""
Modèle Parametre
"""
from sqlalchemy import Column, Integer, String, Text
from .base import Base


class Parametre(Base):
    """Modèle représentant un paramètre de configuration de l'application"""
    __tablename__ = 'parametres'

    # Clé primaire
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Clé unique du paramètre
    cle = Column(String(100), unique=True, nullable=False)

    # Valeur du paramètre (stockée en texte)
    valeur = Column(Text)

    # Type de donnée (pour faciliter la conversion)
    type = Column(String(20), nullable=False, default='string')
    # 'string', 'integer', 'float', 'boolean', 'json'

    def __repr__(self):
        """Représentation textuelle du paramètre"""
        return f"<Parametre(cle='{self.cle}', valeur='{self.valeur}', type='{self.type}')>"