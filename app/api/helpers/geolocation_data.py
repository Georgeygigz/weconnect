import requests
from django.conf import settings
from django.utils.timezone import datetime


from app import celery_app
from ..authentication.models import User


class UserGeolocationInfo():


    def __init__(self):
        self.country_code = ''


    def make_external_request(self, url):
        """Method that makes external request"""
        response = requests.get(url)
        return response.json()

    def get_geolocation_info(self):
        """Method that gets users geologocal data based
        on the user signup ip
        """

        url = f"{settings.GEO_BASE_URL}/?api_key={settings.GEO_API_KEY}"
        response = self.make_external_request(url)
        self.country_code = response['country_code']
        return response

    def get_current_day_holiday(self):
        """Method that gets current day holiday"""
        day = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year
        url = f'{settings.HOLIDAY_BASE_URL}/?api_key={settings.HOLIDAY_API_KEY}&country={self.country_code}&year={year}&month={month}&day={day}'
        response = self.make_external_request(url)
        return response

    def enrich_user_details(self, user_id):
        """Method that captures geolocation data"""
        user = User.objects.get(pk=user_id)
        user.location_info = self.get_geolocation_info()
        user.holiday_info = self.get_current_day_holiday()
        user.save()

@celery_app.task(name='geolocation_data')
def trigger_geolocation_info_enrichment(user_id):
    """Method that triggers geolocation data enrichment"""
    user_geolocation_info = UserGeolocationInfo()
    user_geolocation_info.enrich_user_details(user_id)