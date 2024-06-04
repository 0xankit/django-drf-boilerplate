'''
Error messages for users app
'''
from enum import Enum

from django.utils.translation import gettext as _


class UserErrorMessages(Enum):
    """
    Enum for error messages

        Example: 
            UserErrorMessages.USER_REGISTERED_SUCCESSFULLY.value
        (with parameter)
            UserErrorMessages.USER_NOT_FOUND_WITH_ID.value.format(id=1)
    """
    USER_REGISTERED_SUCCESSFULLY = _('User registered successfully')
    USER_REGISTRATION_FAILED = _('User registration failed')
    USER_FETCHED_SUCCESSFULLY = _('User fetched successfully')
    USER_NOT_FOUND = _('User not found')
    ERROR_FETCHING_USER = _('Error fetching user')
    ERROR_UPDATING_USER_ROLE = _('Error updating user role')
    USER_ROLE_UPDATED_SUCCESSFULLY = _('User role updated successfully')
    ERROR_UPDATING_USER_DESIGNATION = _('Error updating user designation')
    USER_DESIGNATION_UPDATED_SUCCESSFULLY = _(
        'User designation updated successfully')

    USER_ALREADY_EXISTS = _('User already exists')
    USER_NOT_REGISTERED = _('User not registered')
    USER_NOT_AUTHENTICATED = _('User not authenticated')
    USER_NOT_ACTIVE = _('User not active')
    USER_NOT_ADMIN = _('User not admin')
    USER_NOT_SUPERUSER = _('User not superuser')
    USER_NOT_STAFF = _('User not staff')
    USER_NOT_PERMISSION = _('User does not have permission')
    USER_NOT_FOUND_WITH_ID = _('User not found with id: {id}')
    USER_NOT_FOUND_WITH_EMAIL = _('User not found with email: {email}')
    USER_NOT_FOUND_WITH_USERNAME = _(
        'User not found with username: {username}')
    USER_NOT_FOUND_WITH_PHONE = _('User not found with phone: {phone}')
    USER_NOT_FOUND_WITH_ROLE = _('User not found with role: {role}')
    USER_NOT_FOUND_WITH_DESIGNATION = _(
        'User not found with designation: {designation}')
    USER_NOT_FOUND_WITH_DEPARTMENT = _(
        'User not found with department: {department}')
