from django.urls import path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views.recipe_manager_view import *

schema_view = get_schema_view(
    openapi.Info(
        title="Fermento Swagger",
        default_version='v1',
        description="API Documentation for Fermento",
        contact=openapi.Contact(url="https://github.com/BastianLo/Fermento"),
        license=openapi.License(name="Apache-2.0 license "),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path('', RedirectView.as_view(url='swagger/')),
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    ### --- Recipe_manager --- ###
    # Recipe views
    path('RecipeManager/recipe/<int:id>', RecipeDetail.as_view()),
    path('RecipeManager/recipe/', RecipeListCreate.as_view()),
    # Process views
    path('RecipeManager/process/<int:id>', ProcessDetail.as_view()),
    path('RecipeManager/process/', ProcessListCreate.as_view()),
    # Process step view
    path('RecipeManager/processstep/<int:id>', ProcessStepDetail.as_view()),
    path('RecipeManager/processstep/', ProcessStepListCreate.as_view()),
    # Process schedule view
    path('RecipeManager/processschedule/<int:id>', ProcessScheduleDetail.as_view()),
    path('RecipeManager/processschedule/', ProcessScheduleListCreate.as_view()),

]
