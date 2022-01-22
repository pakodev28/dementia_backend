from django.conf import settings
import graphene
from graphene_django.types import DjangoObjectType, ObjectType

from .models import LeftMenuElement, MainMenuElement, MapPoint, NewsArticle, Partner, Settings, Slider


class BaseType(ObjectType):
    id = graphene.ID(description="ID объекта", required=True)
    created_at = graphene.DateTime(description="Дата создания", required=True)
    updated_at = graphene.DateTime(description="Дата обновления", required=True)
    is_active = graphene.Boolean(description="Активность", required=True)


class BaseTypeImageField(BaseType):
    image = graphene.String(description="Изображение", required=True)

    def resolve_image(self, info):
        return f"{settings.CURRENTLY_HOST}{self.image.url}"


class NewsArticleType(BaseTypeImageField, DjangoObjectType):
    title = graphene.String(description="Заголовок новости", required=True)
    sub_title = graphene.String(description="Подзаголовок новости", required=True)
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


class PartnerType(BaseTypeImageField, DjangoObjectType):
    name = graphene.String(description="Название партнера", required=True)
    url = graphene.String(description="Ссылка", required=True)

    class Meta:
        model = Partner


class SliderType(BaseTypeImageField, DjangoObjectType):
    title = graphene.String(description="Заголовок", required=True)
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


class SettingsType(DjangoObjectType):
    site_name = graphene.String(description="Название сайта", required=True)
    copyright = graphene.String(description="Авторское право", required=True)
    meta_description = graphene.String(description="Meta описание", required=True)
    main_section_button_label = graphene.String(description="Название кнопки основной секции", required=True)
    about_section = graphene.String(description="Название секции о заболевании", required=True)
    about_section_term = graphene.String(description="Определение термина", required=True)
    about_section_term_open_label = graphene.String(description="Название кнопки для раскрытия термина", required=True)
    about_section_term_close_label = graphene.String(description="Название кнопки для скрытия термина", required=True)
    about_section_action_title = graphene.String(description="Заголовок действия", required=True)
    about_section_action_subtitle = graphene.String(description="Подзаголовок действия", required=True)
    about_section_info = graphene.String(description="Информация о статистике", required=True)
    about_section_button_label = graphene.String(description="Название кнопки для прохождения теста", required=True)
    news_section = graphene.String(description="Название секции новостей", required=True)
    news_section_url_label = graphene.String(description="Название ссылки новостей", required=True)
    partners_section = graphene.String(description="Название секции партнеров", required=True)
    partners_section_subtitle = graphene.String(description="Подзаголовок секции партнеров", required=True)
    map_section = graphene.String(description="Название секции карты", required=True)
    map_section_subtitle = graphene.String(description="Подзаголовок секции карты", required=True)
    map_section_info = graphene.String(description="Предупреждение", required=True)
    fund_section = graphene.String(description="Название секции фонда", required=True)
    fund_section_info = graphene.String(description="Описание фонда", required=True)
    fund_section_url_label = graphene.String(description="Название ссылки фонда", required=True)
    fund_section_url = graphene.String(description="Ссылка на сайт фонда", required=True)

    class Meta:
        model = Settings


class Query(ObjectType):
    news_articles = graphene.List(
        NewsArticleType, description="Активные объекты класса NewsArticle(Новости) (is_active=True)"
    )
    news_article = graphene.Field(
        NewsArticleType, id=graphene.ID(required=True), description="Объект класса NewsArticle(Новости) по id"
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
    settings = graphene.Field(SettingsType, description="Настройки главной страницы")

    def resolve_news_articles(self, info, **kwargs):
        return NewsArticle.objects.active()

    def resolve_news_article(self, info, id):
        return NewsArticle.objects.get(pk=id)

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

    def resolve_settings(self, info, **kwargs):
        return Settings.objects.get()


schema = graphene.Schema(query=Query)
