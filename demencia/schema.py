import graphene
from graphene_django.types import DjangoObjectType, ObjectType

from .models import LeftMenuElement, MainMenuElement, MapPoint, NewsArticle, Partner, Slider


class BaseType(ObjectType):
    id = graphene.ID(description="ID объекта", required=True)
    created_at = graphene.DateTime(description="Дата создания", required=True)
    updated_at = graphene.DateTime(description="Дата обновления", required=True)
    is_active = graphene.Boolean(description="Активность", required=True)


class NewsArticleType(BaseType, DjangoObjectType):
    image = graphene.String(description="Изображение", required=True)
    title = graphene.String(description="Заголовок новости", required=True)
    text = graphene.String(description="Текст новости", required=True)
    url = graphene.String(description="Ссылка", required=True)
    url_label = graphene.String(description="Название ссылки", required=True)

    class Meta:
        model = NewsArticle


class MapPointType(BaseType, DjangoObjectType):
    city = graphene.String(description="Город", required=True)
    address = graphene.String(description="Адрес в городе", required=True)
    phone_no = graphene.String(description="Номер телефона", required=True)

    class Meta:
        model = MapPoint


class PartnerType(BaseType, DjangoObjectType):
    image = graphene.String(description="Изображение", required=True)
    name = graphene.String(description="Название партнера", required=True)
    url = graphene.String(description="Ссылка", required=True)

    class Meta:
        model = Partner


class SliderType(BaseType, DjangoObjectType):
    title = graphene.String(description="Заголовок", required=True)
    image = graphene.String(description="Изображение", required=True)
    url = graphene.String(description="Ссылка", required=True)
    url_label = graphene.String(description="Название ссылки", required=True)

    class Meta:
        model = Slider


class MainMenuElementType(BaseType, DjangoObjectType):
    name = graphene.String(description="Название элемента", required=True)
    url = graphene.String(description="Ссылка", required=True)

    class Meta:
        model = MainMenuElement


class LeftMenuElementType(BaseType, DjangoObjectType):
    name = graphene.String(description="Название элемента", required=True)
    url = graphene.String(description="Ссылка", required=True)

    class Meta:
        model = LeftMenuElement


class Query(ObjectType):
    news_articles = graphene.List(
        NewsArticleType, description="Активные объекты класса NewsArticle(Новости) (is_active=True)"
    )
    map_points = graphene.List(
        MapPointType, description="Активные объекты класса MapPoint(Точка на карте) (is_active=True)"
    )
    partners = graphene.List(PartnerType, description="Активные объекты класса Partner(Партнер) (is_active=True)")
    sliders = graphene.List(SliderType, description="Активные объекты класса Slider(Слайдер) (is_active=True)")
    main_menu_elements = graphene.List(
        MainMenuElementType,
        description="Активные объекты класса MainMenuElement(Элемент главного меню) (is_active=True)",
    )
    left_menu_elements = graphene.List(
        LeftMenuElementType,
        description="Активные объекты класса LeftMenuElement(Элемент левого меню) (is_active=True)",
    )

    def resolve_news_articles(self, info, **kwargs):
        return NewsArticle.objects.active()

    def resolve_map_points(self, info, **kwargs):
        return MapPoint.objects.active()

    def resolve_partners(self, info, **kwargs):
        return Partner.objects.active()

    def resolve_sliders(self, info, **kwargs):
        return Slider.objects.active()

    def resolve_main_menu_elements(self, info, **kwargs):
        return MainMenuElement.objects.active()

    def resolve_left_menu_elements(self, info, **kwargs):
        return LeftMenuElement.objects.active()


schema = graphene.Schema(query=Query)
