from django.db import models


class Painter(models.Model):
    name = models.CharField(max_length=255)
    url = models.TextField()

    def __str__(self):
        return self.name


class Picture(models.Model):
    painter = models.ForeignKey(Painter, on_delete=models.PROTECT, null=False)
    name = models.CharField(max_length=255)
    year = models.CharField(max_length=4, null=True, blank=True)
    file = models.ImageField(upload_to='pictures', default='')
    link_info = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
