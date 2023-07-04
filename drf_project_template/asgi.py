"""
ASGI config for drf_project_template project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from decouple import config

from django.core.asgi import get_asgi_application

setting_module: str = config("DJANGO_SETTINGS_MODULE", "drf_project_template.settings.local")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting_module)

application = get_asgi_application()
