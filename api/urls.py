from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')
router.register('id', views.IDViewSet, basename='id')
router.register('entities', views.EntityViewSet, basename='entity')
router.register('models', views.ModelViewSet, basename='model')
router.register('accounts', views.AccountViewSet, basename='account')
router.register('journals', views.JournalViewSet, basename='journal')
router.register('plans', views.PlanViewSet, basename='plan')
router.register('trans-ids', views.TransIDsViewSet, basename='trans')
router.register('trans-types', views.TransTypesViewSet, basename='type')

urlpatterns = [
    path('auth/register', views.UserSingUpView.as_view(), name='register'),
    path('auth/login', views.MyTokenObtainPairView.as_view(), name='login'),
    path('auth/token-refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user', views.UserInfoAPIView.as_view(), name='user_info'),
]

urlpatterns += router.urls

