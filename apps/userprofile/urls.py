from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path(r'api/auth/tokens', views.LoginView.as_view())
]

router = DefaultRouter()
# router.register(r'api/auth/tokens', views.TokenViewSet)
router.register(r'api/users', views.UserViewSet)

urlpatterns += router.urls
