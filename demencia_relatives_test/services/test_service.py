import datetime
import logging
from logging.handlers import RotatingFileHandler

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_list_or_404, get_object_or_404
from django.template.loader import render_to_string

from demencia.models import Settings
from demencia_relatives_test.models import Answer, DementiaTestCase, ResultAnswer

from config.settings import MEDIA_ROOT  # noqa: F401


logging.basicConfig(
    level=logging.DEBUG, filename="email.log", format="%(asctime)s, %(levelname)s, %(message)s, %(name)s"
)
logger = logging.getLogger("email_logger")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("email.log", maxBytes=50000000, backupCount=1)
logger.addHandler(handler)


class TestService:
    CORRECT_ANSWER_15 = ("значение 1", "значение 2")
    EMAIL_FROM_ANSWER = 5

    def question_6(answer: str, *args) -> int:
        """Текст теста"""
        result = 2
        return result


def get_result(answer_data: "list[Answer]") -> int:
    result = 0
    for answer in answer_data:
        try:
            f = getattr(TestService, "question_" + str(answer.question))
            score = f(answer.answer_value)
        except BaseException:
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
        elif result in (2, 3, 4, 22, 23, 24):
            result_name = "БАЛЛА"
        answer_instance = get_object_or_404(Answer, test_case=test_id, question=TestService.EMAIL_FROM_ANSWER)
        user_email = answer_instance.answer_value
        images_path = f"{settings.CURRENTLY_HOST}:{settings.CURRENTLY_PORT}/static/"
        site_path = f"{settings.CURRENTLY_HOST}"
        html_message = render_to_string(
            "email_relatives.html",
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
            logger.exception(f"Ошибка в отправке емейла для родственников: {error}")


def save_test_score(test_id: int, result: int) -> None:
    test_case = get_object_or_404(DementiaTestCase, id=test_id)
    question, _ = Answer.objects.update_or_create(test_case=test_case, question=27, defaults={"answer_value": result})

    ResultAnswer.objects.update_or_create(question_id=question, defaults={"answer_value": result})


def send_answer(test_id: int) -> None:
    answer_data = get_list_or_404(Answer, test_case=test_id, question__gte=6, question__lte=26)
    result = get_result(answer_data)
    save_test_score(test_id, result)
    send_email(test_id, result)
