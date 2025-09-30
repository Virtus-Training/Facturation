"""
Point d'entrée de l'application Facturation Coach Pro
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from config import init_directories
from database import init_database
from views import MainWindow


def main():
    """Fonction principale de l'application"""
    # Initialiser les répertoires nécessaires
    init_directories()
    print("[OK] Repertoires initialises")

    # Initialiser la base de données
    if not init_database():
        print("[ERREUR] Echec de l'initialisation de la base de donnees")
        sys.exit(1)

    # Charger les données de test au premier lancement
    from database.seed_data import seed_all
    try:
        seed_all()
    except Exception as e:
        print(f"[INFO] Donnees de test: {e}")

    # Créer l'application Qt
    app = QApplication(sys.argv)

    # Configurer l'application
    app.setApplicationName("Facturation Coach Pro")
    app.setOrganizationName("Coach Pro")

    # Créer et afficher la fenêtre principale
    window = MainWindow()
    window.show()

    print("\n[OK] Application lancee avec succes!")
    print("[INFO] Interface prête a l'utilisation\n")

    # Lancer la boucle d'événements
    sys.exit(app.exec())


if __name__ == "__main__":
    main()