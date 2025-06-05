import os
import logging
from flask import Flask, jsonify
from dotenv import load_dotenv

def create_app():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # Create and configure the app
    app = Flask(__name__)
    
    # Load configuration from environment variables
    try:
        # Load environment variables from .env file
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        load_dotenv(env_path)
        
        # Basic configuration
        app.config.update(
            SECRET_KEY=os.getenv('SECRET_KEY', 'dev-secret-key'),
            SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///weather.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            OPENWEATHER_API_KEY=os.getenv('OPENWEATHER_API_KEY')
        )
        
        # Verify required configuration
        if not app.config['OPENWEATHER_API_KEY']:
            raise ValueError('OPENWEATHER_API_KEY is not set in environment variables')
            
        logger.info('Application configuration loaded successfully')
        
    except Exception as e:
        logger.error(f'Error loading configuration: {str(e)}')
        raise
    
    # Initialize extensions
    from .models import db
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            logger.info('Database tables created successfully')
        except Exception as e:
            logger.error(f'Error creating database tables: {str(e)}')
            raise
    
    # Register blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'status': 'error', 'message': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500
    
    logger.info('Flask application initialized successfully')
    return app
