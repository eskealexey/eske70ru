// weather.js
class WeatherWidget {
    constructor() {
        this.apiKey = '59bdb9972b4f4e4972d35cea19ffb337'; // Получите бесплатный ключ на openweathermap.org
        this.city = 'Volgograd';
        this.units = 'metric';
        this.lang = 'ru';

        this.init();
    }

    init() {
        this.bindEvents();
        this.loadWeather();
    }

    bindEvents() {
        document.getElementById('refresh-btn').addEventListener('click', () => {
            this.loadWeather();
        });
    }

    async loadWeather() {
        try {
            this.showLoading();

            // Текущая погода
            const currentWeather = await this.fetchWeather();
            this.displayCurrentWeather(currentWeather);

            // Прогноз на 5 дней
            const forecast = await this.fetchForecast();
            this.displayForecast(forecast);

            this.hideError();
        } catch (error) {
            console.error('Ошибка загрузки погоды:', error);
            this.showError();
        }
    }

    async fetchWeather() {
        const url = `https://api.openweathermap.org/data/2.5/weather?q=${this.city}&units=${this.units}&lang=${this.lang}&appid=${this.apiKey}`;

        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Weather data not available');
        }

        return await response.json();
    }

    async fetchForecast() {
        const url = `https://api.openweathermap.org/data/2.5/forecast?q=${this.city}&units=${this.units}&lang=${this.lang}&appid=${this.apiKey}`;

        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Forecast data not available');
        }

        return await response.json();
    }

    displayCurrentWeather(data) {
        document.getElementById('city-name').textContent = data.name;
        document.getElementById('temp').textContent = Math.round(data.main.temp);
        document.getElementById('humidity').textContent = `${data.main.humidity}%`;
        document.getElementById('wind').textContent = `${data.wind.speed} м/с`;
        document.getElementById('description').textContent = this.capitalizeFirstLetter(data.weather[0].description);

        const iconCode = data.weather[0].icon;
        document.getElementById('weather-icon').src = `https://openweathermap.org/img/wn/${iconCode}@2x.png`;
        document.getElementById('weather-icon').alt = data.weather[0].description;
    }

    displayForecast(data) {
        const forecastContainer = document.getElementById('forecast');
        forecastContainer.innerHTML = '';

        // Берем по одному прогнозу в день (каждые 24 часа)
        const dailyForecasts = data.list.filter((item, index) => index % 8 === 0).slice(0, 5);

        dailyForecasts.forEach(forecast => {
            const date = new Date(forecast.dt * 1000);
            const dayElement = document.createElement('div');
            dayElement.className = 'forecast-day';

            dayElement.innerHTML = `
                <div class="forecast-date">${this.formatDate(date)}</div>
                <div class="forecast-icon">
                    <img src="https://openweathermap.org/img/wn/${forecast.weather[0].icon}.png" alt="${forecast.weather[0].description}">
                </div>
                <div class="forecast-temp">${Math.round(forecast.main.temp)}°</div>
            `;

            forecastContainer.appendChild(dayElement);
        });
    }

    formatDate(date) {
        return date.toLocaleDateString('ru-RU', {
            weekday: 'short',
            day: 'numeric',
            month: 'short'
        });
    }

    capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    showLoading() {
        document.getElementById('city-name').textContent = 'Загрузка...';
        document.getElementById('temp').textContent = '--';
    }

    showError() {
        document.getElementById('error-message').style.display = 'block';
    }

    hideError() {
        document.getElementById('error-message').style.display = 'none';
    }
}

// Упрощенная версия без API (для демонстрации)
class DemoWeatherWidget extends WeatherWidget {
    async fetchWeather() {
        // Имитация задержки сети
        await new Promise(resolve => setTimeout(resolve, 1000));

        return {
            name: 'Москва',
            main: {
                temp: 15,
                humidity: 65
            },
            wind: {
                speed: 3.5
            },
            weather: [{
                description: 'легкая облачность',
                icon: '02d'
            }]
        };
    }

    async fetchForecast() {
        await new Promise(resolve => setTimeout(resolve, 500));

        const baseDate = new Date();
        return {
            list: [
                { dt: baseDate.getTime() / 1000 + 86400, main: { temp: 16 }, weather: [{ icon: '01d' }] },
                { dt: baseDate.getTime() / 1000 + 172800, main: { temp: 18 }, weather: [{ icon: '02d' }] },
                { dt: baseDate.getTime() / 1000 + 259200, main: { temp: 14 }, weather: [{ icon: '10d' }] },
                { dt: baseDate.getTime() / 1000 + 345600, main: { temp: 12 }, weather: [{ icon: '09d' }] },
                { dt: baseDate.getTime() / 1000 + 432000, main: { temp: 17 }, weather: [{ icon: '01d' }] }
            ]
        };
    }
}

// Запуск виджета
document.addEventListener('DOMContentLoaded', () => {
    // Используйте DemoWeatherWidget для демо или WeatherWidget с реальным API ключом
//    new DemoWeatherWidget();
     new WeatherWidget(); // Раскомментируйте для использования реального API
});
