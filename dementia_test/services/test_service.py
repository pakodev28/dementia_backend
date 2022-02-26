import datetime
from django.shortcuts import get_object_or_404, get_list_or_404
from dementia_test.models import Answer, DementiaTestCase
from dementia_test.services.image_neural_handler.onnx_inference import get_image_score
from dementia_test.services.countries_list.ru_set import COUNTRIES_NAMES


class TestService:
    CORRECT_ANSWER_15 = ("носорог", "арфа")
    CORRECT_ANSWER_16 = ("цветы", "цветок", "растения", "растение", "природа", "флора")
    CORRECT_ANSWER_17 = ("6", "шесть")
    CORRECT_ANSWER_18 = ("1 рубль 95 копеек", "1,95", "1.95")
    CORRECT_ANSWER_23 = "1А2Б3В4Г5Д6Е"
    CORRECT_ANSWER_24 = ("3,4,5,6,7,8", "1,2,3,4,5,6")
    CORRECT_ANSWER_25 = ("я закончила", "я закончил")

    def question_14(answer: str, *args) -> int:
        """Назовите сегодняшнюю дату, месяц, год."""
        result = 0
        date_obj = datetime.datetime.strptime(answer, "%d-%m-%Y").date()
        today = datetime.date.today()
        three_days = datetime.timedelta(3)
        if date_obj == today:
            result += 2
        elif today - three_days <= date_obj <= today + three_days:
            result += 1
        if date_obj.month == today.month:
            result += 1
        if date_obj.year == today.year:
            result += 1
        return result

    def question_15(answer: str, *args) -> int:
        """Назовите объекты, изображённые на рисунках."""
        result = 0
        treated_answer = [x.lower().strip() for x in answer.split(",")]
        if treated_answer[0] == TestService.CORRECT_ANSWER_15[0]:
            result += 1
        if treated_answer[1] == TestService.CORRECT_ANSWER_15[1]:
            result += 1
        return result

    def question_16(answer: str, *args) -> int:
        """Что общего между розой и тюльпаном?"""
        treated_answer = answer.lower().strip()
        if treated_answer in TestService.CORRECT_ANSWER_16:
            return 2
        else:
            return 0

    def question_17(answer: str, *args) -> int:
        """Сколько полтинников в 3 рублях?"""
        treated_answer = answer.lower().strip()
        if treated_answer in TestService.CORRECT_ANSWER_17:
            return 1
        else:
            return 0

    def question_18(answer: str, *args) -> int:
        """
        Вы оплачиваете в кассу 3 рубля 05 копеек?
        Сколько сдачи вы получите, если дадите кассиру 5 рублей?
        """
        treated_answer = answer.lower().strip()
        if treated_answer in TestService.CORRECT_ANSWER_18:
            return 1
        else:
            return 0

    def question_19(answer: str, *args) -> int:
        return 0

    def question_20(answer: str, *args) -> int:
        """Скопируйте рисунок."""
        return get_image_score("figure", args[0])

    def question_21(answer: str, *args) -> int:
        """Нарисуйте циферблат и разместите на нем цифры."""
        return get_image_score("clock", args[0])

    def question_22(answer: str, *args) -> int:
        """Напишите названия 12 разных стран."""
        countries = {item.lower().strip() for item in answer.split(",")}
        result = len(countries.intersection(COUNTRIES_NAMES))
        if result == 12:
            return 2
        if result in (10, 11):
            return 1
        return 0

    def question_23(answer: str, *args) -> int:
        """Прочертите между кругами линию."""
        mistakes = 0
        zipped_answers = zip(answer, TestService.CORRECT_ANSWER_23)
        for user_answ, expected_answ in zipped_answers:
            if user_answ != expected_answ:
                mistakes += 1
        if not mistakes:  # без ошибок
            return 2
        if mistakes in (1, 2):  # 1-2 ошибки
            return 1
        return 0

    def question_24(answer: str, *args) -> int:
        """На рисунке четыре треугольника. Удалите 2 линии[...]"""
        if answer in TestService.CORRECT_ANSWER_24:
            return 2
        return 0

    def question_25(answer: str, *args) -> int:
        """Вы всё сделали?"""
        treated_answer = answer.lower().strip()
        if treated_answer in TestService.CORRECT_ANSWER_25:
            return 2
        return 0


def get_result(answer_data: list[Answer]) -> int:
    result = 0
    for answer in answer_data:
        f = getattr(TestService, "question_" + str(answer.question))
        try:
            score = f(answer.answer_value, answer.image)
        except Exception:
            score = 0
        result += score
    return result


def send_email(test_id: int, result: int) -> None:
    pass


def save_test_score(test_id: int, result: int) -> None:
    test_case = get_object_or_404(DementiaTestCase, id=test_id)
    Answer.objects.create(
        answer_value=result,
        test_case=test_case,
        question=26,
    )


def send_answer(test_id: int) -> None:
    answer_data = get_list_or_404(Answer, test_case=test_id, question__gte=14, question__lte=25)
    result = get_result(answer_data)
    save_test_score(test_id, result)
    send_email(test_id, result)
