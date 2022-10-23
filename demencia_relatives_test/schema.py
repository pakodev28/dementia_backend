import datetime

from demencia_relatives_test.models import Answer, DementiaTestCase
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def test_for_close_person(input):
    answer_value = input.answer_value or Answer._meta.get_field("answer_value").get_default()
    test_case = DementiaTestCase.objects.get(id=input.test_case.id)
    question = input.question

    if question == 1:
        if not answer_value:
            raise ValidationError("Поле не может быть пустым")

    if question == 2:
        try:
            datetime.datetime.strptime(answer_value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Некорректный формат даты, пример даты: 20-12-2022")

    if question == 5:
        try:
            validate_email(answer_value)
        except ValidationError:
            raise ValueError("Некорректный формат email")

    instance, _ = Answer.objects.update_or_create(
        test_case=test_case, question=question, defaults={"answer_value": answer_value}
    )
    ok = True
    return instance, ok
