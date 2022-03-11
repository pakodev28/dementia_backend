from graphene_file_upload.django import FileUploadGraphQLView

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from config.settings import CURRENTLY_HOST


admin.site.site_header = "Администрирование Деменция.net"
admin.site.site_title = "Администрирование Деменция.net"
admin.site.site_url = CURRENTLY_HOST

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    url(r"^graphql", csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
