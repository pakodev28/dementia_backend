import json

from graphene_django.utils.testing import GraphQLTestCase


class APITestCase(GraphQLTestCase):
    fixtures = ["demencia/fixtures/data.json"]

    NUMBER_OF_ACTIVE_ELEMENTS = 3

    def assertResponseHasExpectedFields(self, response, model_query_name, expected):
        """
        Метод проверки соответствия полей объекта в ответе API
        """
        content = json.loads(response.content)
        first_element = content.get("data").get(model_query_name)[0]

        for field in expected:
            with self.subTest(field=field):
                self.assertIn(field, first_element.keys())

    def assertShowOnlyActiveElements(self, response, model_query_name):
        """
        Метод проверки выдачи активных элементов
        """
        content = json.loads(response.content)
        elements = content.get("data").get(model_query_name)
        self.assertEqual(len(elements), self.NUMBER_OF_ACTIVE_ELEMENTS)

    """Тестирование модели NewsArticle"""

    def test_all_fields_news_article(self):
        response = self.query(
            """
            query {
                newsArticles {
                    id
                    title
                    text
                    image
                    url
                    urlLabel
                    isActive
                    createdAt
                    updatedAt
                  }
                }
            """
        )

        expected_fields = ["id", "title", "text", "image", "url", "urlLabel", "isActive", "createdAt", "updatedAt"]

        self.assertResponseNoErrors(response)
        self.assertResponseHasExpectedFields(response, "newsArticles", expected_fields)

    def test_one_field_news_article(self):
        response = self.query(
            """
            query {
                newsArticles {
                    title
                }
            }
            """
        )

        expected_fields = [
            "title",
        ]
        self.assertResponseNoErrors(response)
        self.assertResponseHasExpectedFields(response, "newsArticles", expected_fields)

    def test_wrong_field_news_article(self):
        response = self.query(
            """
            query {
                newsArticles {
                    wrong_field
                }
            }
            """
        )

        self.assertResponseHasErrors(response)

    def test_active_news_article(self):
        response = self.query(
            """
            query {
                newsArticles {
                    id
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        self.assertShowOnlyActiveElements(response, "newsArticles")

    """Тестирование модели MapPoint"""

    def test_all_fields_map_point(self):
        response = self.query(
            """
            query {
                mapPoints {
                    id
                    city
                    address
                    phoneNo
                    isActive
                    createdAt
                    updatedAt
                  }
                }
            """
        )

        expected_fields = ["id", "city", "address", "phoneNo", "isActive", "createdAt", "updatedAt"]

        self.assertResponseNoErrors(response)
        self.assertResponseHasExpectedFields(response, "mapPoints", expected_fields)

    def test_one_field_map_point(self):
        response = self.query(
            """
            query {
                mapPoints {
                    city
                }
            }
            """
        )

        expected_fields = [
            "city",
        ]
        self.assertResponseNoErrors(response)
        self.assertResponseHasExpectedFields(response, "mapPoints", expected_fields)

    def test_wrong_field_map_point(self):
        response = self.query(
            """
            query {
                mapPoints {
                    wrong_field
                }
            }
            """
        )

        self.assertResponseHasErrors(response)

    def test_active_map_point(self):
        response = self.query(
            """
            query {
                mapPoints {
                    id
                }
            }
            """
        )

        self.assertResponseNoErrors(response)
        self.assertShowOnlyActiveElements(response, "mapPoints")

    """Тестирование модели Partner"""

    def test_all_fields_partner(self):
        response = self.query(
            """
            query {
                partners {
                    id
                    image
                    name
                    url
                    isActive
                    createdAt
                    updatedAt
                  }
                }
            """
        )

        expected_fields = ["id", "image", "name", "url", "isActive", "createdAt", "updatedAt"]

        self.assertResponseNoErrors(response)
        self.assertResponseHasExpectedFields(response, "partners", expected_fields)

    def test_one_field_partner(self):
        response = self.query(
            """
            query {
                partners {
                    name
                }
            }
            """
        )

        expected_fields = [
            "name",
        ]
        self.assertResponseNoErrors(response)
        self.assertResponseHasExpectedFields(response, "partners", expected_fields)

    def test_wrong_field_partner(self):
        response = self.query(
            """
            query {
                partners {
                    wrong_field
                }
            }
            """
        )

        self.assertResponseHasErrors(response)

    def test_active_partner(self):
        response = self.query(
            """
            query {
                partners {
                    id
                }
            }
            """
        )

        self.assertResponseNoErrors(response)
        self.assertShowOnlyActiveElements(response, "partners")

    """Тестирование модели Slider"""

    def test_all_fields_slider(self):
        response = self.query(
            """
            query {
                sliders {
                    id
                    title
                    image
                    url
                    urlLabel
                    isActive
                    createdAt
                    updatedAt
                  }
                }
            """
        )

        expected_fields = ["id", "title", "image", "url", "urlLabel", "isActive", "createdAt", "updatedAt"]

        self.assertResponseNoErrors(response)
        self.assertResponseHasExpectedFields(response, "sliders", expected_fields)

    def test_one_field_slider(self):
        response = self.query(
            """
            query {
                sliders {
                    title
                }
            }
            """
        )

        expected_fields = [
            "title",
        ]
        self.assertResponseNoErrors(response)
        self.assertResponseHasExpectedFields(response, "sliders", expected_fields)

    def test_wrong_field_slider(self):
        response = self.query(
            """
            query {
                sliders {
                    wrong_field
                }
            }
            """
        )

        self.assertResponseHasErrors(response)

    def test_active_slider(self):
        response = self.query(
            """
            query {
                sliders {
                    id
                }
            }
            """
        )

        self.assertResponseNoErrors(response)
        self.assertShowOnlyActiveElements(response, "sliders")

    """Тестирование модели MainMenuElement"""

    def test_all_fields_main_menu_element(self):
        response = self.query(
            """
            query {
                mainMenuElements {
                    id
                    name
                    url
                    isActive
                    createdAt
                    updatedAt
                  }
                }
            """
        )

        expected_fields = ["id", "name", "url", "isActive", "createdAt", "updatedAt"]

        self.assertResponseNoErrors(response)
        self.assertResponseHasExpectedFields(response, "mainMenuElements", expected_fields)

    def test_one_field_main_menu_element(self):
        response = self.query(
            """
            query {
                mainMenuElements {
                    name
                }
            }
            """
        )

        expected_fields = [
            "name",
        ]
        self.assertResponseNoErrors(response)
        self.assertResponseHasExpectedFields(response, "mainMenuElements", expected_fields)

    def test_wrong_field_main_menu_element(self):
        response = self.query(
            """
            query {
                mainMenuElements {
                    wrong_field
                }
            }
            """
        )

        self.assertResponseHasErrors(response)

    def test_active_main_menu_element(self):
        response = self.query(
            """
            query {
                mainMenuElements {
                    id
                }
            }
            """
        )

        self.assertResponseNoErrors(response)
        self.assertShowOnlyActiveElements(response, "mainMenuElements")

    """Тестирование модели LeftMenuElement"""

    def test_all_fields_left_menu_element(self):
        response = self.query(
            """
            query {
                leftMenuElements {
                    id
                    name
                    url
                    isActive
                    createdAt
                    updatedAt
                  }
                }
            """
        )

        expected_fields = ["id", "name", "url", "isActive", "createdAt", "updatedAt"]

        self.assertResponseNoErrors(response)
        self.assertResponseHasExpectedFields(response, "leftMenuElements", expected_fields)

    def test_one_field_left_menu_element(self):
        response = self.query(
            """
            query {
                leftMenuElements {
                    name
                }
            }
            """
        )

        expected_fields = [
            "name",
        ]
        self.assertResponseNoErrors(response)
        self.assertResponseHasExpectedFields(response, "leftMenuElements", expected_fields)

    def test_wrong_field_left_menu_element(self):
        response = self.query(
            """
            query {
                leftMenuElements {
                    wrong_field
                }
            }
            """
        )

        self.assertResponseHasErrors(response)

    def test_active_left_menu_element(self):
        response = self.query(
            """
            query {
                leftMenuElements {
                    id
                }
            }
            """
        )

        self.assertResponseNoErrors(response)
        self.assertShowOnlyActiveElements(response, "leftMenuElements")
