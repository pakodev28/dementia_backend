import graphene
from graphene_django.types import ObjectType

from .types import NewsArticleType, MapPointType, PartnerType, SliderType, MainMenuElementType, LeftMenuElementType
from .models import NewsArticle, MapPoint, Partner, Slider, MainMenuElement, LeftMenuElement


class Query(ObjectType):
    newsarticle = graphene.Field(NewsArticleType, id=graphene.Int())
    mappoint = graphene.Field(MapPointType, id=graphene.Int())
    partner = graphene.Field(PartnerType, id=graphene.Int())
    slider = graphene.Field(SliderType, id=graphene.Int())
    mainmenuelement = graphene.Field(MainMenuElementType, id=graphene.Int())
    leftmenuelement = graphene.Field(LeftMenuElementType, id=graphene.Int())
    newsarticles = graphene.List(NewsArticleType)
    mappoints = graphene.List(MapPointType)
    partners = graphene.List(PartnerType)
    sliders = graphene.List(SliderType)
    mainmenuelements = graphene.List(MainMenuElementType)
    leftmenuelements = graphene.List(LeftMenuElementType)

    def resolve_newsarticle(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return NewsArticle.objects.get(pk=id)
        return None

    def resolve_mappoint(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return MapPoint.objects.get(pk=id)
        return None

    def resolve_partner(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Partner.objects.get(pk=id)
        return None

    def resolve_slider(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Slider.objects.get(pk=id)
        return None

    def resolve_mainmenuelement(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return MainMenuElement.objects.get(pk=id)
        return None

    def resolve_leftmenuelement(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return LeftMenuElement.objects.get(pk=id)
        return None

    def resolve_newsarticles(self, info, **kwargs):
        return NewsArticle.objects.all()

    def resolve_mappoints(self, info, **kwargs):
        return MapPoint.objects.all()

    def resolve_partners(self, info, **kwargs):
        return Partner.objects.all()

    def resolve_sliders(self, info, **kwargs):
        return Slider.objects.all()

    def resolve_mainmenuelements(self, info, **kwargs):
        return MainMenuElement.objects.all()

    def resolve_leftmenuelements(self, info, **kwargs):
        return LeftMenuElement.objects.all()
