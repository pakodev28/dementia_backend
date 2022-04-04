from django.contrib import admin

from dementia_test.models import Answer, DementiaTestCase


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

    @admin.display(description="Ответы")
    def answers(self, obj):
        return " | ".join([f"Вопрос №{answer.question}: {answer.answer_value}" for answer in obj.answers.all()])


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "answer_value", "test_case", "question")
    list_filter = ("created_at", "test_case")

    search_fields = ("answer_value", "question")
