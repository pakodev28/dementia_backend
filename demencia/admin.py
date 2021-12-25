from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import LeftMenuElement, MainMenuElement, MapPoint, NewsArticle, Partner, Slider


@admin.display(description="Изображение")
def preview(obj):
    """Метод для отображения превью изображений"""
    return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px;">')


class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "url_label", "url", "text_area", "is_active", "created_at", "updated_at", preview)
    list_filter = ("title", "is_active")
    search_fields = ("title", "text")

    fields = ("title", "url_label", "url", "text", "is_active", ("created_at", "updated_at"), "image", preview)
    readonly_fields = ("created_at", "updated_at", preview)

    @admin.display(description="Текст новости")
    def text_area(self, obj):
        return mark_safe(f'<div style="overflow: auto; width:400px; height:100px;">{obj.text}</div>')


class MapPointAdmin(admin.ModelAdmin):
    list_display = ("city", "address", "phone_no")
    list_filter = ("city", "is_active")
    search_fields = ("city", "address", "phone_no")


class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "is_active", "created_at", "updated_at", preview)
    list_filter = ("name", "is_active")
    search_fields = ("name",)

    fields = ("name", "url", "is_active", ("created_at", "updated_at"), "image", preview)
    readonly_fields = ("created_at", "updated_at", preview)


class SliderAdmin(admin.ModelAdmin):
    list_display = ("title", "url_label", "url", "is_active", "created_at", "updated_at", preview)
    list_filter = ("title", "is_active")
    search_fields = ("title",)

    fields = ("title", "url_label", "url", "is_active", ("created_at", "updated_at"), "image", preview)
    readonly_fields = ("created_at", "updated_at", preview)


class MainMenuElementAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "is_active")
    list_filter = ("name", "is_active")
    search_fields = ("name",)


class LeftMenuElementAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "is_active")
    list_filter = ("name", "is_active")
    search_fields = ("name",)


admin.site.register(NewsArticle, NewsArticleAdmin)
admin.site.register(MapPoint, MapPointAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(LeftMenuElement, LeftMenuElementAdmin)
admin.site.register(MainMenuElement, MainMenuElementAdmin)
