import os
import sys
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

# Check for required environment variables
required_vars = ['OPENWEATHER_API_KEY']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"Error: The following required environment variables are missing: {', '.join(missing_vars)}")
    print("Please create a .env file with these variables or set them in your environment.")
    print("See .env.example for an example configuration.")
    sys.exit(1)

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Debug information
    print("\n=== Weather Dashboard ===")
    print(f"Environment: {os.getenv('FLASK_ENV', 'production')}")
    print(f"Debug mode: {os.getenv('FLASK_DEBUG', 'False')}")
    print(f"OpenWeatherMap API Key: {'*' * 8 + os.getenv('OPENWEATHER_API_KEY')[-4:] if os.getenv('OPENWEATHER_API_KEY') else 'Not set'}")
    print(f"Database URL: {os.getenv('DATABASE_URL', 'sqlite:///weather.db')}")
    print("\nStarting server... (Press Ctrl+C to quit)")
    print(f" * Running on http://127.0.0.1:{port}")
    
    # Run the application
    app.run(host='0.0.0.0', port=port, debug=True)
