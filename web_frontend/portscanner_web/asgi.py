"""
ASGI config for portscanner_web project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portscanner_web.settings')

application = get_asgi_application()
