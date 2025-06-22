import logging
from flask import Blueprint, render_template, request, jsonify, current_app
from .services.weather_service import WeatherService
from .models import db, WeatherData
from sqlalchemy import text

# Set up logging
logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@main.route('/about')
def about():
    """Render the about page"""
    return render_template('about.html')

@main.route('/health')
def health_check():
    """Health check endpoint for Docker and load balancers"""
    try:
        # Check database connection
        db.session.execute(text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'message': 'Service is running',
            'database': 'connected'
        }), 200
    except Exception as e:
        current_app.logger.error(f'Health check failed: {str(e)}')
        return jsonify({
            'status': 'unhealthy',
            'message': str(e),
            'database': 'connection failed'
        }), 500

@main.route('/api/weather', methods=['GET'])
def get_weather():
    """API endpoint to get weather data for a location"""
    try:
        city = request.args.get('city')
        zip_code = request.args.get('zip')
        country = request.args.get('country', 'US')  # Default to US for ZIP codes
        
        logger.debug(f"Request args: {dict(request.args)}")
        
        if not (city or zip_code):
            error_msg = "Either 'city' or 'zip' parameter is required"
            logger.warning(error_msg)
            return jsonify({
                'status': 'error',
                'message': error_msg,
                'requested_params': dict(request.args)
            }), 400
        
        location = f"ZIP: {zip_code}, Country: {country}" if zip_code else f"City: {city}, Country: {country}"
        logger.info(f"Processing weather request for {location}")
        
        weather_service = WeatherService()
        
        try:
            if zip_code:
                # Handle ZIP code search
                logger.debug(f"Attempting ZIP code lookup for {zip_code}, {country}")
                weather_data = weather_service.get_weather_by_zip(zip_code, country)
            else:
                # Handle city name search
                logger.debug(f"Attempting city lookup for {city}, {country}")
                weather_data = weather_service.get_weather_by_city(city, country)
            
            if weather_data:
                logger.info(f"Successfully retrieved weather data for {location}")
                return jsonify({
                    'status': 'success',
                    'data': weather_data,
                    'location': location
                })
            else:
                error_msg = f"No weather data found for {location}"
                logger.error(error_msg)
                return jsonify({
                    'status': 'error',
                    'message': error_msg,
                    'requested_location': location,
                    'suggestion': 'Please check the location and try again.'
                }), 404
                
        except Exception as e:
            error_msg = f"Error processing weather request for {location}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return jsonify({
                'status': 'error',
                'message': 'An error occurred while processing your request',
                'details': str(e),
                'requested_location': location
            }), 500
            
    except Exception as e:
        error_msg = f"Unexpected error in weather endpoint: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'An unexpected error occurred',
            'details': str(e)
        }), 500
            
    except ValueError as ve:
        error_msg = f"Configuration error: {str(ve)}"
        logger.error(error_msg)
        return jsonify({
            'status': 'error',
            'message': error_msg
        }), 500
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'An unexpected error occurred while fetching weather data'
        }), 500

@main.route('/api/weather/history', methods=['GET'])
def get_weather_history():
    """API endpoint to get weather history"""
    try:
        # Get the last 10 weather records
        history = WeatherData.query.order_by(WeatherData.timestamp.desc()).limit(10).all()
        return jsonify({
            'status': 'success',
            'data': [data.to_dict() for data in history]
        })
    except Exception as e:
        current_app.logger.error(f"Error in get_weather_history: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to fetch weather history'
        }), 500
