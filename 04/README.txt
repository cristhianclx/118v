python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt --upgrade
flask --app main run --reload

flask --app main db init # 1ra vez
flask --app main db migrate # crea la migracion
flask --app main db upgrade # aplicar la migracion

flask --app main shell

>>> from main import db, User
>>> item = User(code="0001", first_name="alan", last_name="garcia", age=60)
>>> db.session.add(item)
>>> db.session.commit()

>>> from main import db, User
>>> User.query.all()