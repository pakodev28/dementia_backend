import re
from html import unescape

from adminsortable2.admin import SortableAdminMixin
from solo.admin import SingletonModelAdmin

from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

from demencia.models import LeftMenuElement, MainMenuElement, MapPoint, NewsArticle, Partner, Settings, Slider


@admin.action(description="Сделать активными")
def toggle_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Сделать неактивными")
def toggle_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


def validate_htmlfield(text):
    """Очищает текст в htmlfield от html-тегов для проверки, что в тексте не только пробелы.
    Если проходит валидацию, возвращает исходный текст."""
    if text is not None:
        cleaned_text = strip_tags(unescape(text))
        if cleaned_text.isspace():
            raise forms.ValidationError("Текст не может состоять только из пробелов.")
    return text


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = "__all__"

    def clean_about_section_term(self):
        """Очищает <определение термина> от html-тегов для проверки, что в тексте не только пробелы.
        Если проходит валидацию, возвращает исходный текст."""
        about_section_term = self.cleaned_data.get("about_section_term")
        validate_htmlfield(about_section_term)
        return about_section_term

    def clean_about_section_info(self):
        """Очищает <информация о статистике> от html-тегов для проверки, что в тексте не только пробелы.
        Если проходит валидацию, возвращает исходный текст."""
        about_section_info = self.cleaned_data.get("about_section_info")
        validate_htmlfield(about_section_info)
        return about_section_info

    def clean_fund_section_info(self):
        """Очищает <описание> от html-тегов для проверки, что в тексте не только пробелы.
        Если проходит валидацию, возвращает исходный текст."""
        fund_section_info = self.cleaned_data.get("fund_section_info")
        validate_htmlfield(fund_section_info)
        return fund_section_info


@admin.register(Settings)
class SettingsAdmin(SingletonModelAdmin):

    form = SettingsForm
    fieldsets = (
        (
            "Общая информация",
            {
                "fields": (
                    "site_name",
                    "copyright",
                    "meta_description",
                )
            },
        ),
        (
            "Основная секция",
            {"fields": ("main_section_button_label",)},
        ),
        (
            "О деменции",
            {
                "fields": (
                    "about_section",
                    "about_section_term",
                    "about_section_term_open_label",
                    "about_section_term_close_label",
                    "about_section_action_title",
                    "about_section_action_subtitle",
                    "about_section_info",
                    "about_section_button_label",
                )
            },
        ),
        (
            "Новости",
            {
                "fields": (
                    "news_section",
                    "news_section_url_label",
                )
            },
        ),
        (
            "Партнеры",
            {
                "fields": (
                    "partners_section",
                    "partners_section_subtitle",
                )
            },
        ),
        (
            "Карта",
            {
                "fields": (
                    "map_section",
                    "map_section_subtitle",
                    "map_section_info",
                )
            },
        ),
        (
            "О фонде",
            {
                "fields": (
                    "fund_section",
                    "fund_section_info",
                    "fund_section_url_label",
                    "fund_section_url",
                )
            },
        ),
        ("Отправлять письма", {"fields": ("enable_send_email",)}),
    )


@admin.display(description="Изображение")
def image_preview(obj):
    """Метод для отображения превью изображений"""
    return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px;">')


class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = "__all__"

    def clean_text(self):
        """Очищает <текст новости> от html-тегов для проверки, что в тексте не только пробелы.
        Если проходит валидацию, возвращает исходный текст."""
        text = self.cleaned_data.get("text")
        validate_htmlfield(text)
        return text

    def clean_image(self):
        """Проверяет размер загружаемого изображения, что он не превышает 2MB"""
        image = self.cleaned_data.get("image")
        image_size = image.size

        if image_size > settings.MAX_SIZE:
            raise forms.ValidationError("Максимальный размер загружаемой картинки не должен превышать 2MB.")
        return image


