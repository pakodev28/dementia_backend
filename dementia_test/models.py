from django.db import models

from core.mixins import DateMixin


class DementiaTestCase(DateMixin):
    updated_at = None

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Прохождение теста"
        verbose_name_plural = "Прохождения тестов"

    def __str__(self):
        return f"Тест №{self.pk}, {self.created_at}"


class Answer(DateMixin):
    updated_at = None
    answer_value = models.CharField("Значение ответа", max_length=255)
    test_case = models.ForeignKey(DementiaTestCase, on_delete=models.CASCADE, verbose_name="Прохождение теста")
    question = models.PositiveSmallIntegerField("Номер вопроса")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Ответ на вопрос"
        verbose_name_plural = "Ответы на вопросы"

    def __str__(self):
        return f"Вопрос №{self.question}: {self.answer_value}"
