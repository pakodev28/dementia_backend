from django.contrib import admin

from .models import Partner


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'image', 'is_active')
    list_filter = ('name', 'is_active')
    search_fields = ('name', )


admin.site.register(Partner, PartnerAdmin)
