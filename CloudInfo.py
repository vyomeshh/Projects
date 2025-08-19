import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextBrowser, QProgressDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import datetime

API_KEY = '39e31d7e0a00a42c380d2895aa5f5937'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
ONE_CALL_API_URL = "https://api.openweathermap.org/data/2.5/onecall"


class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CloudInfo🌦️")
        self.setGeometry(100, 100, 800, 400)

        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("QTabBar::tab { height: 50px; width: 200px; font-size: 16px; }")

        tab_widget = QTabWidget(self)
        tab_widget.setGeometry(10, 10, 780, 380)

        # Tab for a single city
        city_tab = QWidget()
        tab_widget.addTab(city_tab, "City Weather")

        city_layout = QVBoxLayout()
        city_tab.setLayout(city_layout)

        city_label = QLabel("City Name:")
        self.city_entry = QLineEdit()
        self.city_entry.setPlaceholderText("Enter city name")
        get_weather_button = QPushButton("Get Weather")
        get_weather_button.clicked.connect(self.get_city_weather)
        self.weather_label = QTextBrowser()

        city_layout.addWidget(city_label)
        city_layout.addWidget(self.city_entry)
        city_layout.addWidget(get_weather_button)
        city_layout.addWidget(self.weather_label)

        # Tab for comparing two cities
        compare_tab = QWidget()
        tab_widget.addTab(compare_tab, "Compare Weather")

        compare_layout = QVBoxLayout()
        compare_tab.setLayout(compare_layout)

        city1_label = QLabel("City 1:")
        self.city1_entry = QLineEdit()
        city2_label = QLabel("City 2:")
        self.city2_entry = QLineEdit()
        compare_button = QPushButton("Compare")
        compare_button.clicked.connect(self.compare_cities)
        self.compare_label = QTextBrowser()

        compare_layout.addWidget(city1_label)
        compare_layout.addWidget(self.city1_entry)
        compare_layout.addWidget(city2_label)
        compare_layout.addWidget(self.city2_entry)
        compare_layout.addWidget(compare_button)
        compare_layout.addWidget(self.compare_label)

        # Connect returnPressed signal to functions
        self.city_entry.returnPressed.connect(self.get_city_weather)
        self.city1_entry.returnPressed.connect(self.compare_cities)
        self.city2_entry.returnPressed.connect(self.compare_cities)

    def get_city_weather(self):
        city = self.city_entry.text()
        if not city:
            return
        self.show_loading_dialog()
        self.worker = WeatherWorker(city)
        self.worker.resultReceived.connect(self.handle_city_weather)
        self.worker.start()

    def handle_city_weather(self, weather_data):
        self.hide_loading_dialog()
        if weather_data:
            self.weather_label.setHtml(weather_data)

    def compare_cities(self):
        city1 = self.city1_entry.text()
        city2 = self.city2_entry.text()
        if not city1 or not city2:
            return
        self.show_loading_dialog()
        self.worker = WeatherComparisonWorker(city1, city2)
        self.worker.resultReceived.connect(self.handle_comparison)
        self.worker.start()

    def handle_comparison(self, comparison_text):
        self.hide_loading_dialog()
        if comparison_text:
            self.compare_label.setHtml(comparison_text)
        else:
            self.compare_label.setPlainText("Error: Invalid cities")

    def show_loading_dialog(self):
        self.loading_dialog = QProgressDialog("Fetching Weather Data...", None, 0, 0, self)
        self.loading_dialog.setWindowModality(Qt.WindowModal)
        self.loading_dialog.show()

    def hide_loading_dialog(self):
        if hasattr(self, 'loading_dialog'):
            self.loading_dialog.close()


class WeatherWorker(QThread):
    resultReceived = pyqtSignal(str)

    def __init__(self, city):
        super().__init__()
        self.city = city

    def run(self):
        weather_data = fetch_weather(self.city)
        self.resultReceived.emit(weather_data)


class WeatherComparisonWorker(QThread):
    resultReceived = pyqtSignal(str)

    def __init__(self, city1, city2):
        super().__init__()
        self.city1 = city1
        self.city2 = city2

    def run(self):
        comparison_data1 = fetch_weather(self.city1)
        comparison_data2 = fetch_weather(self.city2)
        if comparison_data1 and comparison_data2:
            comparison_text = (
                f"<html>"
                f"<head>"
                f"<style>"
                f"body {{ font-family: 'Arial', sans-serif; margin: 10px; padding: 0; }}"
                f"b {{ color: #007BFF; }}"
                f"</style>"
                f"</head>"
                f"<body>"
                f"<b>City 1 Weather Information:</b><br>{comparison_data1}<br>"
                f"{get_weather_icon(comparison_data1)}"
                f"<br><b>City 2 Weather Information:</b><br>{comparison_data2}<br>"
                f"{get_weather_icon(comparison_data2)}"
                f"</body>"
                f"</html>"
            )
            self.resultReceived.emit(comparison_text)
        else:
            self.resultReceived.emit("Error: Invalid cities")


def fetch_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if 'name' in data:
        city_name = data['name']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        weather_description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        visibility = data.get('visibility', 'N/A')
        pressure = data['main']['pressure']

        weather_info = (
            f"<b>City:</b> {city_name}<br>"
            f"<b>Temperature:</b> {temperature}°C<br>"
            f"<b>Feels Like:</b> {feels_like}°C<br>"
            f"<b>Weather:</b> {weather_description}<br>"
            f"<b>Humidity:</b> {humidity}%<br>"
            f"<b>Wind Speed:</b> {wind_speed} m/s<br>"
            f"<b>Visibility:</b> {visibility} meters<br>"
            f"<b>Pressure:</b> {pressure} hPa"
        )

        return weather_info
    else:
        return "Weather data not available."


def get_weather_icon(weather_data):
    # Map weather conditions to local image files
    icon_mapping = {
        'Clear': 'clear.png',
        'Clouds': 'cloud.png',
        'Rain': 'rain.png',
        'Drizzle': 'drizzle.png',
        'Thunderstorm': 'thunderstorm.png',
        'Snow': 'snow.png',
        'Mist': 'mist.png'
    }

    weather_condition = weather_data.split("<br>")[3].split(":")[1].strip()
    icon_path = os.path.join(os.path.dirname(__file__), 'icons', icon_mapping.get(weather_condition, 'question.png'))

    # Check if the icon file exists in the local folder
    if os.path.exists(icon_path):
        # Load the icon from the local folder
        pixmap = QPixmap(icon_path)
        pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio)
        icon_html = f"<img src='data:image/png;base64,{pixmap.toImage().toData().toBase64().data().decode()}'></img>"
    else:
        # If the local icon file is not found, display a placeholder image
        icon_html = "<img src='path/to/placeholder.png'></img>"

    return icon_html
def main():
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
