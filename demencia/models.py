from django.db import models


class BaseModel(models.Model):
    """Абстрактная модель.

    Attributes:
        created_at: Дата создания
        updated_at: Дата обновления
        is_visible: Отображение
    """

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    is_visible = models.BooleanField('Отображение', default=True)

    class Meta:
        abstract = True
