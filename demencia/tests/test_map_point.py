from .testing import APITestCase


class MapPointTestCase(APITestCase):
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
