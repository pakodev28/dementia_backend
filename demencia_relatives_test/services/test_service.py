# flake: noqa
import logging
from logging.handlers import RotatingFileHandler

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_list_or_404, get_object_or_404
from django.template.loader import render_to_string

from demencia.models import Settings
from demencia_relatives_test.models import Answer, DementiaTestCase, ResultAnswer

from .answers import RESULTS


logging.basicConfig(
    level=logging.DEBUG, filename="email.log", format="%(asctime)s, %(levelname)s, %(message)s, %(name)s"
)
logger = logging.getLogger("email_logger")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("email.log", maxBytes=50000000, backupCount=1)
logger.addHandler(handler)


class TestService:
    EMAIL_FROM_ANSWER = 5

    def question_6(answer: str, *args) -> int:
        """У близкого Вам человека есть проблемы с памятью?"""
        result = RESULTS[6].get(answer, 0)
        return result

    def question_7(answer: str, *args) -> int:
        """Если это так, стала память хуже, чем несколько лет назад?"""
        result = RESULTS[7].get(answer, 0)
        return result

    def question_8(answer: str, *args) -> int:
        """
        Ваш близкий повторяет один и тот же вопрос или высказывает одну
        и ту же мысль несколько раз в течение дня?
        """
        result = RESULTS[8].get(answer, 0)
        return result

    def question_9(answer: str, *args) -> int:
        """Забывает ли он о назначенных встречах или событиях?"""
        result = RESULTS[9].get(answer, 0)
        return result

    def question_10(answer: str, *args) -> int:
        """Кладет ли он вещи в непривычные места чаще 1 раза в месяц?"""
        result = RESULTS[10].get(answer, 0)
        return result

    def question_11(answer: str, *args) -> int:
        """
        Подозревает ли близких в том, что они прячут или крадут его вещи,
        когда не может найти их?
        """
        result = RESULTS[11].get(answer, 0)
        return result

    def question_12(answer: str, *args) -> int:
        """
        Часто ли он испытывает трудности
        при попытке вспомнить текущий день недели, месяц, год?
        """
        result = RESULTS[12].get(answer, 0)
        return result

    def question_13(answer: str, *args) -> int:
        """Он испытывает проблему с ориентацией в незнакомом месте?"""
        result = RESULTS[13].get(answer, 0)
        return result

    def question_14(answer: str, *args) -> int:
        """Усиливается ли рассеянность за пределами дома, в поездках?"""
        result = RESULTS[14].get(answer, 0)
        return result

    def question_15(answer: str, *args) -> int:
        """Возникают ли проблемы при подсчете сдачи в магазине?"""
        result = RESULTS[15].get(answer, 0)
        return result

    def question_16(answer: str, *args) -> int:
        """Есть ли трудности с оплатой счетов, финансовых операций?"""
        result = RESULTS[16].get(answer, 0)
        return result

    def question_17(answer: str, *args) -> int:
        """
        Забывает ли он принимать лекарства?
        Были случаи, когда он не мог вспомнить, принимал ли он уже лекарство?
        """
        result = RESULTS[17].get(answer, 0)
        return result

    def question_18(answer: str, *args) -> int:
        """Есть ли проблемы с управлением автомобилем?"""
        result = RESULTS[18].get(answer, 0)
        return result

    def question_19(answer: str, *args) -> int:
        """
        Возникают ли трудности при пользовании бытовыми приборами,
        телефоном, телевизионным пультом?
        """
        result = RESULTS[19].get(answer, 0)
        return result

    def question_20(answer: str, *args) -> int:
        """Испытывает ли он затруднения, выполняя работу по дому?"""
        result = RESULTS[20].get(answer, 0)
        return result

    def question_21(answer: str, *args) -> int:
        """Потерял ли он интерес к привычным увлечениям?"""
        result = RESULTS[21].get(answer, 0)
        return result

    def question_22(answer: str, *args) -> int:
        """Может ли Ваш близкий потеряться на знакомой территории
        (например, рядом с собственным домом)?
        """
        result = RESULTS[22].get(answer, 0)
        return result

    def question_23(answer: str, *args) -> int:
        """Утрачивает ли чувство правильного направления движения?"""
        result = RESULTS[23].get(answer, 0)
        return result

    def question_24(answer: str, *args) -> int:
        """
        Случается, ли, что Ваш близкий не только забывает имена,
        но и не может вспомнить нужное слово?
        """
        result = RESULTS[24].get(answer, 0)
        return result

    def question_25(answer: str, *args) -> int:
        """Путает ли Ваш близкий имена родственников или друзей?"""
        result = RESULTS[25].get(answer, 0)
        return result

    def question_26(answer: str, *args) -> int:
        """Есть ли у него проблемы с узнаванием знакомых людей?"""
        result = RESULTS[26].get(answer, 0)
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
