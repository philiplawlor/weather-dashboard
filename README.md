# Weather Dashboard

A web application that displays weather data from the OpenWeatherMap API.

## Version
0.1.0 (Released: June 5, 2025)

## Features
- Get current weather data from the OpenWeatherMap API
- Search for weather by city name or ZIP code (US only)
- View detailed weather information including temperature, humidity, and conditions
- Responsive design that works on desktop and mobile devices
- View recent search history
- Temperature display in Fahrenheit
- Error handling and user feedback
- About page with project information

## Getting Started

### Prerequisites
- Python 3.8+
- OpenWeatherMap API key (get one at [OpenWeatherMap](https://openweathermap.org/api))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd windsurf_demo
   ```

2. **Set up a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Unix/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Add your OpenWeatherMap API key
   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```

### Running the Application

#### Option 1: Using the provided scripts
- **Windows**: Double-click `run.bat` or run it from the command line
- **Unix/MacOS**: Make the script executable and run it
  ```bash
  chmod +x run.sh
  ./run.sh
  ```

#### Option 2: Manual start
```bash
# Set environment variables
set FLASK_APP=run.py
set FLASK_ENV=development

# Run the application
flask run
```

The application will be available at `http://localhost:5000`

## Project Structure

```
weather_dashboard/
├── app/                    # Main application package
│   ├── __init__.py         # Application factory
│   ├── models.py           # Database models
│   ├── routes.py           # Application routes
│   ├── services/           # Business logic
│   │   └── weather_service.py  # OpenWeatherMap API client
│   ├── static/             # Static files
│   │   ├── css/            # Stylesheets
│   │   └── js/             # JavaScript files
│   └── templates/          # HTML templates
│       ├── base.html       # Base template
│       └── index.html      # Main page
├── tests/                  # Test files
├── .env.example            # Example environment variables
├── .gitignore             # Git ignore file
├── requirements.txt        # Python dependencies
├── run.py                 # Application entry point
├── run.bat                # Windows launcher
└── run.sh                 # Unix/MacOS launcher
```

## Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for their free weather API
- [Bootstrap](https://getbootstrap.com/) for the responsive design framework
- [Flask](https://flask.palletsprojects.com/) for the web framework
