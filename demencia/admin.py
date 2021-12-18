from django.contrib import admin

from .models import Partner, Slider


class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "image", "is_active")
    list_filter = ("name", "is_active")
    search_fields = ("name",)


class SliderAdmin(admin.ModelAdmin):
    list_display = ("title", "text", "image", "url", "is_active")
    list_filter = ("title", "is_active")
    search_fields = ("title", "text")


admin.site.register(Partner, PartnerAdmin)
admin.site.register(Slider, SliderAdmin)
