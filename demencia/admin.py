from solo.admin import SingletonModelAdmin

from django.contrib import admin

from demencia.models import Partner, Settings


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'image', 'is_active')
    list_filter = ('name', 'is_active')
    search_fields = ('name', )


@admin.register(Settings)
class SettingsAdmin(SingletonModelAdmin):
    pass


admin.site.register(Partner, PartnerAdmin)
