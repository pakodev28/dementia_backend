from django.db import models

from core.managers import PublishQuerySet


class DateMixin(models.Model):
    """Миксин добавления дат.

    Attributes:
        created_at: Дата создания
        updated_at: Дата обновления
    """

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-updated_at']


class PublishMixin(DateMixin):
    """Миксин публикаций.

    Attributes:
        is_active: Активность
    """

    is_active = models.BooleanField('Активность', default=True)

    active_objects = PublishQuerySet.as_manager()

    class Meta(DateMixin.Meta):
        pass
