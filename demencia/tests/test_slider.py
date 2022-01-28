from .testing import APITestCase


class SliderTestCase(APITestCase):
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
