"""Production settings."""

from .base import *  # noqa: F401,F403

DEBUG = False

# Security settings for intranet
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Configure ALLOWED_HOSTS for local network
# Set via environment variable in production
import os  # noqa: E402
ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1'
).split(',')
