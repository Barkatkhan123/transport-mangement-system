@echo off
echo === TMS Project Setup ===
echo.

echo [1/5] Creating virtual environment...
python -m venv venv

echo [2/5] Activating virtual environment...
call venv\Scripts\activate

echo [3/5] Installing dependencies...
pip install -r requirements/dev.txt

echo [4/5] Copying .env file...
copy .env.example .env

echo [5/5] Running migrations...
python manage.py migrate

echo.
echo === Setup complete! ===
echo.
echo Next steps:
echo   1. Edit .env with your settings
echo   2. Run: venv\Scripts\activate
echo   3. Run: python manage.py createsuperuser
echo   4. Run: python manage.py runserver
echo   5. Open: http://127.0.0.1:8000
echo.
pause
