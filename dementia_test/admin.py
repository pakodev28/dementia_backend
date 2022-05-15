import csv

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from dementia_test.models import Answer, DementiaTestCase, ResultAnswer


@admin.display(description="Номер вопроса")
def question_number(obj):
    """Метод для отображения номера вопроса"""
    if obj.question == 26:
        result = "Итого: "
    else:
        result = obj.question
    return result  # noqa


@admin.display(description="Значение ответа")
def question_value(obj):
    """Метод для отображения значения ответа"""
    if obj.question == 26:
        result = ""
    else:
        result = obj.answer_value
    return result  # noqa


@admin.display(description="Баллы")
def result_value(obj):
    """Метод для отображения результата вопроса в баллах"""
    try:
        result = ResultAnswer.objects.get(question_id=obj.id).answer_value
    except ObjectDoesNotExist:
        result = "-"
    if obj.question == 26:
        result = f"{result}"
    return result  # noqa


@admin.display(description="Изображение")
def image_preview(obj):
    """Метод для отображения превью изображений"""
    return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px;">')


class AnswersInline(admin.TabularInline):
    model = Answer

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False

    fields = (
        question_number,
        question_value,
        result_value,
        image_preview,
    )
    readonly_fields = (
        question_number,
        question_value,
        result_value,
        image_preview,
    )
    ordering = ("question",)


@admin.register(DementiaTestCase)
class DementiaTestCaseAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/custom_admin.css',)
        }
    list_per_page = 20
    actions = ["download_csv"]
    list_display = ("id", "created_at", "answers")
    readonly_fields = (
        "id",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("id", "answers__answer_value")
    inlines = [
        AnswersInline,
    ]
    date_hierarchy = 'created_at'

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
        result_list = []
        for answer in obj.answers.order_by('-question').all():
            try:
                result = ResultAnswer.objects.get(question_id=answer.id).answer_value
            except ObjectDoesNotExist:
                result = "-"
            if answer.question == 26:
                result_list.append(f"Итого: {result} бал.")
            else:
                result_list.append(f"№{answer.question}: {answer.answer_value}: {result}")
        return " | ".join(result_list)


# @admin.register(Answer)
# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ("id", "created_at", "answer_value", "test_case", "question")
#     list_filter = ("created_at",)
#     search_fields = ("answer_value", "id")
