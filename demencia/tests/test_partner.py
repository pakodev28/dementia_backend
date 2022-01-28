from .testing import APITestCase


class PartnerTestCase(APITestCase):
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
