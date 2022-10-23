import graphene
from graphene_django.types import DjangoObjectType, ObjectType

from django.conf import settings

from demencia_test.models import Answer, DementiaTestCase
from demencia_relatives_test.models import DementiaTestCase as DementiaRelativesTestCase
from demencia_relatives_test.models import Answer as AnswerRelatives
from demencia_test.services.test_service import send_answer
from demencia_relatives_test.services.test_service import send_answer as send_relatives_answer

from .models import LeftMenuElement, MainMenuElement, MapPoint, NewsArticle, Partner, Region, Settings, Slider


class BaseType(ObjectType):
    id = graphene.ID(description="ID объекта", required=True)
    created_at = graphene.DateTime(description="Дата создания", required=True)
    updated_at = graphene.DateTime(description="Дата обновления", required=True)


class BaseTypeImageField(BaseType):
    image = graphene.String(description="Изображение", required=True)

    def resolve_image(self, info):
        return f"{settings.CURRENTLY_HOST}:{settings.CURRENTLY_PORT}{self.image.url}"


class NewsArticleType(BaseTypeImageField, DjangoObjectType):
    title = graphene.String(description="Заголовок новости", required=True)
    sub_title = graphene.String(description="Подзаголовок новости", required=True)
    text = graphene.String(description="Текст новости", required=True)
    url = graphene.String(description="Ссылка", required=True)
    url_label = graphene.String(description="Название ссылки", required=True)

    class Meta:
        model = NewsArticle
        exclude = ("is_active",)


class MapPointType(DjangoObjectType):
    city = graphene.String(description="Город", required=True)
    address = graphene.String(description="Адрес в городе", required=True)
    phone_no = graphene.String(description="Номер телефона", required=True)
    phone_no_secondary = graphene.String(description="Номер телефона (дополнительный)")
    description = graphene.String(description="Описание", required=True)
    opening_hours = graphene.String(description="Время открытия", required=True)

    class Meta:
        model = MapPoint
        fields = ("city", "address", "phone_no", "phone_no_secondary", "description", "opening_hours")
        description = "Объекты класса MapPoint"

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.active()


class RegionType(DjangoObjectType):
    id = graphene.ID(description="ID объекта", required=True)
    geocode = graphene.String(description="Геокод", required=True)

    class Meta:
        model = Region
        fields = ("id", "geocode", "centers")


class PartnerType(BaseTypeImageField, DjangoObjectType):
    name = graphene.String(description="Название партнера", required=True)
    url = graphene.String(description="Ссылка", required=True)

    class Meta:
        model = Partner
        exclude = ("is_active", "position")


class SliderType(BaseTypeImageField, DjangoObjectType):
    title = graphene.String(description="Заголовок", required=True)
    url = graphene.String(description="Ссылка", required=True)
    url_label = graphene.String(description="Название ссылки", required=True)

    class Meta:
        model = Slider
        exclude = ("is_active", "position")


class MainMenuElementType(BaseType, DjangoObjectType):
    name = graphene.String(description="Название элемента", required=True)
    url = graphene.String(description="Ссылка", required=True)

    class Meta:
        model = MainMenuElement
        exclude = ("is_active", "position")


class LeftMenuElementType(BaseType, DjangoObjectType):
    name = graphene.String(description="Название элемента", required=True)
    url = graphene.String(description="Ссылка", required=True)

    class Meta:
        model = LeftMenuElement
        exclude = ("is_active", "position")


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
    news_articles = graphene.List(NewsArticleType, description="Активные объекты класса NewsArticle(Новости)")
    news_article = graphene.Field(
        NewsArticleType, id=graphene.ID(required=True), description="Объект класса NewsArticle(Новости) по id"
    )
    new_test = graphene.ID(
        forClosePerson=graphene.Boolean(), description="Создаёт новый объект класса DementiaTestCase"
    )
    test_result = graphene.String(
        id=graphene.ID(required=True), forClosePerson=graphene.Boolean(), description="Итоговый результат по id теста"
    )
    regions = graphene.List(
        graphene.NonNull(RegionType),
        description="Объекты класса Region с геокодами и связанные с ними объкты класса MapPoint",
        required=True,
    )
    centers = graphene.List(
        graphene.NonNull(MapPointType),
        city=graphene.String(required=True),
        description="""Массив центров профилактики(MapPoint) по значению city""",
        required=True,
    )
    partners = graphene.List(PartnerType, description="Активные объекты класса Partner(Партнер)")
    sliders = graphene.List(SliderType, description="Активные объекты класса Slider(Слайдер)")
    main_menu_elements = graphene.List(
        MainMenuElementType,
        description="Активные объекты класса MainMenuElement(Элемент главного меню)",
    )
    left_menu_elements = graphene.List(
        LeftMenuElementType,
        description="Активные объекты класса LeftMenuElement(Элемент левого меню)",
    )
    settings = graphene.Field(SettingsType, description="Настройки главной страницы")

    def resolve_news_articles(self, info, **kwargs):
        return NewsArticle.objects.active()

    def resolve_news_article(self, info, id):
        return NewsArticle.objects.get(pk=id)

    def resolve_regions(self, info, **kwargs):
        return Region.objects.filter(centers__isnull=False, centers__is_active=True).distinct()

    def resolve_centers(self, info, city, **kwargs):
        return MapPoint.objects.filter(
            is_active=True,
            city__icontains=city,
        )

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

    def resolve_new_test(self, info, forClosePerson):  # noqa: N803
        if forClosePerson:
            return DementiaRelativesTestCase.objects.create().id
        else:
            return DementiaTestCase.objects.create().id

    def resolve_test_result(self, info, id, forClosePerson):  # noqa: N803
        if forClosePerson:
            send_relatives_answer(id)
            return AnswerRelatives.objects.get(test_case=id, question=27).answer_value
        else:
            send_answer(id)
            return Answer.objects.get(test_case=id, question=26).answer_value


schema = graphene.Schema(query=Query)
