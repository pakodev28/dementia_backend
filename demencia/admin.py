from django.contrib import admin

from .models import LeftMenuElement, MainMenuElement, NewsArticle, MapPoint, Partner, Slider


class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "text", "url", "image", "is_active")
    list_filter = ("title", "is_active")
    search_fields = ("title", "text")


class MapPointAdmin(admin.ModelAdmin):
    list_display = ("city", "address", "phone_no")
    list_filter = ("city", "is_active")
    search_fields = ("city", "address", "phone_no")


class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "image", "is_active")
    list_filter = ("name", "is_active")
    search_fields = ("name",)


class SliderAdmin(admin.ModelAdmin):
    list_display = ("title", "image", "url", "is_active")
    list_filter = ("title", "is_active")
    search_fields = ("title",)


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
