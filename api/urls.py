from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')
router.register('id', views.IDViewSet, basename='id')

urlpatterns = [
    path('auth/register', views.UserSingUpView.as_view(), name='register'),
    path('auth/login', views.MyTokenObtainPairView.as_view(), name='login'),
    path('auth/token-refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user', views.UserInfoAPIView.as_view(), name='user_info'),
]

urlpatterns += router.urls

