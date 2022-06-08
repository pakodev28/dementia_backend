import datetime
import logging
from logging.handlers import RotatingFileHandler

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_list_or_404, get_object_or_404
from django.template.loader import render_to_string

from demencia.models import Settings
from demencia_test.models import Answer, DementiaTestCase, ResultAnswer
from demencia_test.services.countries_list.ru_set import COUNTRIES_NAMES
from demencia_test.services.image_neural_handler.onnx_inference import get_image_score

from config.settings import MEDIA_ROOT  # noqa: F401


logging.basicConfig(
    level=logging.DEBUG, filename="email.log", format="%(asctime)s, %(levelname)s, %(message)s, %(name)s"
)
logger = logging.getLogger("email_logger")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("email.log", maxBytes=50000000, backupCount=1)
logger.addHandler(handler)


class TestService:
    CORRECT_ANSWER_15 = ("носорог", "арфа")
    CORRECT_ANSWER_16 = ("цветы", "цветок", "растения", "растение", "природа", "флора")
    CORRECT_ANSWER_17 = ("6", "шесть")
    CORRECT_ANSWER_18 = ("1 рубль 95 копеек", "1,95", "1.95", "01,95", "01.95", "01 рубль 95 копеек")
    CORRECT_ANSWER_23 = "1А2Б3В4Г5Д6Е"
    CORRECT_ANSWER_24 = ("3,4,5,6,7,8,9", "1,2,3,4,5,6,7")
    CORRECT_ANSWER_25 = ("я закончила", "я закончил")
    EMAIL_FROM_ANSWER = 4

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
        result = set()
        answer = answer.replace(" ", "")
        answer = answer.replace("-", "")
        countries = {item.lower() for item in answer.split(",")}
        for country in countries:
            tmp = COUNTRIES_NAMES.get(country, "False")
            if tmp != "False":
                if tmp == "":
                    result.add(country)
                else:
                    result.add(tmp)
        result = len(result)
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


def get_result(answer_data: "list[Answer]") -> int:
    result = 0
    for answer in answer_data:
        f = getattr(TestService, "question_" + str(answer.question))
        try:
            score = f(answer.answer_value, answer.image)
        except Exception:
            score = 0
        question_id = Answer.objects.get(test_case=answer.test_case, question=answer.question)
        ResultAnswer.objects.update_or_create(question_id=question_id, defaults={"answer_value": score})
        result += score
    return result


def send_email(test_id: int, result: int) -> None:
    if Settings.objects.get().enable_send_email:
        result_name = "БАЛЛОВ"
        if result in (1, 21):
            result_name = "БАЛЛ"
        elif result in (2, 3, 4, 22):
            result_name = "БАЛЛА"
        answer_instance = get_object_or_404(Answer, test_case=test_id, question=TestService.EMAIL_FROM_ANSWER)
        user_email = answer_instance.answer_value
        images_path = f"{settings.CURRENTLY_HOST}:{settings.CURRENTLY_PORT}/static/"
        site_path = f"{settings.CURRENTLY_HOST}"
        html_message = render_to_string(
            "email.html",
            {"result": result, "result_name": result_name, "images_path": images_path, "site_path": site_path},
        )
        try:
            send_mail(
                settings.EMAIL_NAME,
                None,
                settings.DEFAULT_FROM_EMAIL,
                [user_email],
                fail_silently=False,
                html_message=html_message,
            )
        except Exception as error:
            logger.exception(f"Ошибка в отправке емейла: {error}")


def save_test_score(test_id: int, result: int) -> None:
    test_case = get_object_or_404(DementiaTestCase, id=test_id)
    question, _ = Answer.objects.update_or_create(test_case=test_case, question=26, defaults={"answer_value": result})

    ResultAnswer.objects.update_or_create(question_id=question, defaults={"answer_value": result})


def send_answer(test_id: int) -> None:
    answer_data = get_list_or_404(Answer, test_case=test_id, question__gte=14, question__lte=25)
    result = get_result(answer_data)
    save_test_score(test_id, result)
    send_email(test_id, result)
