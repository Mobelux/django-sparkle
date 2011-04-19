import os

from django.conf import settings

SPARKLE_PRIVATE_KEY_PATH = getattr(settings, 'SPARKLE_PRIVATE_KEY_PATH', None)
