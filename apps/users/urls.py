# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.users.views import (CustomTokenObtainPairView, DesignationListViews,
                              RoleListViews, get_user_profile, register_user,
                              update_user_designation, update_user_roles)

urlpatterns = [
    path('user/', register_user, name='register_user'),
    path('profile/', get_user_profile, name='get_user_profile'),
    # path('login/', login_user, name='login_user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('roles/', RoleListViews.as_view(), name='role_list'),
    path('designations/', DesignationListViews.as_view(), name='designation_list'),
    path('update-role/', update_user_roles, name='update_user_roles'),
    path('update-designation/', update_user_designation,
         name='update_user_designation'),
]
