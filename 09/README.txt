python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt --upgrade
flask --app main run --reload

flask --app main db init # 1ra vez
flask --app main db migrate # crea la migracion
flask --app main db upgrade # aplicar la migracion
