from rest_framework.throttling import UserRateThrottle


class CustomThrottle(UserRateThrottle):
    rate = '15/minute'
