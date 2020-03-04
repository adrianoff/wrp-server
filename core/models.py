from django.db import models


class Painter(models.Model):
    name = models.CharField(max_length=255)
    url = models.TextField()


class Picture(models.Model):
    painter = models.ForeignKey(Painter, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    file = models.ImageField(upload_to='static/pictures', default='')
    link_info = models.TextField()
