"""
Configuration globale de l'application Facturation Coach Pro
"""
import os
from pathlib import Path

# Chemins de base
BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
DOCUMENTS_DIR = BASE_DIR / "documents"
RESOURCES_DIR = BASE_DIR / "resources"
TEMPLATES_DIR = BASE_DIR / "templates"

# Base de données
DATABASE_PATH = DATABASE_DIR / "facturation.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Répertoires de sauvegarde des PDF
FACTURES_DIR = DOCUMENTS_DIR / "factures"
DEVIS_DIR = DOCUMENTS_DIR / "devis"
AVOIRS_DIR = DOCUMENTS_DIR / "avoirs"

# Paramètres de numérotation par défaut
FACTURE_PREFIX = "FACT"
DEVIS_PREFIX = "DEV"
AVOIR_PREFIX = "AV"
NUMERO_FORMAT = "{prefix}-{annee}-{numero:03d}"  # Ex: FACT-2025-001

# Paramètres de facturation par défaut
TVA_APPLICABLE = False
MENTION_TVA = "TVA non applicable, art. 293 B du CGI"
DELAI_PAIEMENT_DEFAUT = 0  # jours (0 = à réception)
TAUX_PENALITES = 3  # fois le taux d'intérêt légal
INDEMNITE_RECOUVREMENT = 40  # euros

# Paramètres de l'application
APP_NAME = "Facturation Coach Pro"
APP_VERSION = "1.0.0"
WINDOW_MIN_WIDTH = 1280
WINDOW_MIN_HEIGHT = 720

# Plafond auto-entrepreneur (prestations de services)
PLAFOND_AUTO_ENTREPRENEUR = 77700  # euros pour 2025

# Délai de validité devis par défaut
DEVIS_VALIDITE_DEFAUT = 90  # jours (3 mois)

# Logging
LOG_FILE = BASE_DIR / "logs" / "facturation.log"
LOG_LEVEL = "INFO"

# Créer les répertoires s'ils n'existent pas
def init_directories():
    """Crée les répertoires nécessaires au fonctionnement de l'application"""
    dirs_to_create = [
        DATABASE_DIR,
        DOCUMENTS_DIR,
        FACTURES_DIR,
        DEVIS_DIR,
        AVOIRS_DIR,
        RESOURCES_DIR,
        TEMPLATES_DIR,
        BASE_DIR / "logs"
    ]

    for directory in dirs_to_create:
        directory.mkdir(parents=True, exist_ok=True)

    # Créer des sous-dossiers par année pour les factures
    from datetime import datetime
    current_year = datetime.now().year
    for year_dir in [FACTURES_DIR, DEVIS_DIR, AVOIRS_DIR]:
        (year_dir / str(current_year)).mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    init_directories()
    print("Repertoires initialises avec succes!")