import json

from graphene_django.utils.testing import GraphQLTestCase


class APITestCase(GraphQLTestCase):
    fixtures = ["demencia/fixtures/data.json"]

    NUMBER_OF_ACTIVE_ELEMENTS = 3

    def assertResponseHasExpectedFields(self, response, model_query_name, expected):  # noqa: N802
        """
        Метод проверки соответствия полей объекта в ответе API
        """
        content = json.loads(response.content)
        first_element = content.get("data").get(model_query_name)[0]

        for field in expected:
            with self.subTest(field=field):
                self.assertIn(field, first_element.keys())

    def assertShowOnlyActiveElements(self, response, model_query_name):  # noqa: N802
        """
        Метод проверки выдачи активных элементов
        """
        content = json.loads(response.content)
        elements = content.get("data").get(model_query_name)
        self.assertEqual(len(elements), self.NUMBER_OF_ACTIVE_ELEMENTS)
