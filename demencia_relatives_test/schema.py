from demencia_relatives_test.models import Answer, DementiaTestCase


def test_for_close_person(input):
    answer_value = input.answer_value or Answer._meta.get_field("answer_value").get_default()
    test_case = DementiaTestCase.objects.get(id=input.test_case.id)
    question = input.question

    if question == 1:
        try:
            pass
        except ValueError:
            raise ValueError("Неверное значение")

    instance, _ = Answer.objects.update_or_create(
        test_case=test_case, question=question, defaults={"answer_value": answer_value}
    )
    ok = True
    return instance, ok
