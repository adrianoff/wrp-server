from django.contrib import admin

# Register your models here.
from .models import Painter, Picture

admin.site.register(Painter)
admin.site.register(Picture)
