from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

from dementia_test.models import Answer, DementiaTestCase, ResultAnswer


class AnswersInline(admin.TabularInline):
    model = Answer


@admin.register(DementiaTestCase)
class DementiaTestCaseAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "answers")
    readonly_fields = (
        "id",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("answers__answer_value", "answers__question")
    inlines = [
        AnswersInline,
    ]

    @admin.display(description="Вопрос:ответ:баллы")
    def answers(self, obj):
        result = []
        for answer in obj.answers.all():
            try:
                result_value = ResultAnswer.objects.get(question_id=answer.id).answer_value
            except ObjectDoesNotExist:
                result_value = "-"
            if answer.question == 26:
                result.append(f"Итого: {result_value} бал.")
            else:
                result.append(f"№{answer.question}: {answer.answer_value}: {result_value}")
        return " | ".join(result)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "answer_value", "test_case", "question")
    list_filter = ("created_at", "test_case")

    search_fields = ("answer_value", "question")
