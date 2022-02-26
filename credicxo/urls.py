"""credicxo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from rest_framework_simplejwt import views as jwt_views
from schoolmanageapp.views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Credicxo API",
      default_version='v1',
      description="A Rest Api for Credicxo task",
      contact=openapi.Contact(email="abc@gmail.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('RegisterApiView',RegisterApiView.as_view()),
    path("ViewUserAccount",ViewUserAccount.as_view()),
    path("ViewAndAddstudentApiView",ViewAndAddstudentApiView.as_view()),
    path("StudentProfile",StudentProfile.as_view()),
    path("SendOtpToForgetPassword",SendOtpToForgetPassword.as_view()),
    path("VerifyForgetpasswordOtp",VerifyForgetpasswordOtp.as_view()),
    path('swagger<format>.json|.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]