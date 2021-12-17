from django.contrib import admin

from .models import LeftMenuElement, MainMenuElement, Partner


class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "image", "is_active")
    list_filter = ("name", "is_active")
    search_fields = ("name",)


@admin.register(MainMenuElement)
class MainMenuElementAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "is_active")
    list_filter = ("name", "is_active")
    search_fields = ("name",)


@admin.register(LeftMenuElement)
class LeftMenuElementAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "is_active")
    list_filter = ("name", "is_active")
    search_fields = ("name",)


admin.site.register(Partner, PartnerAdmin)
