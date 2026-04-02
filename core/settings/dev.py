"""Development settings."""

from .base import *  # noqa: F401,F403

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Development logging - more verbose
LOGGING['root']['level'] = 'DEBUG'  # noqa: F405

# Disable SSL redirect for development
SECURE_SSL_REDIRECT = False

# Enable Django Debug Toolbar if available
try:
    import debug_toolbar  # noqa: F401
    INSTALLED_APPS.append('debug_toolbar')  # noqa: F405
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa: F405
    INTERNAL_IPS = ['127.0.0.1']
except ImportError:
    pass
