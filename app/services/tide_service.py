import os
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

class TideService:
    """Service for fetching tide and beach forecast data."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the TideService with an optional API key.
        
        Args:
            api_key: Optional API key for the tide service. If not provided,
                   will try to get from environment variable STORMGLASS_API_KEY.
        """
        self.api_key = api_key or os.getenv('STORMGLASS_API_KEY')
        self.base_url = "https://api.stormglass.io/v2"
        
    def get_tide_data(self, lat: float, lng: float, start: datetime = None, 
                     end: datetime = None) -> Dict:
        """Get tide data for a specific location and time range.
        
        Args:
            lat: Latitude of the location
            lng: Longitude of the location
            start: Start datetime (defaults to now if not provided)
            end: End datetime (defaults to 24 hours from start if not provided)
            
        Returns:
            Dictionary containing tide data
        """
        if not self.api_key:
            logger.error("No StormGlass API key provided")
            return {"error": "Tide data service not configured"}
            
        start = start or datetime.utcnow()
        end = end or (start + timedelta(days=1))
        
        try:
            response = requests.get(
                f"{self.base_url}/tide/extremes/point",
                params={
                    'lat': lat,
                    'lng': lng,
                    'start': start.timestamp(),
                    'end': end.timestamp()
                },
                headers={
                    'Authorization': self.api_key
                }
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching tide data: {str(e)}")
            return {"error": f"Failed to fetch tide data: {str(e)}"}
    
    def get_beach_conditions(self, lat: float, lng: float) -> Dict:
        """Get beach conditions including water temperature, wave height, etc.
        
        Args:
            lat: Latitude of the location
            lng: Longitude of the location
            
        Returns:
            Dictionary containing beach conditions
        """
        if not self.api_key:
            logger.error("No StormGlass API key provided")
            return {"error": "Beach conditions service not configured"}
            
        end = datetime.utcnow()
        start = end - timedelta(hours=24)  # Last 24 hours of data
        
        try:
            response = requests.get(
                f"{self.base_url}/weather/point",
                params={
                    'lat': lat,
                    'lng': lng,
                    'params': ','.join([
                        'waterTemperature',
                        'waveHeight',
                        'waveDirection',
                        'swellHeight',
                        'swellPeriod',
                        'swellDirection',
                        'windWaveHeight',
                        'windWavePeriod',
                        'windWaveDirection'
                    ]),
                    'start': start.timestamp(),
                    'end': end.timestamp()
                },
                headers={
                    'Authorization': self.api_key
                }
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching beach conditions: {str(e)}")
            return {"error": f"Failed to fetch beach conditions: {str(e)}"}
    
    def get_combined_beach_forecast(self, lat: float, lng: float) -> Dict:
        """Get combined tide and beach conditions for a location.
        
        Args:
            lat: Latitude of the location
            lng: Longitude of the location
            
        Returns:
            Dictionary containing both tide and beach conditions
        """
        return {
            "tides": self.get_tide_data(lat, lng),
            "conditions": self.get_beach_conditions(lat, lng),
            "location": {"lat": lat, "lng": lng},
            "timestamp": datetime.utcnow().isoformat()
        }
