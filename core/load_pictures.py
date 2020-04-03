import os
import json
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wrp_server.settings')

import django
django.setup()

from core.models import Picture, Painter


with open('../pictures_final.json', 'r', encoding="utf-8") as json_file:
    data = json.load(json_file)
    for painter in data:
        painter_url = painter['painter_url']
        painter_name = painter['painter_name']

        try:
            painter_object = Painter.objects.get(url=painter_url)
        except Painter.DoesNotExist:
            painter_object = Painter()
            painter_object.name = painter_name
            painter_object.url = painter_url
            painter_object.save()

        for picture in painter['pictures']:
            picture_url = picture['picture_url']
            try:
                picture_object = Picture.objects.get(link_info=picture_url)
            except Picture.DoesNotExist:
                picture_object = Picture()

            picture_object.link_info = picture_url
            picture_object.painter = painter_object
            picture_object.name = picture['picture_name']
            picture_object.file = 'static/pictures/' + picture['filename']
            picture_object.save()
