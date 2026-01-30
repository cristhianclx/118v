# iniciar el proyecto
python -m venv venv # crea un entorno virtual

# activar el entorno virtual
source venv/bin/activate # linux
.\venv\Scripts\activate.bat # windows
.\venv\Scripts\Activate.ps1 # windows

pip install -r requirements.txt
pip install -r requirements.txt --upgrade

pip install Flask # instalar un paquete

pip freeze # ver lo instalado

deactivate # desactiva el entorno virtual

# python
https://www.python.org/downloads/


#
source venv\Scripts\activate.bat
flask --app main run --reload

# windows - permisos
# abrir power shell como administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser