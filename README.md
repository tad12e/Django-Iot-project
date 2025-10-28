# IoT Appliance Monitoring System

A full-stack IoT system for real-time monitoring of electrical appliances with secure data logging, visualization, and alert capabilities.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![Arduino](https://img.shields.io/badge/Arduino-C++-orange.svg)
![IoT](https://img.shields.io/badge/IoT-Platform-yellow.svg)

## 🚀 Features

### Hardware Layer
- **Arduino-based sensors** monitoring appliance usage
- **Real-time data serialization** to JSON payloads
- **HTTP communication** with secure backend API
- **Multiple sensor support** (current, voltage, power consumption)

### Backend Services
- **Django REST API** with CSRF protection
- **Secure user authentication** with email verification
- **Data validation** and logging pipeline
- **SQLite/PostgreSQL database** for data storage

### Frontend Dashboard
- **Real-time analytics** with interactive charts
- **Responsive design** using Tailwind CSS
- **Appliance status monitoring**
- **Historical data visualization**

## 🛠️ Tech Stack

**Hardware:** Arduino Uno, Current Sensors, WiFi Module

**Backend:** Django, Django REST Framework, SQLite/PostgreSQL, Python

**Frontend:** HTML5, Tailwind CSS, JavaScript, Chart.js

**Communication:** HTTP/REST APIs, JSON Serialization

## 📋 Prerequisites

- Python 3.8+
- Arduino IDE
- Django 4.2

## ⚡ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/tad12e/Django-Iot-project.git
cd Django-Iot-project
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Database setup
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### 3. Arduino Setup
1. Open `arduino/sensor_node.ino` in Arduino IDE
2. Install required libraries:
   - WiFi library for your module (ESP8266/ESP32)
   - ArduinoJSON library
3. Configure WiFi credentials in `config.h`
4. Upload to Arduino board

## 🔧 Project Structure
```
Django-Iot-project/
├── iot_app/                 # Django main application
│   ├── models.py           # Database models
│   ├── views.py            # API views and dashboard
│   ├── urls.py             # URL routing
│   └── templates/          # HTML templates
├── arduino/                # Hardware code
│   ├── sensor_node.ino     # Main Arduino sketch
│   └── config.h            # WiFi configuration
├── requirements.txt        # Python dependencies
└── manage.py              # Django management script
```

## 🎯 Usage

### 1. User Registration
- Visit `/register` to create account
- Complete email verification process
- Login to access dashboard

### 2. Device Setup
- Connect Arduino to power and network
- Device automatically registers with backend
- View connected devices in admin panel

### 3. Data Monitoring
- Real-time data appears on dashboard
- View historical trends and analytics
- Set up alerts for abnormal consumption

### API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/data/` | Submit sensor data |
| GET | `/api/devices/` | List user devices |
| GET | `/api/analytics/` | Get consumption analytics |
| POST | `/api/alerts/` | Configure alert thresholds |

## 🔌 Hardware Configuration

### Components Required
- Arduino Uno/ESP32
- ACS712 Current Sensor (20A)
- WiFi Module (ESP8266/ESP32)
- Breadboard and Jumper Wires

### Circuit Diagram
```
+5V ────╔═══════╗─── Analog A0
        ║ ACS712║
GND ────╚═══════╝─── Load
```

### Sensor Calibration
```cpp
// Current sensor calibration
float sensitivity = 0.100; // 100mV/A for ACS712-20A
float offset = 2.5; // Vcc/2
float current = (sensorValue - offset) / sensitivity;
```

## 📊 Data Flow

```
Arduino Sensor → JSON Serialization → HTTP POST → Django Backend
     ↓
Data Validation → Database Storage → Real-time Dashboard
     ↓
User Authentication ← Email Verification ← Registration
```

## 🔒 Security Features

- **CSRF Protection** on all POST endpoints
- **User authentication** and session management
- **Email verification** for new accounts
- **Data validation** and sanitization

## 🚀 Deployment

### Backend Deployment (Heroku)
```bash
# Install Heroku CLI
heroku create your-iot-app
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set DEBUG=False
git push heroku main
```

## 📈 Performance Metrics

- **Data transmission interval**: 5-10 seconds
- **API response time**: < 200ms
- **Concurrent device support**: 10+ devices
- **Data retention**: 30 days (configurable)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Tadiwos Tamene**
- Email: tadiwosgetahun49@gmail.com
- GitHub: [@tad12e](https://github.com/tad12e)
- LinkedIn: [Tadiwos Tamene](https://linkedin.com/in/tadiwos-tamene)

## 🙏 Acknowledgments

- Addis Ababa University Electrical and Computer Engineering Department
- Django Software Foundation
- Arduino community for hardware libraries and support

---

**⭐ Star this repo if you find it helpful!**
```
