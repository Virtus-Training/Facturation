@echo off
echo ====================================
echo  Facturation Coach Pro - Lancement
echo ====================================
echo.

:: Vérifier si l'environnement virtuel existe
if not exist "venv\" (
    echo [INFO] Creation de l'environnement virtuel...
    python -m venv venv
    echo [OK] Environnement virtuel cree
    echo.
)

:: Activer l'environnement virtuel
echo [INFO] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

:: Installer les dépendances si nécessaire
echo [INFO] Verification des dependances...
pip install -q -r requirements.txt

echo.
echo [INFO] Demarrage de l'application...
echo.
python main.py

pause