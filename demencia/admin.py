from solo.admin import SingletonModelAdmin
from adminsortable2.admin import SortableAdminMixin

from django.contrib import admin
from django.utils.safestring import mark_safe

from demencia.models import LeftMenuElement, MainMenuElement, MapPoint, NewsArticle, Partner, Settings, Slider


@admin.action(description="Сделать активными")
def toggle_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Сделать неактивными")
def toggle_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.register(Settings)
class SettingsAdmin(SingletonModelAdmin):

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
    )


@admin.display(description="Изображение")
def image_preview(obj):
    """Метод для отображения превью изображений"""
    return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px;">')


class NewsArticleAdmin(admin.ModelAdmin):
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
    list_filter = ("title", "is_active")
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


class MapPointAdmin(SortableAdminMixin, admin.ModelAdmin):
    actions = [toggle_active, toggle_inactive]
    list_display = ("city", "is_active", "address", "phone_no")
    list_filter = ("city", "is_active")
    search_fields = ("city", "address", "phone_no")

    fields = ("is_active", "city", "address", "phone_no", ("created_at", "updated_at"), "position")
    readonly_fields = ("created_at", "updated_at", "position")


class PartnerAdmin(SortableAdminMixin, admin.ModelAdmin):
    actions = [toggle_active, toggle_inactive]
    list_display = ("name", "is_active", image_preview, "url", "created_at", "updated_at")
    list_filter = ("name", "is_active")
    search_fields = ("name",)

    fields = ("name", "url", "is_active", "image", image_preview, ("created_at", "updated_at"), "position")
    readonly_fields = ("created_at", "updated_at", image_preview, "position")


class SliderAdmin(SortableAdminMixin, admin.ModelAdmin):
    actions = [toggle_active, toggle_inactive]
    list_display = ("title", "is_active", image_preview, "url", "url_label", "created_at", "updated_at")
    list_filter = ("title", "is_active")
    search_fields = ("title",)

    fields = (
        "title",
        "url_label",
        "url",
        "is_active",
        "image",
        image_preview,
        ("created_at", "updated_at"),
        "position",
    )
    readonly_fields = ("created_at", "updated_at", image_preview, "position")


class MainMenuElementAdmin(SortableAdminMixin, admin.ModelAdmin):
    actions = [toggle_active, toggle_inactive]
    list_display = ("name", "is_active", "url")
    list_filter = ("name", "is_active")
    search_fields = ("name",)

    readonly_fields = ("position",)


class LeftMenuElementAdmin(SortableAdminMixin, admin.ModelAdmin):
    actions = [toggle_active, toggle_inactive]
    list_display = ("name", "is_active", "url")
    list_filter = ("name", "is_active")
    search_fields = ("name",)

    readonly_fields = ("position",)


admin.site.register(NewsArticle, NewsArticleAdmin)
admin.site.register(MapPoint, MapPointAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(LeftMenuElement, LeftMenuElementAdmin)
admin.site.register(MainMenuElement, MainMenuElementAdmin)
