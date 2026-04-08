import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boutique_ai_saas.settings")

application = get_wsgi_application()

