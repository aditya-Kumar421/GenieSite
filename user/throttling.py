from rest_framework.throttling import ScopedRateThrottle

class CustomScopedRateThrottle(ScopedRateThrottle):
    def get_cache_key(self, request, view):
        """
        Generate a cache key based on the user ID (string) or IP for anonymous users.
        """
        # If there's a user ID from JWT, use it
        if hasattr(request, 'user') and request.user:
            ident = request.user  # This is the user_id string
        else:
            # For anonymous users, use the IP address
            ident = self.get_ident(request)

        # Combine with the throttle scope
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }