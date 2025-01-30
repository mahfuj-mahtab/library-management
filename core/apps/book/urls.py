from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'all', ShowAllBook, basename='user')
urlpatterns = router.urls