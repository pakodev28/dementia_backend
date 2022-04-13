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
        answer_value = input.answer_value
        test_case = DementiaTestCase.objects.get(id=input.test_case.id)
        question = input.question
        image_list = input.image.split('.')
        image = f"{''.join(image_list[0:-1])}_{now.strftime('%d-%m-%Y_%H-%M-%S')}.{image_list[-1]}"
        if question < 1 or question > 25:
            raise ValidationError("Номер вопроса не может быть меньше 1 и больше 25.")
        instance = Answer.objects.create(
            answer_value=answer_value, test_case=test_case, question=question, image=image
        )
        instance.save()
        ok = True
        return CreateAnswer(answer=instance, ok=ok)


class Mutation(graphene.ObjectType):
    create_answer = CreateAnswer.Field()


schema = graphene.Schema(mutation=Mutation)
