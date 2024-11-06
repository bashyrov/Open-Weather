"""
WSGI config for Weather project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
import sys
import os

from django.core.wsgi import get_wsgi_application


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openweather.settings')

application = get_wsgi_application()
