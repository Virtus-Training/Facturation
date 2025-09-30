"""
Fonctions de validation pour les formulaires
"""
import re


def validate_email(email: str) -> bool:
    """
    Valide le format d'une adresse email.

    Args:
        email: Adresse email à valider

    Returns:
        bool: True si le format est valide, False sinon
    """
    if not email:
        return False

    # Pattern regex pour email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_siret(siret: str) -> tuple[bool, str]:
    """
    Valide un numéro SIRET français (14 chiffres).

    Args:
        siret: Numéro SIRET à valider

    Returns:
        tuple: (valid: bool, message: str)
    """
    if not siret:
        return False, "Le SIRET est obligatoire pour les entreprises"

    # Retirer les espaces et tirets
    siret_clean = siret.replace(' ', '').replace('-', '')

    # Vérifier que c'est 14 chiffres
    if not siret_clean.isdigit():
        return False, "Le SIRET doit contenir uniquement des chiffres"

    if len(siret_clean) != 14:
        return False, f"Le SIRET doit contenir 14 chiffres (actuellement {len(siret_clean)})"

    return True, "SIRET valide"


def validate_code_postal(code: str) -> bool:
    """
    Valide un code postal français (5 chiffres).

    Args:
        code: Code postal à valider

    Returns:
        bool: True si le format est valide, False sinon
    """
    if not code:
        return False

    # Retirer les espaces
    code_clean = code.replace(' ', '')

    # Vérifier que c'est 5 chiffres
    return code_clean.isdigit() and len(code_clean) == 5


def validate_telephone(tel: str) -> bool:
    """
    Valide un numéro de téléphone français (10 chiffres).

    Args:
        tel: Numéro de téléphone à valider

    Returns:
        bool: True si le format est valide, False sinon
    """
    if not tel:
        return True  # Le téléphone est optionnel

    # Retirer les espaces, points, tirets
    tel_clean = tel.replace(' ', '').replace('.', '').replace('-', '')

    # Vérifier que c'est 10 chiffres commençant par 0
    return tel_clean.isdigit() and len(tel_clean) == 10 and tel_clean.startswith('0')


def format_telephone(tel: str) -> str:
    """
    Formate un numéro de téléphone français.
    Exemple: 0612345678 -> 06 12 34 56 78

    Args:
        tel: Numéro de téléphone à formater

    Returns:
        str: Numéro formaté
    """
    if not tel:
        return ""

    # Retirer les espaces, points, tirets
    tel_clean = tel.replace(' ', '').replace('.', '').replace('-', '')

    # Si pas valide, retourner tel quel
    if not (tel_clean.isdigit() and len(tel_clean) == 10):
        return tel

    # Formater par paires: 06 12 34 56 78
    return f"{tel_clean[0:2]} {tel_clean[2:4]} {tel_clean[4:6]} {tel_clean[6:8]} {tel_clean[8:10]}"


def format_siret(siret: str) -> str:
    """
    Formate un numéro SIRET.
    Exemple: 12345678901234 -> 123 456 789 01234

    Args:
        siret: Numéro SIRET à formater

    Returns:
        str: SIRET formaté
    """
    if not siret:
        return ""

    # Retirer les espaces et tirets
    siret_clean = siret.replace(' ', '').replace('-', '')

    # Si pas valide, retourner tel quel
    if not (siret_clean.isdigit() and len(siret_clean) == 14):
        return siret

    # Formater: 123 456 789 01234
    return f"{siret_clean[0:3]} {siret_clean[3:6]} {siret_clean[6:9]} {siret_clean[9:14]}"


def validate_required_field(value: str, field_name: str = "Ce champ") -> tuple[bool, str]:
    """
    Valide qu'un champ obligatoire n'est pas vide.

    Args:
        value: Valeur du champ
        field_name: Nom du champ pour le message d'erreur

    Returns:
        tuple: (valid: bool, message: str)
    """
    if not value or not value.strip():
        return False, f"{field_name} est obligatoire"

    return True, ""


if __name__ == "__main__":
    # Tests des validateurs
    print("=== Tests des validateurs ===\n")

    # Test email
    print("Test email:")
    print(f"  test@example.com: {validate_email('test@example.com')}")
    print(f"  invalid-email: {validate_email('invalid-email')}")

    # Test SIRET
    print("\nTest SIRET:")
    print(f"  12345678901234: {validate_siret('12345678901234')}")
    print(f"  123456789: {validate_siret('123456789')}")
    print(f"  Format: {format_siret('12345678901234')}")

    # Test code postal
    print("\nTest code postal:")
    print(f"  75001: {validate_code_postal('75001')}")
    print(f"  7500: {validate_code_postal('7500')}")

    # Test téléphone
    print("\nTest telephone:")
    print(f"  0612345678: {validate_telephone('0612345678')}")
    print(f"  06 12 34 56 78: {validate_telephone('06 12 34 56 78')}")
    print(f"  Format: {format_telephone('0612345678')}")
    print(f"  123: {validate_telephone('123')}")