from django.db import models


class PublishQuerySet(models.QuerySet):
    """Фильтрация только активных записей."""

    def active(self):
        return self.filter(is_active=True)
