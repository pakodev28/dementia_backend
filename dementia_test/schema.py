import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload

from django.core.exceptions import ValidationError

from .models import Answer, DementiaTestCase

import datetime

now = datetime.datetime.now()


class DementiaTestCaseType(DjangoObjectType):
    id = graphene.ID(description="ID теста")

    class Meta:
        model = DementiaTestCase
        fields = ("id",)


class AnswerType(DjangoObjectType):
    id = graphene.ID(description="ID ответа")
    answer_value = graphene.String(description="Значение ответа")
    question = graphene.Int(description="Номер вопроса")
    image = graphene.String(description="Изображение")
    test_case = graphene.Field(DementiaTestCaseType, description="Экземпляр теста")

    class Meta:
        model = Answer
        fields = ("id", "answer_value", "test_case", "question", "image")


class DementiaTestCaseInput(graphene.InputObjectType):
    id = graphene.ID(description="ID теста", required=True)


class AnswerInput(graphene.InputObjectType):
    image = Upload(description="Изображение")
    answer_value = graphene.String(description="Значение ответа")
    test_case = graphene.InputField(DementiaTestCaseInput, description="Экземпляр теста", required=True)
    question = graphene.Int(description="Номер вопроса", required=True)


class CreateAnswer(graphene.Mutation):
    answer = graphene.Field(AnswerType)
    ok = graphene.Boolean()

    class Arguments:
        input = AnswerInput(required=True)

    def mutate(self, info, input=None):
        answer_value = input.answer_value or Answer._meta.get_field('answer_value').get_default()
        test_case = DementiaTestCase.objects.get(id=input.test_case.id)
        question = input.question
        image = input.image or Answer._meta.get_field('image').get_default()

        if question < 1 or question > 25:
            raise ValidationError("Номер вопроса не может быть меньше 1 и больше 25.")

        if not(question in [20, 21]) and image:
            raise ValidationError(f"Вопрос {question} должен содержать только ответ и не может включать изображение")

        if question in [20, 21] and answer_value:
            raise ValidationError(f"Вопрос {question} должен содержать только изображение и не может включать ответ")

        if question in [20, 21] and not(image):
            raise ValidationError(f"Вопрос {question} должен содержать изображение")

        instance, _ = Answer.objects.update_or_create(
            test_case=test_case,
            question=question,
            defaults={'answer_value': answer_value, "image": image}
        )

        ok = True
        return CreateAnswer(answer=instance, ok=ok)


class Mutation(graphene.ObjectType):
    create_answer = CreateAnswer.Field()


schema = graphene.Schema(mutation=Mutation)
