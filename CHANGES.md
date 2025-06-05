# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- 🌊 Beach and tide information section
  - Integration with StormGlass API for marine data
  - Display of high and low tide times
  - Water temperature, wave height, and swell period information
  - Refresh button for updating marine data
- GitHub repository setup and initial push
- Comprehensive README with badges and project information
- Detailed CHANGES.md for version history
- Run scripts for both Windows and Unix-based systems
- About page with project information and GitHub link

### Changed
- Updated documentation with installation and setup instructions
- Improved error handling in run scripts
- Enhanced UI with better navigation and GitHub link
- Weather display now includes coordinates for beach data lookup

## [0.1.0] - 2025-06-05
### Added
- Complete Flask application structure with blueprints
- OpenWeatherMap API integration with error handling
- Responsive frontend using Bootstrap 5
- Weather data display with icons and descriptions
- Search functionality by city name and ZIP code
- Temperature display in Fahrenheit
- Search history with local storage
- Error handling and user feedback
- Environment variable configuration
- SQLite database for search history
- Comprehensive documentation

### Changed
- Updated API endpoint to support both city and ZIP code searches
- Improved error handling and user feedback
- Enhanced UI/UX with better responsive design
- Switched temperature units to Fahrenheit

### Fixed
- Resolved API key loading issues
- Fixed ZIP code search functionality
- Addressed various UI/UX issues
