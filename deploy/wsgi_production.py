"""Waitress WSGI entry point for production deployment.

Usage:
    waitress-serve --listen=0.0.0.0:8000 --threads=8 --call core.wsgi:application

Windows Task Scheduler setup:
    schtasks /Create /TN "KeToanSME" /TR "waitress-serve --listen=0.0.0.0:8000 --threads=8 --call core.wsgi:application" /SC ONSTART /RL HIGHEST
"""

import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