class NewsArticleAdmin(admin.ModelAdmin):
    form = NewsArticleForm
    actions = [toggle_active, toggle_inactive]
    list_display = (
        "title",
        "is_active",
        "sub_title",
        "text_area",
        image_preview,
        "url",
        "url_label",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_active",)
    search_fields = ("title", "text")

    fields = (
        "is_active",
        "title",
        "sub_title",
        "url_label",
        "url",
        "text",
        "image",
        image_preview,
        ("created_at", "updated_at"),
    )
    readonly_fields = ("created_at", "updated_at", image_preview)

    @admin.display(description="Текст новости")
    def text_area(self, obj):
        return mark_safe(f'<div style="overflow: auto; width:400px; height:100px;">{obj.text}</div>')


class MapPointForm(forms.ModelForm):
    class Meta:
        model = MapPoint
        fields = "__all__"

    def clean_city(self):
        """Проверяет отсутвие в поле город специальных символов и цифр"""
        city = self.cleaned_data.get("city")
        if re.search(r"[A-Za-z0-9@_!#$%^&*()<>?/\\|}{~:\[\]\.,]", city):
            raise forms.ValidationError(
                "Название города не может содержать цифры, специальные символы и символы других языков"
            )
        return city

    def clean_address(self):
        """Проверяет отсутсвие в адресе специальных символов"""
        address = self.cleaned_data.get("address")
        if re.search(r"[A-Za-z@_!#$%^&*()<>?/\\|}{~:\[\]]", address):
            raise forms.ValidationError("Адрес не может содержать специальные символы и символы других языков ")
        return address


class MapPointAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = MapPointForm
    actions = [toggle_active, toggle_inactive]
    list_display = (
        "city",
        "region",
        "is_active",
        "address",
        "phone_no",
        "phone_no_secondary",
        "description",
        "opening_hours",
    )
    list_filter = ("city", "is_active")
    search_fields = ("city", "address", "phone_no", "phone_no_secondary")

    fields = (
        "is_active",
        "city",
        "region",
        "address",
        ("phone_no", "phone_no_secondary"),
        "description",
        "opening_hours",
        ("created_at", "updated_at"),
    )
    readonly_fields = ("created_at", "updated_at")


class PartnerAdmin(SortableAdminMixin, admin.ModelAdmin):
    actions = [toggle_active, toggle_inactive]
    list_display = ("name", "is_active", image_preview, "url", "created_at", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name",)

    fields = ("name", "url", "is_active", "image", image_preview, ("created_at", "updated_at"))
    readonly_fields = ("created_at", "updated_at", image_preview)


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = "__all__"

    def clean_title(self):
        """Очищает <заголовок> от html-тегов для проверки, что в тексте не только пробелы.
        Если проходит валидацию, возвращает исходный текст."""
        title = self.cleaned_data.get("title")
        validate_htmlfield(title)
        return title


class SliderAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = SliderForm
    actions = [toggle_active, toggle_inactive]
    list_display = ("title", "is_active", image_preview, "url", "url_label", "created_at", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title",)

    fields = ("title", "url_label", "url", "is_active", "image", image_preview, ("created_at", "updated_at"))
    readonly_fields = ("created_at", "updated_at", image_preview)


class MainMenuElementAdmin(SortableAdminMixin, admin.ModelAdmin):
    actions = [toggle_active, toggle_inactive]
    list_display = ("name", "is_active", "url")
    list_filter = ("is_active",)
    search_fields = ("name",)


class LeftMenuElementAdmin(SortableAdminMixin, admin.ModelAdmin):
    actions = [toggle_active, toggle_inactive]
    list_display = ("name", "is_active", "url")
    list_filter = ("is_active",)
    search_fields = ("name",)


admin.site.register(NewsArticle, NewsArticleAdmin)
admin.site.register(MapPoint, MapPointAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(LeftMenuElement, LeftMenuElementAdmin)
admin.site.register(MainMenuElement, MainMenuElementAdmin)
