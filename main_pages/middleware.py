from django.contrib.gis.geoip2 import GeoIP2
from .models import WebsiteVisit
import logging

logger = logging.getLogger(__name__)

class TrackVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        try:
            self.geoip = GeoIP2()
        except Exception as e:
            logger.error(f"Could not initialize GeoIP2: {e}. Location data will not be tracked.")
            self.geoip = None

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Avoid tracking visits to admin or static/media files if desired
        # if request.path.startswith('/admin/') or request.path.startswith('/static/') or request.path.startswith('/media/'):
        #     return self.get_response(request)

        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        country, city, timezone = None, None, None
        if self.geoip and ip_address:
            try:
                location_info = self.geoip.city(ip_address)
                country = location_info.get('country_name')
                city = location_info.get('city')
                timezone = location_info.get('time_zone')
            except Exception as e:
                # Handle cases where IP is private or GeoIP lookup fails
                logger.warning(f"Could not get GeoIP info for {ip_address}: {e}")


        # Check if a similar visit record already exists recently to avoid duplicates (optional)
        # if not WebsiteVisit.objects.filter(ip_address=ip_address, user_agent=user_agent).order_by('-timestamp').first() ... :

        try:
            WebsiteVisit.objects.create(
                ip_address=ip_address,
                user_agent=user_agent,
                country=country,
                city=city,
                timezone=timezone
            )
        except Exception as e:
            logger.error(f"Failed to save website visit for {ip_address}: {e}")


        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def get_client_ip(self, request):
        """Gets the client IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

# --- Add this middleware to your settings.py ---
# MIDDLEWARE = [
#     ...,
#     'portfolio.middleware.TrackVisitMiddleware', # Add your middleware here
#     ...,
# ]