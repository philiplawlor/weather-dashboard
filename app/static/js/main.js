// Main JavaScript for Weather Dashboard
document.addEventListener('DOMContentLoaded', function() {
    // Initialize elements
    const weatherForm = document.getElementById('weatherForm');
    const cityInput = document.getElementById('cityInput');
    const currentWeather = document.getElementById('currentWeather');
    const errorMessage = document.getElementById('errorMessage');
    const weatherHistory = document.getElementById('weatherHistory');
    const noHistory = document.getElementById('noHistory');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const beachInfo = document.getElementById('beachInfo');
    const refreshBeachData = document.getElementById('refreshBeachData');
    
    // Store current coordinates for tide data
    let currentCoords = null;
    
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

    // Fetch beach and tide data
    async function fetchBeachData(lat, lon) {
        if (!lat || !lon) return;
        
        try {
            const response = await fetch(`/api/beach?lat=${lat}&lng=${lon}`);
            const data = await response.json();
            
            if (data.status === 'success') {
                displayBeachData(data.data);
            } else {
                console.error('Error fetching beach data:', data.message);
            }
        } catch (error) {
            console.error('Error fetching beach data:', error);
        }
    }
    
    // Display beach and tide data
    function displayBeachData(data) {
        if (!data) return;
        
        const tideInfo = document.getElementById('tideInfo');
        const waterTemp = document.getElementById('waterTemp');
        const waveHeight = document.getElementById('waveHeight');
        const swellPeriod = document.getElementById('swellPeriod');
        
        // Update tide information
        if (data.tides && data.tides.data && data.tides.data.length > 0) {
            const tides = data.tides.data;
            let tideHtml = `
                <div class="row justify-content-around">
                    <div class="col-md-6">
                        <div class="h6">Next High Tide</div>
                        <div class="h4 text-primary">${formatTideTime(tides.find(t => t.type === 'high')?.time) || '--'}</div>
                    </div>
                    <div class="col-md-6">
                        <div class="h6">Next Low Tide</div>
                        <div class="h4 text-primary">${formatTideTime(tides.find(t => t.type === 'low')?.time) || '--'}</div>
                    </div>
                </div>
            `;
            tideInfo.innerHTML = tideHtml;
        }
        
        // Update beach conditions
        if (data.conditions && data.conditions.hours && data.conditions.hours.length > 0) {
            const latest = data.conditions.hours[0];
            
            if (latest.waterTemperature) {
                waterTemp.textContent = `${Math.round(latest.waterTemperature.noaa * 1.8 + 32)}°F`;
            }
            
            if (latest.waveHeight) {
                waveHeight.textContent = `${latest.waveHeight.noaa.toFixed(1)} ft`;
            }
            
            if (latest.swellPeriod) {
                swellPeriod.textContent = `${latest.swellPeriod.noaa.toFixed(1)} s`;
            }
        }
        
        // Show the beach info section
        beachInfo.classList.remove('d-none');
    }
    
    // Format tide time
    function formatTideTime(timestamp) {
        if (!timestamp) return '--';
        const date = new Date(timestamp);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    // Fetch weather data from the API
    async function fetchWeather(location) {
        showLoading(true);
        showError(''); // Clear any previous errors
        
        // Hide beach info until new data is loaded
        if (beachInfo) {
            beachInfo.classList.add('d-none');
        }
        
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
        if (!data || data.cod !== 200) {
            showError('Unable to fetch weather data. Please try again.');
            return;
        }
        
        // Update the UI with weather data
        document.getElementById('location').textContent = `${data.name}, ${data.sys.country}`;
        document.getElementById('temperature').textContent = `${Math.round(data.main.temp)}°F`;
        document.getElementById('weatherDescription').textContent = data.weather[0].description;
        document.getElementById('humidity').textContent = `${data.main.humidity}%`;
        document.getElementById('feelsLike').textContent = `${Math.round(data.main.feels_like)}°F`;
        
        // Set weather icon
        const iconCode = data.weather[0].icon;
        const iconUrl = `http://openweathermap.org/img/wn/${iconCode}@2x.png`;
        document.getElementById('weatherIcon').src = iconUrl;
        
        // Show the weather section and hide loading spinner
        currentWeather.classList.remove('d-none');
        showLoading(false);
        
        // Save to history
        saveToHistory(data);
        
        // Store coordinates for beach data
        currentCoords = {
            lat: data.coord.lat,
            lon: data.coord.lon
        };
        
        // Fetch beach and tide data
        fetchBeachData(data.coord.lat, data.coord.lon);
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
