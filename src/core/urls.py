"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from core import settings
from logic.api.urls import urlpatterns
from drf_spectacular.views import (
    SpectacularAPIView as OpenAPI,
    SpectacularRedocView as Redoc,
    SpectacularSwaggerView as Swagger
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView as TokenView,
    TokenRefreshView as TokenRefresh,
    TokenVerifyView as TokenVerify,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefresh.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerify.as_view(), name='token_verify'),
    path("api-auth/", include("rest_framework.urls")),  
    path('api/v1/', include((urlpatterns, 'logic'), namespace='v1')),
    path(
        'api/v1/schema/',
        OpenAPI.as_view(api_version='v1'),
        name='schema'
    ),
    path(
        'api/v1/schema/swagger/',
        Swagger.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'api/v1/schema/redoc/',
        Redoc.as_view(url_name='schema'),
        name='redoc'
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
