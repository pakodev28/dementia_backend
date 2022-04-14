import csv

from django.contrib import admin
from django.http import HttpResponse

from dementia_test.models import Answer, DementiaTestCase


class AnswersInline(admin.TabularInline):
    model = Answer


@admin.register(DementiaTestCase)
class DementiaTestCaseAdmin(admin.ModelAdmin):
    actions = ["download_csv"]
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

    @admin.action(description="Скачать в CSV")
    def download_csv(self, request, queryset):
        """Downloads TestCase(s) queryset as a .csv file."""

        filename = "testcase_data.csv"
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
        writer = csv.writer(response)
        writer.writerow(["Test case ID", "Question ID", "Answer Value"])
        for testcase in queryset:
            answers = testcase.answers.all().order_by("question")
            for answer in answers:
                writer.writerow([answer.test_case_id, answer.question, answer.answer_value])
        return response

    @admin.display(description="Ответы")
    def answers(self, obj):
        return " | ".join([f"Вопрос №{answer.question}: {answer.answer_value}" for answer in obj.answers.all()])


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "answer_value", "test_case", "question")
    list_filter = ("created_at", "test_case")
    search_fields = ("answer_value", "question")
