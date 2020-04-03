
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wrp_server.settings')

import django
django.setup()

from core.models import Picture, Painter
