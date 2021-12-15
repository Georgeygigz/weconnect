from django.urls import include, path

# from django.conf.urls import url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_swagger.views import get_swagger_view
from rest_framework import permissions

schema_view_ = get_schema_view(
    openapi.Info(
        title="Weconnect",
        default_version="v1",
        description="Official documentation for the Weconnect",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
swagger_ui_view = get_swagger_view()


urlpatterns = [
    path(
        "docs/",
        schema_view_.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # path('docs(?P<format>\.json|\.yaml)', schema_view_.without_ui(cache_timeout=0), name='schema-json'),
    path("redoc/", schema_view_.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("docs/", swagger_ui_view),
    path(
        "users/",
        include(
            ("app.api.authentication.urls", "authentication"),
            namespace="authentication",
        ),
    ),

    path(
        "posts/",
        include(
            ("app.api.posts.urls", "posts"),
            namespace="posts",
        ),
    ),
]
