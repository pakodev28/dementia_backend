from graphene_django.views import GraphQLView

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from dementia_test.views import create_new_test


admin.site.site_header = "Администрирование Деменция.net"
admin.site.site_title = "Администрирование Деменция.net"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path("new_test/", create_new_test, name="new test"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
