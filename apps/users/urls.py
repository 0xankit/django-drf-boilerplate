# urls.py
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from apps.users.views import get_user_profile, register_user

urlpatterns = [
    path('user/', register_user, name='register_user'),
    path('profile/', get_user_profile, name='get_user_profile'),
    # path('login/', login_user, name='login_user'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
