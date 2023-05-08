from django.urls import path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views.authentification_view import api_login, ObtainTokenPairView
from .views.batch_view import BatchDetail, BatchListCreate, QrCodeDetail, QrCodeListCreate, ExecutionListCreate, \
    ExecutionDetail, JournalEntryListCreate, JournalEntryDetail
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

    ### --- API Authentification --- ###
    path('auth/login/', api_login, name='api_login'),
    path('auth/token/', ObtainTokenPairView.as_view(), name='token_obtain_pair'),

    ### --- Recipe_manager --- ###
    # Recipe views
    path('recipe/<int:id>', RecipeDetail.as_view()),
    path('recipe/', RecipeListCreate.as_view()),
    # Process views
    path('process/<int:id>', ProcessDetail.as_view()),
    path('process/', ProcessListCreate.as_view()),
    # Process step view
    path('processstep/<int:id>', ProcessStepDetail.as_view()),
    path('processstep/', ProcessStepListCreate.as_view()),
    # Process schedule view
    path('processschedule/<int:id>', ProcessScheduleDetail.as_view()),
    path('processschedule/', ProcessScheduleListCreate.as_view()),
    # Ingredient view
    path('ingredient/<int:id>', RecipeIngredientDetail.as_view()),
    path('ingredient/', RecipeIngredientListCreate.as_view()),
    # Utensil view
    path('utensil/<int:id>', UtensilsDetail.as_view()),
    path('utensil/', UtensilsListCreate.as_view()),

    ### --- Batch Manager --- ###
    # Batch view
    path('batch/<int:id>', BatchDetail.as_view()),
    path('batch/', BatchListCreate.as_view()),
    # QrCode view
    path('qrcode/<int:id>', QrCodeDetail.as_view()),
    path('qrcode/', QrCodeListCreate.as_view()),
    # Execution view
    path('execution/<int:id>', ExecutionDetail.as_view()),
    path('execution/', ExecutionListCreate.as_view()),
    # JournalEntry view
    path('journalentry/<int:id>', JournalEntryDetail.as_view()),
    path('journalentry/', JournalEntryListCreate.as_view()),

]
