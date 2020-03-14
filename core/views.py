from django.http import HttpResponse
from django.shortcuts import render

from core.models import Picture
import random
import json


def index(request):
    return HttpResponse('ok')


def get_random_picture(request):
    pictures_ids = list(Picture.objects.filter().values_list('id', flat=True))
    picture_id = random.choice(pictures_ids)
    picture = Picture.objects.get(pk=picture_id)

    picture_dict = {
        'id': picture.id,
        'file': picture.file.url,
        'link_info': picture.link_info,
        'name': picture.name,
        'year': picture.year,
        'painter': picture.painter.name
    }

    return HttpResponse(json.dumps(picture_dict))
