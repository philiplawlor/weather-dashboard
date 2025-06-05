import os
import requests
import logging
from datetime import datetime, timedelta
from ..models import db, WeatherData

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherService:
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')
        logger.info(f"Initializing WeatherService with API key: {'*' * 8 + self.api_key[-4:] if self.api_key else 'None'}")
        if not self.api_key:
            error_msg = "OpenWeatherMap API key is required. Please set OPENWEATHER_API_KEY in your .env file"
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    def get_weather_by_city(self, city_name, country_code=''):
        """
        Get current weather data for a city name
        
        Args:
            city_name (str): Name of the city
            country_code (str, optional): Country code. Defaults to ''.
            
        Returns:
            dict: Weather data
        """
        query = f"{city_name},{country_code}" if country_code else city_name
        params = {
            'q': query,
            'appid': self.api_key,
            'units': 'imperial'  # Get temperature in Fahrenheit
        }
        return self._fetch_weather(params, f"city: {city_name}, country: {country_code}")
    
    def get_weather_by_zip(self, zip_code, country_code='US'):
        """
        Get current weather data for a ZIP code
        
        Args:
            zip_code (str): ZIP code
            country_code (str, optional): Country code. Defaults to 'US'.
            
        Returns:
            dict: Weather data or None if failed
        """
        try:
            # Clean the zip code (remove any non-digit characters)
            clean_zip = ''.join(c for c in zip_code if c.isdigit())
            if not clean_zip:
                logger.error(f"Invalid ZIP code format: {zip_code}")
                return None
                
            logger.info(f"Fetching weather for ZIP code: {clean_zip}, country: {country_code}")
            
            params = {
                'zip': f"{clean_zip},{country_code}",
                'appid': self.api_key,
                'units': 'imperial'  # Get temperature in Fahrenheit
            }
            
            return self._fetch_weather(params, f"ZIP: {clean_zip}, country: {country_code}")
            
        except Exception as e:
            logger.error(f"Error in get_weather_by_zip: {str(e)}", exc_info=True)
            return None
    
    def _fetch_weather(self, params, location_desc):
        """
        Internal method to fetch weather data from the API
        
        Args:
            params (dict): Request parameters
            location_desc (str): Description of the location for logging
            
        Returns:
            dict: Weather data or None if failed
        """
        logger.info(f"Fetching weather data for {location_desc}")
        logger.debug(f"API Request URL: {self.BASE_URL}")
        logger.debug(f"API Request Params: {params}")
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            logger.debug(f"API Response Status: {response.status_code}")
            logger.debug(f"API Response Headers: {response.headers}")
            logger.debug(f"API Response Body: {response.text[:200]}...")  # Log first 200 chars
            
            response.raise_for_status()
            data = response.json()
            
            # Save to database
            weather_data = self._save_weather_data(data)
            if weather_data:
                logger.info(f"Successfully retrieved weather data for {location_desc}")
                return weather_data.to_dict()
            else:
                logger.error(f"Failed to save weather data for {location_desc}")
                return None
                
        except requests.exceptions.HTTPError as http_err:
            error_msg = f"HTTP error occurred for {location_desc}: {http_err}"
            if hasattr(http_err, 'response') and http_err.response is not None:
                error_msg += f" - Response: {http_err.response.text}"
            logger.error(error_msg)
            return None
            
        except requests.exceptions.RequestException as req_err:
            error_msg = f"Error fetching weather data for {location_desc}: {req_err}"
            logger.error(error_msg)
            return None
            
        except Exception as e:
            error_msg = f"Unexpected error for {location_desc}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return None
    
    def _save_weather_data(self, api_data):
        """Save weather data to the database"""
        try:
            if not api_data or 'weather' not in api_data or 'main' not in api_data:
                logger.error(f"Invalid API response data: {api_data}")
                return None
                
            weather = api_data.get('weather', [{}])[0]
            main_data = api_data.get('main', {})
            
            if not weather or not main_data:
                logger.error(f"Missing required weather data in API response: {api_data}")
                return None
            
            location = f"{api_data.get('name')}, {api_data.get('sys', {}).get('country')}"
            if not location or location == ', ':
                logger.error(f"Could not determine location from API response: {api_data}")
                return None
                
            weather_data = WeatherData(
                location=location,
                temperature=main_data.get('temp'),
                humidity=main_data.get('humidity'),
                description=weather.get('description', '').capitalize(),
                icon=weather.get('icon', ''),
                timestamp=datetime.utcnow()
            )
            
            db.session.add(weather_data)
            db.session.commit()
            return weather_data
            
        except Exception as e:
            logger.error(f"Error saving weather data: {str(e)}", exc_info=True)
            db.session.rollback()
            return None
