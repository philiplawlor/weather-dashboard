# Weather Dashboard - Technical Specification

## 1. System Architecture

### 1.1 High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │   Flask App     │    │  External APIs  │
│   (Frontend)    │◄──►│   (Backend)     │◄──►│  OpenWeatherMap │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │    Database     │
                       │  PostgreSQL/    │
                       │    SQLite       │
                       └─────────────────┘
```

### 1.2 Technology Stack

#### Backend
- **Language**: Python 3.9+
- **Web Framework**: Flask 2.3.3
- **Database ORM**: SQLAlchemy 3.1.1
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Testing**: pytest, pytest-cov
- **Configuration**: python-dotenv
- **HTTP Client**: requests 2.31.0

#### Frontend
- **Framework**: Bootstrap 5.3.x
- **JavaScript**: Vanilla ES6+
- **Icons**: Bootstrap Icons
- **CSS**: Custom styles with Bootstrap variables
- **Images**: OpenWeatherMap weather icons

#### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Web Server**: Gunicorn (production)
- **Database**: PostgreSQL 14+
- **Caching**: Redis (future)
- **Monitoring**: Application health endpoints

## 2. Database Schema

### 2.1 Core Tables

#### weather_data
Stores current weather information and search history.

```sql
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    location VARCHAR(100) NOT NULL,           -- "City, Country"
    latitude DECIMAL(10, 8),                   -- GPS coordinates
    longitude DECIMAL(11, 8),                  -- GPS coordinates
    temperature DECIMAL(5, 2) NOT NULL,       -- Current temperature
    feels_like DECIMAL(5, 2),                  -- Feels like temperature
    temperature_min DECIMAL(5, 2),             -- Daily minimum
    temperature_max DECIMAL(5, 2),             -- Daily maximum
    humidity INTEGER NOT NULL,                 -- Relative humidity %
    pressure DECIMAL(7, 2),                    -- Atmospheric pressure hPa
    visibility INTEGER,                        -- Visibility in meters
    uv_index DECIMAL(3, 1),                    -- UV index
    wind_speed DECIMAL(5, 2),                  -- Wind speed m/s
    wind_direction INTEGER,                    -- Wind direction degrees
    wind_gust DECIMAL(5, 2),                   -- Wind gust m/s
    weather_main VARCHAR(50) NOT NULL,          -- Main weather (Rain, Snow, etc.)
    weather_description VARCHAR(200) NOT NULL,  -- Detailed description
    weather_icon VARCHAR(10),                  -- Weather icon code
    cloud_cover INTEGER,                       -- Cloudiness percentage
    sunrise TIMESTAMP,                         -- Sunrise time
    sunset TIMESTAMP,                          -- Sunset time
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_source VARCHAR(20) DEFAULT 'openweathermap', -- API source
    api_response JSONB,                        -- Raw API response
    search_query VARCHAR(200),                 -- Original user query
    user_agent TEXT,                           -- Browser user agent
    ip_address INET,                           -- User IP address
    INDEX idx_location_timestamp (location, timestamp DESC),
    INDEX idx_timestamp (timestamp DESC)
);
```

#### user_preferences (Future)
Stores user customization preferences.

```sql
CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(36),                       -- UUID for anonymous users
    temperature_units VARCHAR(1) DEFAULT 'F',   -- 'F' or 'C'
    wind_speed_units VARCHAR(10) DEFAULT 'mph', -- 'mph', 'km/h', 'm/s'
    pressure_units VARCHAR(10) DEFAULT 'hPa',   -- 'hPa', 'inHg', 'mmHg'
    theme VARCHAR(10) DEFAULT 'auto',          -- 'light', 'dark', 'auto'
    default_location VARCHAR(200),             -- Saved default location
    notifications_enabled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);
