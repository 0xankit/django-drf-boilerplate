# views.py
from venv import logger

from django.contrib.auth import authenticate
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import CustomUser, Designation, Role
from apps.users.permissions import IsAdminUserOrReadOnly
from django_drf_boilerplate.utils.response import ApiResponse

from .serializers import (CustomTokenObtainPairSerializer,
                          DesignationSerializer, ManageUserDesignation,
                          ManageUserRolesSerializer, RoleSerializer,
                          UserSerializer)


@swagger_auto_schema(method='post',
                     operation_description=_('Register User API'),
                     request_body=UserSerializer,
                     responses={200: UserSerializer})
@api_view(['POST'])
def register_user(request):
    '''
    Register User API

    Parameters
    ----------
        request : `HttpRequest`
            User request object

    Returns
    -------
        `ApiResponse`
        API response in standard format
    '''
    logger.debug('Register user: %s', request.data)
    data = request.data
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        logger.info('User registered successfully: %s',
                    serializer.data.get('id'))
        return ApiResponse.success(data=serializer.data, message='User registered successfully')
    logger.error('Error in registering user: %s', serializer.errors)
    return ApiResponse.error(message=serializer.errors)


@swagger_auto_schema(method='get',
                     operation_description=_('Get User Profile API'),
                     responses={200: UserSerializer})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    '''
    Get User Profile API

    Parameters
    ----------
        request : `HttpRequest`
            User request object

    Returns
    -------
        `ApiResponse`
        API response in standard format
    '''
    logger.debug('Get user profile: %s', request.user.id)
    try:
        user = get_object_or_404(CustomUser, id=request.user.id)
        serializer = UserSerializer(user)
        return ApiResponse.success(data=serializer.data, message=_('User profile fetched successfully'))
    except Http404:
        logger.error('User not found: %s', request.user.id)
        return ApiResponse.error(message=_('User not found'))
    except Exception as exp:
        logger.error('Error in fetching user profile: %s', exp)
        return ApiResponse.error(message=str(exp))


class RoleListViews(generics.ListCreateAPIView):
    """
    Role List Views
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUserOrReadOnly, IsAuthenticated]


class DesignationListViews(generics.ListCreateAPIView):
    """
    Designation List Views
    """
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [IsAdminUserOrReadOnly, IsAuthenticated]

    # def get(self, request, *args, **kwargs):
    #     """
    #     Get Designation List
    #     """
    #     return super().get(request, *args, **kwargs)


# custom authentication Token pair
class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom Token Obtain Pair View

    Args:
        TokenObtainPairView (TokenObtainPairView): Token Obtain Pair View
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


@swagger_auto_schema(method='put',
                     operation_description=_('Update User Roles'),
                     request_body=RoleSerializer,
                     responses={200: RoleSerializer})
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_roles(request):
    """
    Update User Roles
    """
    logger.info('Update User Roles: %s', request.data)
    try:
        user = get_object_or_404(CustomUser, id=request.user.id)
        roles_serializer = ManageUserRolesSerializer(
            instance=user, data=request.data, partial=True)
        if not roles_serializer.is_valid():
            logger.error('Error in updating user roles: %s',
                         roles_serializer.errors)
            return ApiResponse.error(message=roles_serializer.errors)
        roles_serializer.save()
        return ApiResponse.success(message='User roles updated successfully')
    except Http404:
        logger.error('User not found: %s', request.user.id)
        return ApiResponse.error(message='User not found')


# update designation
@swagger_auto_schema(method='put',
                     operation_description=_('Update User Designation'),
                     request_body=DesignationSerializer,
                     responses={200: DesignationSerializer})
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_designation(request):
    """
    Update User Designation
    """
    logger.info('Update User Designation: %s', request.data)
    try:
        user = get_object_or_404(CustomUser, id=request.user.id)
        designation_serializer = ManageUserDesignation(
            instance=user, data=request.data, partial=True)
        if not designation_serializer.is_valid():
            logger.error('Error in updating user designation: %s',
                         designation_serializer.errors)
            return ApiResponse.error(message=designation_serializer.errors)
        designation_serializer.save()
        return ApiResponse.success(message='User designation updated successfully')
    except Http404:
        logger.error('User not found: %s', request.user.id)
        return ApiResponse.error(message='User not found')
