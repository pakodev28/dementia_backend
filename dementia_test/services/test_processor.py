import datetime

from dementia_test.models import Answer, DementiaTestCase
from dementia_test.services.image_neural_handler.onnx_inference import get_image_score


class _TestProcessor:

    def question_14(answer: str, *args) -> int:
        result = 0
        date_obj = datetime.datetime.strptime(answer, '%d-%m-%Y').date()
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
        result = 0
        treated_answer = [x.lower().strip() for x in answer.split(',')]
        if treated_answer[0] == 'носорог':
            result += 1
        if treated_answer[1] == 'арфа':
            result += 1
        return result

    def question_16(answer: str, *args) -> int:
        correct_answers = ['цветы', 'цветок', 'растения', 'растение', 'природа', 'флора']
        treated_answer = answer.lower().strip()
        if treated_answer in correct_answers:
            return 2
        else:
            return 0

    def question_17(answer: str, *args) -> int:
        correct_answers = ['6', 'шесть']
        treated_answer = answer.lower().strip()
        if treated_answer in correct_answers:
            return 1
        else:
            return 0

    def question_18(answer: str, *args) -> int:
        correct_answers = ['1 рубль 95 копеек', '1,95', '1.95']
        treated_answer = answer.lower().strip()
        if treated_answer in correct_answers:
            return 1
        else:
            return 0

    def question_19(answer: str, *args) -> int:
        return 0

    def question_20(answer: str, *args) -> int:
        return get_image_score('figure', args[0])

    def question_21(answer: str, *args) -> int:
        return get_image_score('clock', args[0])

    def question_22(answer: str, *args) -> int:
        return 0

    def question_23(answer: str, *args) -> int:
        return 0

    def question_24(answer: str, *args) -> int:
        return 0

    def question_25(answer: str, *args) -> int:
        return 0


def _get_result(answer_data: list[Answer]) -> int:
    result = 0
    for answer in answer_data:
        f = getattr(_TestProcessor, "question_" + str(answer.question))
        try:
            score = f(answer.answer_value, answer.image)
        except Exception:
            score = 0
        result += score
    return result


def _send_email(test_id: int, result: int) -> None:
    pass


def _save_test_score(test_id: int, result: int) -> None:
    test_case = DementiaTestCase.objects.get(id=test_id)
    Answer.objects.create(
        answer_value=result, test_case=test_case, question=26,
    )


def send_answer(test_id: int) -> None:
    answer_data = Answer.objects.get(test_case=test_id).filter(question__gte=14, question__lte=25)
    result = _get_result(answer_data)
    _save_test_score(test_id, result)
    _send_email(test_id, result)
