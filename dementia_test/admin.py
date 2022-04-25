import csv

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from dementia_test.models import Answer, DementiaTestCase, ResultAnswer


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
        answers_qty = 25  # кол-во вопросов в тесте

        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
        writer = csv.writer(response)
        csv_header = ["Test case", "Date"]
        csv_header.extend([f"Answer #{id+1}" for id in range(answers_qty)])
        writer.writerow(csv_header)

        for testcase in queryset:
            answers = testcase.answers.all().order_by("question")
            test_results = [str(testcase.id), testcase.created_at.strftime("%d.%m.%y %H:%M")]
            test_results.extend([ans.answer_value for ans in answers])
            writer.writerow(test_results)
        return response

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
    list_filter = ("created_at",)
    date_hierarchy = 'created_at'
    search_fields = ("answer_value", "id")
