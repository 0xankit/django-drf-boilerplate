'''
API response class for returning response in standard format

Usage:
    from django_drf_boilerplate.utils.response import ApiResponse
    
    # Success response
    return ApiResponse.success(data={'key': 'value'}, message='Success', status_code=200)
    
    # Error response
    return ApiResponse.error(message='Error', status_code=400)
    
    # Exception response
    return ApiResponse.exception(message='Exception', status_code=500)
    
    # Custom response
    return ApiResponse.custom_response(data={'key': 'value'}, message='Custom message', status_code=200)
    
'''
from django.http import JsonResponse
from rest_framework import status


class ApiResponse:
    '''
    Api response class for returning response in standard format
    '''
    @staticmethod
    def success(data=None, message='Success', status_code=status.HTTP_200_OK):
        """
        Returns a success response in standard format

        Parameters
        ----------
            data : dict
                data to be sent in response
            message : str
                message to be sent in response
            status_code : int
                status code of response
        """
        response_data = {'success': True, 'message': message}
        if data is not None:
            response_data['data'] = data
        return JsonResponse(response_data, status=status_code)

    @staticmethod
    def error(message='Error', status_code=status.HTTP_400_BAD_REQUEST):
        '''
        Returns an error response in standard format

        Parameters
        ----------
            message : `str`
                message to be sent in response
            status_code : `int`
                status code of response
        '''
        response_data = {'success': False, 'message': message}
        return JsonResponse(response_data, status=status_code)

    @staticmethod
    def exception(message="Exception", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        '''
        Returns an exception response in standard format

        Parameters
        ----------
            message : `str`
                message to be sent in response
            status_code : `int`
                status code of response
        '''
        response_data = {'success': False, 'message': message}
        return JsonResponse(response_data, status=status_code)

    @staticmethod
    def custom_response(data, message, status_code):
        '''
        Returns a custom response in standard format

        Parameters
        ----------
            data : `dict`
                data to be sent in response
            message : `str`
                message to be sent in response
            status_code : `int`
                status code of response
        '''
        response_data = {'success': True, 'message': message, 'data': data}
        return JsonResponse(response_data, status=status_code)
