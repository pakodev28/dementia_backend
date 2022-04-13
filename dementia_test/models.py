from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from core.mixins import DateMixin


class DementiaTestCase(DateMixin):
    updated_at = None

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Прохождение теста"
        verbose_name_plural = "Прохождения тестов"

    def __str__(self):
        return f"Тест №{self.pk}, {timezone.localtime(self.created_at).strftime('%d.%m.%Y %H:%M')}"


class Answer(DateMixin):
    updated_at = None
    answer_value = models.CharField("Значение ответа", max_length=255, null=True)
    test_case = models.ForeignKey(
        DementiaTestCase, on_delete=models.CASCADE, related_name="answers", verbose_name="Прохождение теста"
    )
    question = models.PositiveSmallIntegerField(
        "Номер вопроса", validators=[MinValueValidator(1), MaxValueValidator(25)]
    )
    image = models.ImageField(upload_to="answer/", verbose_name="Изображение", null=True)

    class Meta:
        unique_together = ("test_case", "question")
        ordering = ["-created_at"]
        verbose_name = "Ответ на вопрос"
        verbose_name_plural = "Ответы на вопросы"
