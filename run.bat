@echo off
echo Press any key to begin processing
cd .\Code\
python -m pipenv run python main.py -i "..\Config\config.ini"
pause
