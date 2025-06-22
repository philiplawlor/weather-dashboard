# 🌦️ Weather Dashboard

[![GitHub stars](https://img.shields.io/github/stars/philiplawlor/weather-dashboard?style=social)](https://github.com/philiplawlor/weather-dashboard/stargazers) [![GitHub license](https://img.shields.io/github/license/philiplawlor/weather-dashboard)](https://github.com/philiplawlor/weather-dashboard/blob/master/LICENSE)

A responsive web application that displays real-time weather data from the OpenWeatherMap API. Built with Flask, Bootstrap 5, and modern JavaScript.

🔗 **Live Demo**: [https://philiplawlor.github.io/weather-dashboard/](https://philiplawlor.github.io/weather-dashboard/)

## 📌 Features

- 🌍 Search weather by city name or ZIP code (US only)
- 🌡️ Temperature display in Fahrenheit
- 📱 Responsive design that works on all devices
- 📊 View detailed weather information including:
  - Current conditions
  - Temperature (feels like, min/max)
  - Humidity and wind speed
  - Weather description and icons
- 📜 Search history
- 📱 Mobile-friendly interface
- 🌙 Dark/Light mode support

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (for local development)
- Docker and Docker Compose (for containerized deployment)
- OpenWeatherMap API key (get one at [OpenWeatherMap](https://openweathermap.org/api))

### Running with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/philiplawlor/weather-dashboard.git
   cd weather-dashboard
   ```

2. **Create a `.env` file**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your OpenWeatherMap API key:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   SECRET_KEY=your_secret_key_here
   ```

3. **Build and start the containers**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   Open your browser and go to: http://localhost:5000

### Local Development Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/philiplawlor/weather-dashboard.git
   cd weather-dashboard
   ```

2. **Set up a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
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
   - Add your OpenWeatherMap API key:
   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   SECRET_KEY=your_secret_key_here
   ```

5. **Run the application**
   ```bash
   # Windows
   .\run.bat
   
   # Unix/MacOS
   chmod +x run.sh
   ./run.sh
   ```
   The application will be available at `http://127.0.0.1:5000`

## 🛠️ Built With

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap 5](https://getbootstrap.com/) - Frontend framework
- [OpenWeatherMap API](https://openweathermap.org/api) - Weather data
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [Bootstrap Icons](https://icons.getbootstrap.com/) - Icons

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/philiplawlor/weather-dashboard](https://github.com/philiplawlor/weather-dashboard)

## 🙏 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for the free weather API
- [Bootstrap](https://getbootstrap.com/) for the awesome frontend framework
- [Flask](https://flask.palletsprojects.com/) for the simple yet powerful web framework

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
