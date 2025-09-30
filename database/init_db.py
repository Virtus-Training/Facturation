"""
Initialisation et gestion de la base de données SQLite
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import DATABASE_URL, DATABASE_PATH
from models import Base


# Engine global
engine = None
SessionLocal = None


def init_database():
    """
    Initialise la base de données et crée toutes les tables si elles n'existent pas.

    Returns:
        bool: True si l'initialisation est réussie
    """
    global engine, SessionLocal

    try:
        # Créer le répertoire database s'il n'existe pas
        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Créer l'engine SQLAlchemy
        engine = create_engine(
            DATABASE_URL,
            echo=False,  # Mettre à True pour voir les requêtes SQL (debug)
            connect_args={"check_same_thread": False}  # Nécessaire pour SQLite
        )

        # Créer toutes les tables
        Base.metadata.create_all(bind=engine)

        # Créer la factory de session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        print(f"[OK] Base de donnees initialisee avec succes : {DATABASE_PATH}")
        return True

    except Exception as e:
        print(f"[ERREUR] Erreur lors de l'initialisation de la base de donnees : {e}")
        return False


def get_session() -> Session:
    """
    Retourne une nouvelle session de base de données.

    Returns:
        Session: Session SQLAlchemy
    """
    global SessionLocal

    if SessionLocal is None:
        init_database()

    return SessionLocal()


def get_engine():
    """
    Retourne l'engine SQLAlchemy global.

    Returns:
        Engine: Engine SQLAlchemy
    """
    global engine

    if engine is None:
        init_database()

    return engine


if __name__ == "__main__":
    # Test de l'initialisation
    if init_database():
        # Afficher les tables créées
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        print("\nTables créées :")
        for table in tables:
            print(f"  - {table}")

        # Tester la création d'une session
        session = get_session()
        print(f"\n[OK] Session creee : {session}")
        session.close()