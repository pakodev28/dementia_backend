from .testing import APITestCase


class MainMenuElementTestCase(APITestCase):
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
