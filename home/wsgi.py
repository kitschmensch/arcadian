import os
from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")

application = get_wsgi_application()


application = get_wsgi_application()
root = os.path.join(os.path.dirname(__file__), "static")
print("WhiteNoise is serving static files from %s" % root)
application = WhiteNoise(application, root=root)
