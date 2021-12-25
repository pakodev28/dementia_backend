from django.db import models

from core.mixins import DateMixin, PublishMixin


class NewsArticle(DateMixin, PublishMixin):
    image = models.ImageField(upload_to="news/", verbose_name="Изображение")
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст новости")
    url = models.URLField(max_length=250, null=True, verbose_name="Ссылка")
    url_label = models.CharField(max_length=50, default="ПОДРОБНЕЕ", verbose_name="Название ссылки")

    class Meta(DateMixin.Meta):
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title


class MapPoint(DateMixin, PublishMixin):
    city = models.CharField(max_length=250, verbose_name="Город")
    address = models.CharField(max_length=250, verbose_name="Адрес в городе")
    phone_no = models.CharField(max_length=250, verbose_name="Номер телефона")

    class Meta(DateMixin.Meta):
        verbose_name = "Точка на карте"
        verbose_name_plural = "Точки на карте"

    def __str__(self):
        return f"{self.city} ({self. address})"


class Partner(DateMixin, PublishMixin):
    image = models.ImageField(upload_to="partners/", verbose_name="Изображение")
    name = models.CharField(max_length=250, verbose_name="Название партнёра")
    url = models.URLField(max_length=250, verbose_name="Ссылка")

    class Meta(DateMixin.Meta):
        verbose_name = "Партнёр"
        verbose_name_plural = "Партнёры"

    def __str__(self):
        return self.name


class Slider(DateMixin, PublishMixin):
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    image = models.ImageField(upload_to="slider/", verbose_name="Изображение")
    url = models.URLField(max_length=250, verbose_name="Ссылка")
    url_label = models.CharField(max_length=50, default="ПОДРОБНЕЕ", verbose_name="Название ссылки")

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
