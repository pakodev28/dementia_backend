import csv

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from demencia_test.models import Answer, DemeniaTestCaseAlt, DementiaTestCase, ResultAnswer


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
        css = {"all": ("css/custom_admin.css",)}

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
    date_hierarchy = "created_at"

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
        for answer in obj.answers.order_by("-question").all():
            try:
                result = ResultAnswer.objects.get(question_id=answer.id).answer_value
            except ObjectDoesNotExist:
                result = "-"
            if answer.question == 26:
                result_list.append(f"Итого: {result} бал.")
            else:
                result_list.append(f"№{answer.question}: {answer.answer_value}: {result}")
        return " | ".join(result_list)


@admin.register(DemeniaTestCaseAlt)
class DementiaTestCaseAltAdmin(DementiaTestCaseAdmin):
    list_display = (
        "id",
        "created_at",
        "answer_1",
        "answer_2",
        "answer_3",
        "answer_4",
        "answer_5",
        "answer_6",
        "answer_7",
        "answer_8",
        "answer_9",
        "answer_10",
        "answer_11",
        "answer_12",
        "answer_13",
        "answer_14",
        "answer_15",
        "answer_16",
        "answer_17",
        "answer_18",
        "answer_19",
        "answer_20",
        "answer_21",
        "answer_22",
        "answer_23",
        "answer_24",
        "answer_25",
        "total_score",
    )

    @staticmethod
    def get_answer(testcase, num):
        answer = testcase.answers.get(question=num)
        try:
            score = ResultAnswer.objects.get(question_id=answer.id).answer_value
        except ObjectDoesNotExist:
            score = "-"
        return f"{answer.answer_value} ({score})"

    @admin.display(description="Ответ №1 (оценка)")
    def answer_1(self, obj):
        return self.get_answer(obj, 1)

    @admin.display(description="Ответ №2 (оценка)")
    def answer_2(self, obj):
        return self.get_answer(obj, 2)

    @admin.display(description="Ответ №3 (оценка)")
    def answer_3(self, obj):
        return self.get_answer(obj, 3)

    @admin.display(description="Ответ №4 (оценка)")
    def answer_4(self, obj):
        return self.get_answer(obj, 4)

    @admin.display(description="Ответ №5 (оценка)")
    def answer_5(self, obj):
        return self.get_answer(obj, 5)

    @admin.display(description="Ответ №6 (оценка)")
    def answer_6(self, obj):
        return self.get_answer(obj, 6)

    @admin.display(description="Ответ №7 (оценка)")
    def answer_7(self, obj):
        return self.get_answer(obj, 7)

    @admin.display(description="Ответ №8 (оценка)")
    def answer_8(self, obj):
        return self.get_answer(obj, 8)

    @admin.display(description="Ответ №9 (оценка)")
    def answer_9(self, obj):
        return self.get_answer(obj, 9)

    @admin.display(description="Ответ №10 (оценка)")
    def answer_10(self, obj):
        return self.get_answer(obj, 10)

    @admin.display(description="Ответ №11 (оценка)")
    def answer_11(self, obj):
        return self.get_answer(obj, 11)

    @admin.display(description="Ответ №12 (оценка)")
    def answer_12(self, obj):
        return self.get_answer(obj, 12)

    @admin.display(description="Ответ №13 (оценка)")
    def answer_13(self, obj):
        return self.get_answer(obj, 13)

    @admin.display(description="Ответ №14 (оценка)")
    def answer_14(self, obj):
        return self.get_answer(obj, 14)

    @admin.display(description="Ответ №15 (оценка)")
    def answer_15(self, obj):
        return self.get_answer(obj, 15)

    @admin.display(description="Ответ №16 (оценка)")
    def answer_16(self, obj):
        return self.get_answer(obj, 16)

    @admin.display(description="Ответ №17 (оценка)")
    def answer_17(self, obj):
        return self.get_answer(obj, 17)

    @admin.display(description="Ответ №18 (оценка)")
    def answer_18(self, obj):
        return self.get_answer(obj, 18)

    @admin.display(description="Ответ №19 (оценка)")
    def answer_19(self, obj):
        return self.get_answer(obj, 19)

    @admin.display(description="Ответ №20 (оценка)")
    def answer_20(self, obj):
        answer = obj.answers.get(question=20)
        try:
            score = ResultAnswer.objects.get(question_id=answer.id).answer_value
            return f"Изображение ({score})"
        except ObjectDoesNotExist:
            return "-"

    @admin.display(description="Ответ №21 (оценка)")
    def answer_21(self, obj):
        answer = obj.answers.get(question=21)
        try:
            score = ResultAnswer.objects.get(question_id=answer.id).answer_value
            return f"Изображение ({score})"
        except ObjectDoesNotExist:
            return "-"

    @admin.display(description="Ответ №22 (оценка)")
    def answer_22(self, obj):
        return self.get_answer(obj, 22)

    @admin.display(description="Ответ №23 (оценка)")
    def answer_23(self, obj):
        return self.get_answer(obj, 23)

    @admin.display(description="Ответ №24 (оценка)")
    def answer_24(self, obj):
        return self.get_answer(obj, 24)

    @admin.display(description="Ответ №25 (оценка)")
    def answer_25(self, obj):
        return self.get_answer(obj, 25)

    @admin.display(description="Итоговая оценка")
    def total_score(self, obj):
        return self.get_answer(obj, 26)


# @admin.register(Answer)
# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ("id", "created_at", "answer_value", "test_case", "question")
#     list_filter = ("created_at",)
#     search_fields = ("answer_value", "id")
