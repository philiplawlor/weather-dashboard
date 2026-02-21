// Main JavaScript for Weather Dashboard
console.log('Weather Dashboard JavaScript loaded');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');
    
    // Initialize elements
    const weatherForm = document.getElementById('weatherForm');
    const cityInput = document.getElementById('cityInput');
    const currentWeather = document.getElementById('currentWeather');
    const errorMessage = document.getElementById('errorMessage');
    const weatherHistory = document.getElementById('weatherHistory');
    const noHistory = document.getElementById('noHistory');
    const loadingSpinner = document.getElementById('loadingSpinner');
    
    // Debug: Log element status
    console.log('Form element:', weatherForm ? 'Found' : 'Not found');
    console.log('City input:', cityInput ? 'Found' : 'Not found');
    console.log('Current weather div:', currentWeather ? 'Found' : 'Not found');
    console.log('Error message div:', errorMessage ? 'Found' : 'Not found');
    console.log('Weather history div:', weatherHistory ? 'Found' : 'Not found');

    // Load weather history on page load
    loadWeatherHistory();

    // Handle form submission
    if (weatherForm) {
        console.log('Adding form submit event listener');
        weatherForm.addEventListener('submit', function(e) {
            console.log('Form submitted');
            e.preventDefault();
            const location = cityInput ? cityInput.value.trim() : '';
            console.log('Location input value:', location);
            
            if (!location) {
                console.error('No location entered');
                showError('Please enter a city name or ZIP code');
                return;
            }
            
            console.log('Fetching weather for location:', location);
            fetchWeather(location);
        });
    } else {
        console.error('Weather form not found in the DOM');
    }

    // Fetch weather data from the API
    async function fetchWeather(location) {
        showLoading(true);
        showError(''); // Clear any previous errors
        
        // Check if the input is a ZIP code (US only for now)
        const isZipCode = /^\d{5}(-\d{4})?$/.test(location);
        const endpoint = isZipCode ? 
            `/api/weather?zip=${encodeURIComponent(location)}` : 
            `/api/weather?city=${encodeURIComponent(location)}`;
        
        console.log(`Fetching weather from: ${endpoint}`);
        
        try {
            const response = await fetch(endpoint);
            const data = await response.json();
            
            console.log('API Response:', data);
            
            if (!response.ok) {
                const errorMsg = data.message || 'Failed to fetch weather data';
                throw new Error(errorMsg);
            }
            
            if (data.status === 'success') {
                displayWeather(data.data);
                loadWeatherHistory(); // Reload history after new search
            } else {
                throw new Error(data.message || 'Failed to process weather data');
            }
        } catch (error) {
            console.error('Error fetching weather:', error);
            showError(`Error: ${error.message || 'Failed to fetch weather data. Please try again.'}`);
        } finally {
            showLoading(false);
        }
    }

    // Display weather data
    function displayWeather(data) {
        if (!data) return;
        
        // Update DOM elements
        document.getElementById('location').textContent = data.location || 'N/A';
        document.getElementById('temperature').innerHTML = data.temperature ? `${Math.round(data.temperature)}&deg;F` : 'N/A';
        document.getElementById('weatherDescription').textContent = data.description || 'N/A';
        document.getElementById('humidity').textContent = data.humidity ? `${data.humidity}%` : 'N/A';
        document.getElementById('feelsLike').textContent = data.temperature ? `${Math.round(data.temperature)}°F` : 'N/A';
        
        // Set weather icon if available
        const weatherIcon = document.getElementById('weatherIcon');
        if (weatherIcon && data.icon) {
            weatherIcon.src = `http://openweathermap.org/img/wn/${data.icon}@2x.png`;
            weatherIcon.alt = data.description || 'Weather icon';
            weatherIcon.style.display = 'block';
        } else if (weatherIcon) {
            weatherIcon.style.display = 'none';
        }

        // Show weather card and hide error
        if (currentWeather) currentWeather.classList.remove('d-none');
        if (errorMessage) errorMessage.classList.add('d-none');
    }

    // Show error message
    function showError(message) {
        if (!message) {
            if (errorMessage) {
                errorMessage.textContent = '';
                errorMessage.style.display = 'none';
            }
            return;
        }
        
        console.error('Showing error:', message);
        
        if (errorMessage) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';
            
            // Hide error after 5 seconds
            setTimeout(() => {
                errorMessage.style.display = 'none';
            }, 5000);
        } else {
            console.error('Error message element not found');
        }
    }

    // Load weather history
    async function loadWeatherHistory() {
        try {
            const response = await fetch('/api/weather/history');
            const data = await response.json();
            
            if (data.status === 'success' && data.data.length > 0) {
                renderWeatherHistory(data.data);
            } else {
                showNoHistory();
            }
        } catch (error) {
            console.error('Error loading history:', error);
            showNoHistory();
        }
    }

    // Render weather history
    function renderWeatherHistory(history) {
        if (!weatherHistory) return;
        
        weatherHistory.innerHTML = '';
        
        history.forEach(item => {
            const date = new Date(item.timestamp);
            const timeString = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            
            const historyItem = document.createElement('a');
            historyItem.href = '#';
            historyItem.className = 'list-group-item list-group-item-action';
            historyItem.innerHTML = `
                <div class="d-flex w-100 justify-content-between">
                    <h5 class="mb-1">${item.location || 'Unknown Location'}</h5>
                    <small>${timeString}</small>
                </div>
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <span class="h4 mb-0">${item.temperature ? Math.round(item.temperature) + '°F' : 'N/A'}</span>
                        <small class="text-muted ms-2">${item.description || ''}</small>
                    </div>
                    ${item.icon ? `<img src="http://openweathermap.org/img/wn/${item.icon}.png" alt="${item.description || ''}" class="weather-history-icon">` : ''}
                </div>`;
            
            // Add click event to search for this location again
            historyItem.addEventListener('click', (e) => {
                e.preventDefault();
                if (item.location) {
                    cityInput.value = item.location.split(',')[0].trim();
                    weatherForm.dispatchEvent(new Event('submit'));
                }
            });
            
            weatherHistory.appendChild(historyItem);
        });
        
        if (noHistory) noHistory.classList.add('d-none');
    }

    // Show no history message
    function showNoHistory() {
        if (weatherHistory) weatherHistory.innerHTML = '';
        if (noHistory) noHistory.classList.remove('d-none');
    }

    // Show/hide loading spinner
    function showLoading(show) {
        const submitBtn = weatherForm ? weatherForm.querySelector('button[type="submit"]') : null;
        
        if (submitBtn) {
            if (show) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
            } else {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="bi bi-search"></i> Get Weather';
            }
        }
    }
});
