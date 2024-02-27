from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import UserDetailView, LoginView, RegisterView, LogoutView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserDetailView.as_view(), name='user'),
]
