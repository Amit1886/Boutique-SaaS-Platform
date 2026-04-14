# PythonAnywhere (Flask backend)

1) Upload/clone repo on PythonAnywhere.
2) Create virtualenv (Python 3.10/3.11):
   - `python -m venv ~/.virtualenvs/bvp`
   - `source ~/.virtualenvs/bvp/bin/activate`
   - `pip install -r boutique_virtual_suite_pro/backend/requirements.txt`
3) Set env vars in a `.env` next to `run.py` (or in WSGI file).
4) Point WSGI to `deployment/pythonanywhere/wsgi_flask.py` and set the project path.
5) Run migrations:
   - `flask --app boutique_virtual_suite_pro/backend/run.py db upgrade`

