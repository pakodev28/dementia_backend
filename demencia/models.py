from django.db import models

from core.mixins import DateMixin, PublishMixin


class Partner(DateMixin, PublishMixin):
    image = models.ImageField(upload_to='partners/', verbose_name='Изображение')
    name = models.CharField(max_length='250', verbose_name='Название партнёра')

    class Meta:
        orgering = ['-updated_at']
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'
