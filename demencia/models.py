from solo.models import SingletonModel
from tinymce.models import HTMLField
from phonenumber_field.modelfields import PhoneNumberField


from django.db import models

from core.mixins import DateMixin, PublishMixin


class NewsArticle(DateMixin, PublishMixin):
    image = models.ImageField(upload_to="news/", verbose_name="Файл изображения")
    title = models.CharField(max_length=250, verbose_name="Заголовок", help_text="Введите заголовок")
    text = models.TextField(verbose_name="Текст новости", help_text="Введите текст")
    url = models.URLField(max_length=250, verbose_name="Ссылка", help_text="Введите адрес ссылки")
    url_label = models.CharField(
        max_length=50, default="ПОДРОБНЕЕ", verbose_name="Название ссылки", help_text="Введите текст ссылки"
    )

    class Meta(DateMixin.Meta):
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title


class MapPoint(DateMixin, PublishMixin):
    city = models.CharField(max_length=250, verbose_name="Город")
    address = models.CharField(max_length=250, verbose_name="Адрес в городе", help_text="Улица, дом, офис")
    phone_no = PhoneNumberField(verbose_name="Номер телефона", help_text="Номер телефона с указанием кода")

    class Meta(DateMixin.Meta):
        verbose_name = "Точка на карте"
        verbose_name_plural = "Точки на карте"

    def __str__(self):
        return f"{self.city} ({self. address})"


class Partner(DateMixin, PublishMixin):
    image = models.ImageField(upload_to="partners/", verbose_name="Файл изображения")
    name = models.CharField(max_length=250, verbose_name="Название партнёра", help_text="Введите название партнёра")
    url = models.URLField(max_length=250, verbose_name="Ссылка", help_text="Введите адрес ссылки")

    class Meta(DateMixin.Meta):
        verbose_name = "Партнёр"
        verbose_name_plural = "Партнёры"

    def __str__(self):
        return self.name


class Slider(DateMixin, PublishMixin):
    title = models.CharField(max_length=250, verbose_name="Заголовок", help_text="Введите заголовок")
    image = models.ImageField(upload_to="slider/", verbose_name="Файл изображения")
    url = models.URLField(max_length=250, verbose_name="Ссылка", help_text="Введите адрес ссылки")
    url_label = models.CharField(
        max_length=50, default="ПОДРОБНЕЕ", verbose_name="Название ссылки", help_text="Введите текст ссылки"
    )

    class Meta(DateMixin.Meta):
        verbose_name = "Слайд"
        verbose_name_plural = "Слайды"

    def __str__(self):
        return self.title


class MainMenuElement(DateMixin, PublishMixin):
    name = models.CharField(max_length=250, verbose_name="Название элемента")
    url = models.URLField(max_length=250, verbose_name="Ссылка")

    class Meta(DateMixin.Meta):
        verbose_name = "Элемент главного меню"
        verbose_name_plural = "Элементы главного меню"

    def __str__(self):
        return self.name


class LeftMenuElement(DateMixin, PublishMixin):
    name = models.CharField(max_length=250, verbose_name="Название элемента")
    url = models.URLField(max_length=250, verbose_name="Ссылка")

    class Meta(DateMixin.Meta):
        verbose_name = "Элемент левого меню"
        verbose_name_plural = "Элементы левого меню"

    def __str__(self):
        return self.name


class Settings(SingletonModel):
    site_name = models.CharField(max_length=255, default="Деменция.net")
    copyright = models.CharField(max_length=255, default="Благотворительный фонд «Память поколений»")
    meta_description = models.TextField()

    main_section_link = models.CharField(max_length=255, default="Пройти тест")
    main_section_additional = models.TextField()

    about_section = models.CharField(max_length=255, default="О деменции")
    about_section_term = HTMLField()
    about_section_term_link = models.CharField(max_length=255, default="Подробнее")
    about_section_action_title = models.CharField(max_length=255, default="Помоги близким")
    about_section_action_subtitle = models.CharField(max_length=255, default="Пройди тест с тем кому нужна помощь")
    about_section_info = HTMLField()
    about_section_link = models.CharField(max_length=255, default="Пройти тест")

    news_section = models.CharField(max_length=255, default="Что нового?")
    news_section_link = models.CharField(max_length=255, default="Перейти к ленте новостей")

    partners_section = models.CharField(max_length=255, default="Кто с нами?")
    partners_section_link = models.CharField(max_length=255, default="Партнеры")

    map_section = models.CharField(max_length=255, default="Куда идти?")
    map_section_link = models.CharField(max_length=255, default="Карта центров профилактики")
    map_section_info = HTMLField()

    fund_section = models.CharField(max_length=255, default="О фонде")
    fund_section_info = HTMLField()
    fund_section_link = models.CharField(max_length=255, default="Перейти на сайт фонда")

    class Meta:
        verbose_name = "Системные настройки"
        verbose_name_plural = "Системные настройки"
