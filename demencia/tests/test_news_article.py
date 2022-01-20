from .testing import APITestCase


class NewsArticleTestCase(APITestCase):
    """Тестирование модели NewArticle"""

    def test_all_fields_news_article(self):
        response = self.query(
            """
            query {
                newsArticles {
                    id
                    title
                    subTitle
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

        expected_fields = [
            "id",
            "title",
            "subTitle",
            "text",
            "image",
            "url",
            "urlLabel",
            "isActive",
            "createdAt",
            "updatedAt",
        ]

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
