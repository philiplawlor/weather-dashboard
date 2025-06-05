from app import create_app
from app.models import db, WeatherData, ForecastData

def run_migrations():
    app = create_app()
    with app.app_context():
        # This will create all tables that don't exist yet
        db.create_all()
        print("Database migrations completed successfully!")

if __name__ == '__main__':
    run_migrations()
