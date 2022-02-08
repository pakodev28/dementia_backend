from django.contrib import admin

from dementia_test.models import DementiaTestCase, Answer


class AnswersInline(admin.TabularInline):
    model = Answer


@admin.register(DementiaTestCase)
class DementiaTestCaseAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
    readonly_fields = (
        "id",
        "created_at",
    )

    inlines = [
        AnswersInline,
    ]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "answer_value", "test_case", "question")
