from graphene_django.types import DjangoObjectType

from .models import NewsArticle, MapPoint, Partner, Slider, MainMenuElement, LeftMenuElement


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
