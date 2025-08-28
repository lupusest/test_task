from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView 
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Убираем лишние импорты
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(
      title="Project API",
      default_version='v1',
      description="API for Content Management",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/v1/pages/', include('pages.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

# Этот блок оставляем, он нужен для статики в админке
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
