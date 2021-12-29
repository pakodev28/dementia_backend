import graphene
from graphene_file_upload.scalars import Upload

# from .types import NewsArticleType, MapPointType, PartnerType, SliderType, MainMenuElementType, LeftMenuElementType
# from .models import NewsArticle, MapPoint, Partner, Slider, MainMenuElement, LeftMenuElement
from .types import NewsArticleType
from .models import NewsArticle


class NewsArticleInput(graphene.InputObjectType):
    id = graphene.ID()
    is_active = graphene.Boolean()
    image = Upload()
    title = graphene.String()
    text = graphene.String()
    url = graphene.String()
    url_label = graphene.String()


class CreateNewsArticle(graphene.Mutation):
    newsarticle = graphene.Field(NewsArticleType)
    ok = graphene.Boolean()

    class Arguments:
        input = NewsArticleInput(required=True)

    def mutate(root, info, input=None):
        instance = NewsArticle.objects.create(**input)
        instance.save()
        ok = True
        return CreateNewsArticle(newsarticle=instance, ok=ok)


class UpdateNewsArticle(graphene.Mutation):
    newsarticle = graphene.Field(NewsArticleType)
    ok = graphene.Boolean()

    class Arguments:
        input = NewsArticleInput(required=False)

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        instance = NewsArticle.objects.get(pk=input.id)
        if instance:
            ok = True
            instance.is_active = input.is_active
            instance.image = input.image
            instance.title = input.title
            instance.text = input.text
            instance.url = input.url
            instance.url_label = input.url_label
            instance.save()
            return UpdateNewsArticle(ok=ok, newsarticle=instance)
        return UpdateNewsArticle(ok=ok, newsarticle=None)


class Mutation(graphene.ObjectType):
    create_newsarticle = CreateNewsArticle.Field()
    update_newsarticle = UpdateNewsArticle.Field()
