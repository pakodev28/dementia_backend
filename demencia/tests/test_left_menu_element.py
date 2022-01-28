from .testing import APITestCase


class LeftMenuTestCase(APITestCase):
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
