from django.db import models

from core.managers import PublishQuerySet


class DateMixin(models.Model):
    """Миксин добавления дат.

    Attributes:
        created_at: Дата создания
        updated_at: Дата обновления
    """

    created_at = models.DateTimeField("Дата создания", auto_now_add=True, help_text="Заполняется автоматически")
    updated_at = models.DateTimeField("Дата обновления", auto_now=True, help_text="Заполняется автоматически")

    class Meta:
        abstract = True
        ordering = ["-updated_at"]


class PublishMixin(models.Model):
    """Миксин публикаций.

    Attributes:
        is_active: Активность
    """

    is_active = models.BooleanField("Активность", default=True, help_text="Включить/отключить показ на сайте")

    objects = PublishQuerySet.as_manager()

    class Meta:
        abstract = True
