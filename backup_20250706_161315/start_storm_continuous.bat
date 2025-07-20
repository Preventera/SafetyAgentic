@echo off
echo 🚀 Démarrage STORM Déploiement Continu
cd /d "C:\Users\Mario\Documents\PROJECTS_NEW\SafeGraph"

REM Installer dépendances
pip install -r requirements_continuous.txt

REM Créer répertoire logs
if not exist "logs" mkdir logs

REM Démarrer service continu
echo ⏰ Lancement en mode service...
python continuous_deployment.py

pause