```

#### weather_forecasts (Future)
Stores forecast data.

```sql
CREATE TABLE weather_forecasts (
    id SERIAL PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    forecast_date DATE NOT NULL,
    temperature_high DECIMAL(5, 2),
    temperature_low DECIMAL(5, 2),
    weather_main VARCHAR(50),
    weather_description VARCHAR(200),
    weather_icon VARCHAR(10),
    humidity INTEGER,
    wind_speed DECIMAL(5, 2),
    precipitation_probability INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_location_date (location, forecast_date),
    UNIQUE(location, forecast_date)
);
```

### 2.2 Database Configuration

#### Development (SQLite)
```python
DATABASE_URL = "sqlite:///weather.db"
```

#### Production (PostgreSQL)
```python
DATABASE_URL = "postgresql://user:password@localhost:5432/weather_dashboard"
```

## 3. API Specification

### 3.1 Authentication
Currently no authentication required. Future implementation may use JWT tokens.

### 3.2 Base URL
```
https://api.weather-dashboard.com/v1
```

### 3.3 Endpoints

#### GET /api/weather
Retrieve current weather data for a location.

**Request Parameters:**
```
city (string, optional): City name (e.g., "London")
zip (string, optional): ZIP/postal code (e.g., "10001")
country (string, optional): Country code (default: "US")
units (string, optional): "imperial" or "metric" (default: "imperial")
```

**Response Format:**
```json
{
    "status": "success",
    "data": {
        "location": "New York, US",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "temperature": 75.2,
        "feels_like": 77.1,
        "temperature_min": 68.0,
        "temperature_max": 82.0,
        "humidity": 65,
        "pressure": 1013.2,
        "visibility": 10000,
        "uv_index": 6.5,
        "wind_speed": 8.5,
        "wind_direction": 180,
        "wind_gust": 12.3,
        "weather_main": "Clear",
        "weather_description": "Clear sky",
        "weather_icon": "01d",
        "cloud_cover": 10,
        "sunrise": "2025-01-14T12:30:00Z",
        "sunset": "2025-01-15T00:15:00Z",
        "timestamp": "2025-01-14T15:30:00Z"
    },
    "location": "City: New York, Country: US",
    "units": "imperial"
}
```

**Error Response:**
```json
{
    "status": "error",
    "message": "City not found",
    "requested_location": "City: InvalidCity, Country: US",
    "suggestion": "Please check the location and try again."
}
```

#### GET /api/weather/history
Retrieve recent weather search history.

**Request Parameters:**
```
limit (integer, optional): Number of records to return (default: 10, max: 100)
offset (integer, optional): Pagination offset (default: 0)
```

**Response Format:**
```json
{
    "status": "success",
    "data": [
        {
            "id": 1,
            "location": "New York, US",
            "temperature": 75.2,
            "humidity": 65,
            "weather_description": "Clear sky",
            "weather_icon": "01d",
            "timestamp": "2025-01-14T15:30:00Z"
        }
    ],
    "pagination": {
        "total": 25,
        "limit": 10,
        "offset": 0,
        "has_more": true
    }
}
```

#### GET /api/weather/forecast (Future)
5-day weather forecast.

#### POST /api/preferences (Future)
Update user preferences.

#### GET /health
Health check endpoint.

**Response Format:**
```json
{
    "status": "healthy",
    "message": "Service is running",
    "database": "connected",
    "api_keys": {
        "openweathermap": "valid"
    },
    "timestamp": "2025-01-14T15:30:00Z"
}
```

## 4. File Formats

### 4.1 Environment Configuration (.env)
```env
# Application
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
PORT=5000

# Database
DATABASE_URL=sqlite:///weather.db
# DATABASE_URL=postgresql://user:password@localhost:5432/weather_dashboard

# External APIs
OPENWEATHER_API_KEY=your-openweathermap-api-key
OPENWEATHER_BASE_URL=https://api.openweathermap.org/data/2.5

# Caching (Future)
REDIS_URL=redis://localhost:6379/0
CACHE_TYPE=redis

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/weather_dashboard.log

# Security
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
RATE_LIMIT_PER_MINUTE=60
```

### 4.2 Docker Configuration Files

#### Dockerfile
```dockerfile
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py \
    FLASK_ENV=production \
    PYTHONPATH=/app

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY . .

# Create directories
RUN mkdir -p /app/instance /app/logs

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8008/health || exit 1

EXPOSE 8008

