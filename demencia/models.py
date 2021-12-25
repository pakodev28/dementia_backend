from solo.models import SingletonModel
from tinymce.models import HTMLField

from django.db import models

from core.mixins import DateMixin, PublishMixin


class Partner(DateMixin, PublishMixin):
    image = models.ImageField(upload_to='partners/', verbose_name='Изображение')
    name = models.CharField(max_length=250, verbose_name='Название партнёра')
    url = models.URLField(max_length=250, verbose_name='Ссылка')

    class Meta(DateMixin.Meta):
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'

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
