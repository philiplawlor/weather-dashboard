# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2025-06-22

### Added
- Dark mode toggle with user preference persistence
- System preference detection for automatic theme selection
- Smooth transitions between light and dark themes
- Enhanced UI components for dark mode compatibility
- CSS variables for consistent theming

## [0.2.1] - 2025-06-22

### Added
- Docker support with multi-stage builds
- Docker Compose configuration for easy local development
- Entrypoint script for database initialization
- Health check endpoint at `/health`
- Windows compatibility improvements

### Changed
- Updated server port from 5000 to 8008
- Improved error handling and logging
- Updated documentation for Docker deployment

### Fixed
- Database initialization in container
- File permission issues in Docker
- Line ending handling for Windows compatibility
