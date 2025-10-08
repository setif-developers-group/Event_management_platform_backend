from rest_framework import throttling


class RegisterThrottleMin(throttling.AnonRateThrottle):
    scope = 'registration_min'

class RegisterThrottleHour(throttling.AnonRateThrottle):
    scope = 'registration_hour'


class RegisterThrottleDay(throttling.AnonRateThrottle):
    scope = 'registration_day'


class LoginUserNameThrottle(throttling.AnonRateThrottle):
    scope = 'username_login'
    def get_cache_key(self, request, view):
        if request.method == 'POST':
            username = request.data.get('username')
            if not username:
                return None
            
        return self.cache_format % {
            'scope': self.scope,
            'ident': username.lower()
        }

class LoginThrottle(throttling.AnonRateThrottle):
    scope = 'login'


class RefreshThrottle(throttling.AnonRateThrottle):
    scope = 'refresh'

class ConfirmEmailThrottle(throttling.AnonRateThrottle):
    rate = '1/min'

class ConfirmEmailHourThrottle(throttling.AnonRateThrottle):
    rate = '10/hour'

class ConfirmEmailDayThrottle(throttling.AnonRateThrottle):
    rate = '20/day'
