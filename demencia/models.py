from phonenumber_field.modelfields import PhoneNumberField
from solo.models import SingletonModel
from tinymce.models import HTMLField
from url_or_relative_url_field.fields import URLOrRelativeURLField

from django.db import models

from core.mixins import DateMixin, PublishMixin, OrderingMixin


class NewsArticle(DateMixin, PublishMixin):
    image = models.ImageField(upload_to="news/", verbose_name="Файл изображения")
    title = models.CharField(max_length=250, verbose_name="Заголовок", help_text="Введите заголовок")
    sub_title = models.CharField(max_length=250, verbose_name="Подзаголовок", help_text="Введите подзаголовок")
    text = HTMLField(verbose_name="Текст новости", help_text="Введите текст")
    url = URLOrRelativeURLField(max_length=250, verbose_name="Ссылка", help_text="Введите адрес ссылки")
    url_label = models.CharField(
        max_length=50, default="ПОДРОБНЕЕ", verbose_name="Название ссылки", help_text="Введите текст ссылки"
    )

    class Meta(DateMixin.Meta):
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title


class MapPoint(DateMixin, PublishMixin, OrderingMixin):
    city = models.CharField(max_length=250, verbose_name="Город")
    address = models.CharField(max_length=250, verbose_name="Адрес в городе", help_text="Улица, дом, офис")
    phone_no = PhoneNumberField(verbose_name="Номер телефона", help_text="Номер телефона с указанием кода")

    class Meta(OrderingMixin.Meta):
        verbose_name = "Точка на карте"
        verbose_name_plural = "Точки на карте"

    def __str__(self):
        return f"{self.city} ({self. address})"


class Partner(DateMixin, PublishMixin, OrderingMixin):
    image = models.ImageField(upload_to="partners/", verbose_name="Файл изображения")
    name = models.CharField(max_length=250, verbose_name="Название партнёра", help_text="Введите название партнёра")
    url = models.URLField(max_length=250, verbose_name="Ссылка", help_text="Введите адрес ссылки")

    class Meta(OrderingMixin.Meta):
        verbose_name = "Партнёр"
        verbose_name_plural = "Партнёры"

    def __str__(self):
        return self.name


class Slider(DateMixin, PublishMixin, OrderingMixin):
    title = HTMLField(max_length=250, verbose_name="Заголовок", help_text="Введите заголовок")
    image = models.ImageField(upload_to="slider/", verbose_name="Файл изображения")
    url = URLOrRelativeURLField(max_length=250, verbose_name="Ссылка", help_text="Введите адрес ссылки")
    url_label = models.CharField(
        max_length=50, default="ПОДРОБНЕЕ", verbose_name="Название ссылки", help_text="Введите текст ссылки"
    )

    class Meta(OrderingMixin.Meta):
        verbose_name = "Слайд"
        verbose_name_plural = "Слайды"

    def __str__(self):
        return self.title


class MainMenuElement(DateMixin, PublishMixin, OrderingMixin):
    name = models.CharField(max_length=250, verbose_name="Название элемента")
    url = URLOrRelativeURLField(max_length=250, verbose_name="Ссылка")

    class Meta(OrderingMixin.Meta):
        verbose_name = "Элемент главного меню"
        verbose_name_plural = "Элементы главного меню"

    def __str__(self):
        return self.name


class LeftMenuElement(DateMixin, PublishMixin, OrderingMixin):
    name = models.CharField(max_length=250, verbose_name="Название элемента")
    url = URLOrRelativeURLField(max_length=250, verbose_name="Ссылка")

    class Meta(OrderingMixin.Meta):
        verbose_name = "Элемент левого меню"
        verbose_name_plural = "Элементы левого меню"

    def __str__(self):
        return self.name


class Settings(SingletonModel):
    site_name = models.CharField("Название сайта", max_length=255, default="Деменция.net")
    copyright = models.CharField(
        "Авторское право", max_length=255, default="Благотворительный фонд «Память поколений»"
    )
    meta_description = models.TextField("Meta описание")

    main_section_button_label = models.CharField("Название кнопки", max_length=255, default="Пройти тест")

    about_section = models.CharField("Название секции", max_length=255, default="О деменции")
    about_section_term = HTMLField("Определение термина")
    about_section_term_open_label = models.CharField(
        verbose_name="Название кнопки для раскрытия термина", max_length=255, default="Подробнее"
    )
    about_section_term_close_label = models.CharField(
        verbose_name="Название кнопки для скрытия термина", max_length=255, default="Скрыть"
    )
    about_section_action_title = models.CharField(
        verbose_name="Заголовок действия", max_length=255, default="Помоги близким"
    )
    about_section_action_subtitle = models.CharField(
        verbose_name="Подзаголовок действия", max_length=255, default="Пройди тест с тем кому нужна помощь"
    )
    about_section_info = HTMLField("Информация о статистике")
    about_section_button_label = models.CharField(
        verbose_name="Название кнопки для прохождения теста", max_length=255, default="Пройти тест"
    )

    news_section = models.CharField("Название секции", max_length=255, default="Что нового?")
    news_section_url_label = models.CharField(
        verbose_name="Название ссылки", max_length=255, default="Перейти к ленте новостей"
    )

    partners_section = models.CharField("Название секции", max_length=255, default="Кто с нами?")
    partners_section_subtitle = models.CharField("Подзаголовок секции", max_length=255, default="Партнеры")

    map_section = models.CharField("Название секции", max_length=255, default="Куда идти?")
    map_section_subtitle = models.CharField(
        verbose_name="Подзаголовок секции", max_length=255, default="Карта центров профилактики"
    )
    map_section_info = models.TextField("Предупреждение")

    fund_section = models.CharField("Название секции", max_length=255, default="О фонде")
    fund_section_info = HTMLField("Описание")
    fund_section_url_label = models.CharField(
        verbose_name="Название ссылки", max_length=255, default="Перейти на сайт фонда"
    )
    fund_section_url = models.URLField(
        verbose_name="Ссылка на сайт фонда", max_length=255, default="https://pamyatpokoleniy.ru/"
    )

    class Meta:
        verbose_name = "Настройки главной страницы"
        verbose_name_plural = "Настройки главной страницы"

    def __str__(self):
        return "Настройки"
