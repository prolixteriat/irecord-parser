@echo off
echo Press any key to begin processing
cd .\Code\
pipenv run python main.py -i "..\Config\config.ini"
pause
