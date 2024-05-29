# views.py
from venv import logger

from django.contrib.auth import authenticate
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from apps.users.models import CustomUser
from django_drf_boilerplate.utils.response import ApiResponse

from .serializers import LoginRequestSerializer, UserSerializer


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


# login_user
@swagger_auto_schema(method='post',
                     operation_description=_('Login User API'),
                     request_body=LoginRequestSerializer,
                     responses={200: UserSerializer})
@api_view(['POST'])
def login_user(request):
    '''
    Login User API

    Parameters
    ----------
        request : `HttpRequest`
            User request object

    Returns
    -------
        `ApiResponse`
        API response in standard format
    '''
    logger.debug('Login user: %s', request.data)
    data = request.data
    request = LoginRequestSerializer(data=data)
    if not request.is_valid():
        logger.debug('Error in logging in user: %s', request.errors)
        return ApiResponse.error(message=request.errors)
    # user can login with username or email
    user = authenticate(
        username=data.get('username'), password=data.get('password'))
    if user:
        serializer = UserSerializer(user)
        logger.info('User logged in successfully: %s', user.id)
        return ApiResponse.success(data=serializer.data, message='User logged in successfully')
    logger.error('Error in logging in user: %s', _('Invalid credentials'))
    return ApiResponse.error(message=_('Invalid credentials'))