CMD ["gunicorn", "--bind", "0.0.0.0:8008", "--workers", "4", "run:app"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8008:8008"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://weatheruser:weatherpass@db:5432/weatherdb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
      - ./instance:/app/instance
    restart: unless-stopped

  db:
    image: postgres:14-alpine
    environment:
      - POSTGRES_DB=weatherdb
      - POSTGRES_USER=weatheruser
      - POSTGRES_PASSWORD=weatherpass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init_db.sql:/docker-entrypoint-initdb.d/init_db.sql
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### 4.3 Log Format
```json
{
    "timestamp": "2025-01-14T15:30:00.123Z",
    "level": "INFO",
    "logger": "app.services.weather_service",
    "message": "Weather data retrieved successfully",
    "context": {
        "location": "New York, US",
        "duration_ms": 245,
        "api_response_time_ms": 200,
        "cache_hit": false
    },
    "request_id": "req_123456789",
    "user_id": "anonymous"
}
```

## 5. API Integration Details

### 5.1 OpenWeatherMap API

#### Current Weather Endpoint
```
GET https://api.openweathermap.org/data/2.5/weather
```

**Parameters:**
- `q`: City name (e.g., "London")
- `zip`: ZIP code with country code (e.g., "10001,US")
- `lat`: Latitude
- `lon`: Longitude
- `appid`: API key
- `units`: "imperial" or "metric"

**Response Structure:**
```json
{
    "coord": {"lon": -74.0060, "lat": 40.7128},
    "weather": [
        {
            "id": 800,
            "main": "Clear",
            "description": "clear sky",
            "icon": "01d"
        }
    ],
    "main": {
        "temp": 75.2,
        "feels_like": 77.1,
        "temp_min": 68.0,
        "temp_max": 82.0,
        "pressure": 1013,
        "humidity": 65
    },
    "visibility": 10000,
    "wind": {
        "speed": 8.5,
        "deg": 180,
        "gust": 12.3
    },
    "clouds": {"all": 10},
    "dt": 1642184400,
    "sys": {
        "country": "US",
        "sunrise": 1642156200,
        "sunset": 1642192500
    },
    "timezone": -18000,
    "id": 5128581,
    "name": "New York",
    "cod": 200
}
```

#### Forecast Endpoint (Future)
```
GET https://api.openweathermap.org/data/2.5/forecast
```

### 5.2 Rate Limiting
- **Free Plan**: 60 calls/minute, 1,000,000 calls/month
- **Paid Plan**: Available for higher usage
- **Implementation**: Redis-based rate limiting per IP address

## 6. Caching Strategy

### 6.1 Multi-Level Caching

#### Memory Cache (L1)
- **Duration**: 5 minutes per location
- **Scope**: Individual application instance
- **Storage**: Python dictionary or LRU cache

#### Redis Cache (L2)
- **Duration**: 10 minutes per location
- **Scope**: All application instances
- **Storage**: Redis hash with location as key

#### Cache Key Format
```
weather:{location}:{units}:{hash(coordinates)}
```

#### Cache Structure
```json
{
    "location": "New York, US",
    "data": {...weather_data...},
    "timestamp": "2025-01-14T15:30:00Z",
    "expires_at": "2025-01-14T15:40:00Z",
    "api_response_time_ms": 200
}
```

### 6.2 Cache Invalidation
- **Time-based**: Automatic expiration after 10 minutes
- **Manual**: Admin endpoint to clear cache for specific locations
- **Size-based**: LRU eviction when cache reaches memory limits

## 7. Security Implementation

### 7.1 API Key Management
- **Environment Variables**: Never commit to repository
- **Key Rotation**: Automated rotation every 90 days
- **Monitoring**: API key usage monitoring and alerts
- **Backup**: Encrypted backup of API keys

### 7.2 Input Validation
```python
# Location validation
def validate_location_input(location: str) -> bool:
    """Validate city name or ZIP code input"""
    # City name: letters, spaces, hyphens, apostrophes
    # ZIP code: digits, optional -+4
    city_pattern = r'^[a-zA-Z\s\-\'\.]+$'
    zip_pattern = r'^\d{5}(-\d{4})?$'
    
    return (re.match(city_pattern, location) or 
            re.match(zip_pattern, location))
```

### 7.3 Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["60 per minute", "1000 per hour"]
)

