import graphene
from graphene_django.types import DjangoObjectType, ObjectType

from .models import LeftMenuElement, MainMenuElement, MapPoint, NewsArticle, Partner, Slider


class NewsArticleType(DjangoObjectType):
    class Meta:
        model = NewsArticle


class MapPointType(DjangoObjectType):
    class Meta:
        model = MapPoint


class PartnerType(DjangoObjectType):
    class Meta:
        model = Partner


class SliderType(DjangoObjectType):
    class Meta:
        model = Slider


class MainMenuElementType(DjangoObjectType):
    class Meta:
        model = MainMenuElement


class LeftMenuElementType(DjangoObjectType):
    class Meta:
        model = LeftMenuElement


class Query(ObjectType):
    newsarticles = graphene.List(NewsArticleType)
    mappoints = graphene.List(MapPointType)
    partners = graphene.List(PartnerType)
    sliders = graphene.List(SliderType)
    mainmenuelements = graphene.List(MainMenuElementType)
    leftmenuelements = graphene.List(LeftMenuElementType)

    def resolve_newsarticles(self, info, **kwargs):
        return NewsArticle.objects.active()

    def resolve_mappoints(self, info, **kwargs):
        return MapPoint.objects.active()

    def resolve_partners(self, info, **kwargs):
        return Partner.objects.active()

    def resolve_sliders(self, info, **kwargs):
        return Slider.objects.active()

    def resolve_mainmenuelements(self, info, **kwargs):
        return MainMenuElement.objects.active()

    def resolve_leftmenuelements(self, info, **kwargs):
        return LeftMenuElement.objects.active()


schema = graphene.Schema(query=Query)
