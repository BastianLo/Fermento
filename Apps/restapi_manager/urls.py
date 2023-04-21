from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views.recipe_view import *

schema_view = get_schema_view(
    openapi.Info(
        title="Administration Swagger",
        default_version='v1',
        description="API Documentation for Administration",
        contact=openapi.Contact(url="https://github.com/BastianLo/Fermento"),
        license=openapi.License(name="Apache-2.0 license "),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # recipe views
    path('RecipeManager/recipe/<int:id>', RecipeDetail.as_view()),
    path('RecipeManager/recipe/', RecipeListCreate.as_view()),
]