@app.route('/api/weather')
@limiter.limit("30 per minute")
def get_weather():
    # Endpoint implementation
```

### 7.4 CORS Configuration
```python
from flask_cors import CORS

# Production CORS
CORS(app, 
     origins=['https://yourdomain.com', 'https://www.yourdomain.com'],
     methods=['GET', 'POST', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'])
```

## 8. Performance Optimization

### 8.1 Database Optimization
- **Indexes**: Location, timestamp, and compound indexes
- **Query Optimization**: Use EXPLAIN ANALYZE for slow queries
- **Connection Pooling**: SQLAlchemy connection pool
- **Read Replicas**: Read queries to replica instances (future)

### 8.2 Frontend Optimization
- **Asset Minification**: CSS/JS minification
- **Image Optimization**: WebP format, lazy loading
- **CDN**: Static assets served via CDN
- **Browser Caching**: Appropriate cache headers

### 8.3 API Optimization
- **Response Compression**: gzip compression
- **Pagination**: Large result sets paginated
- **Field Selection**: Allow clients to request specific fields
- **Batch Operations**: Multiple locations in single request (future)

## 9. Monitoring & Logging

### 9.1 Application Metrics
- **Response Times**: API endpoint performance
- **Error Rates**: HTTP 5xx, API failures
- **Usage Statistics**: Daily active users, search volume
- **Database Performance**: Query times, connection usage

### 9.2 Log Aggregation
```python
import structlog

# Structured logging
logger = structlog.get_logger()

logger.info(
    "Weather request processed",
    location=location,
    response_time_ms=duration,
    cache_hit=cache_hit,
    status_code=200
)
```

### 9.3 Health Checks
- **Application Health**: /health endpoint
- **Database Health**: Connection and query performance
- **External API Health**: OpenWeatherMap API status
- **Infrastructure Health**: CPU, memory, disk usage

## 10. Deployment Architecture

### 10.1 Production Environment
```
Internet
    │
    ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Nginx    │    │   Flask     │    │ PostgreSQL  │
│  (Web/SSL)  │◄──►│  (App/4x)   │◄──►│ (Database)  │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    Redis    │
                    │   (Cache)   │
                    └─────────────┘
```

### 10.2 Deployment Strategy
- **Blue-Green Deployment**: Zero downtime deployments
- **Rolling Updates**: Gradual pod updates
- **Health Checks**: Automated health verification
- **Rollback**: Automatic rollback on failures

### 10.3 Infrastructure Requirements
- **Minimum**: 2 vCPU, 4GB RAM, 50GB SSD
- **Recommended**: 4 vCPU, 8GB RAM, 100GB SSD
- **Database**: Separate instance, 2 vCPU, 4GB RAM
- **Cache**: Redis instance, 1 vCPU, 2GB RAM

## 11. Testing Strategy

### 11.1 Test Types
- **Unit Tests**: Individual function testing (pytest)
- **Integration Tests**: API endpoint testing
- **End-to-End Tests**: Full user journey testing
- **Performance Tests**: Load and stress testing

### 11.2 Test Coverage
- **Target**: 90%+ code coverage
- **Critical Path**: 100% coverage for core weather functionality
- **Security**: Input validation and authentication testing
- **Accessibility**: WCAG compliance testing

### 11.3 Continuous Testing
- **Pre-commit Hooks**: Local test execution
- **CI Pipeline**: Automated testing on every commit
- **Staging Environment**: Production-like testing environment
- **Monitoring**: Test execution metrics and trends

## 12. Future Enhancements

### 12.1 Technology Roadmap
- **GraphQL API**: Alternative to REST API
- **WebSocket**: Real-time weather updates
- **Microservices**: Separate weather and user services
- **Machine Learning**: Weather prediction models

### 12.2 Scalability Planning
- **Horizontal Scaling**: Load balancer with multiple instances
- **Database Sharding**: Geographic data distribution
- **CDN Integration**: Global content delivery
- **Edge Computing**: Cloudflare Workers for API calls

### 12.3 Feature Pipeline
- **User Accounts**: Authentication and profiles
- **Mobile Apps**: iOS and Android applications
- **API v2**: Enhanced API with more features
- **Third-party Integrations**: Smart home, calendars