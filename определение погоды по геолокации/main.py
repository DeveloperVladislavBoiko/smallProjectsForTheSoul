import requests
from datetime import datetime


"""
программа определяет погоду по заданным координатам, отдельная функция находит их, формирует текстовый файл с погодными условиями.
В случае успешного формирования отчета о погоде возвращает True, иначе False, программа требует подключения к интернету
"""

def get_user_geolocation(api_key=None):
    """
    Определяет приблизительную геолокацию пользователя по его публичному IP-адресу.
    """
    try:
        url = "https://ipinfo.io/json"
        params = {}
        if api_key:
            params["token"] = api_key

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()

        if "loc" in data:
            lat, lon = data["loc"].split(",")
            data["latitude"] = float(lat)
            data["longitude"] = float(lon)

        return data

    except requests.exceptions.RequestException as e:
        return None
    except Exception as e:
        return None


def get_weather(latitude, longitude):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&hourly=weathercode"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        current_weather = data.get('current_weather', {})
        weather_code = current_weather.get('weathercode', None)

        weather_conditions = get_weather_conditions(weather_code)

        return {
            'temperature': current_weather.get('temperature'),
            'windspeed': current_weather.get('windspeed'),
            'winddirection': current_weather.get('winddirection'),
            'conditions': weather_conditions
        }
    except Exception as e:
        return None


def get_weather_conditions(weather_code):
    if weather_code is None:
        return None

    weather_map = {
        0: "ясно",
        1: "преимущественно ясно",
        2: "переменная облачность",
        3: "пасмурно",
        45: "туман",
        48: "туман с инеем",
        51: "морось",
        53: "умеренная морось",
        55: "сильная морось",
        56: "ледяная морось",
        57: "сильная ледяная морось",
        61: "слабый дождь",
        63: "умеренный дождь",
        65: "сильный дождь",
        66: "ледяной дождь",
        67: "сильный ледяной дождь",
        71: "слабый снег",
        73: "умеренный снег",
        75: "сильный снег",
        77: "град",
        80: "слабые ливни",
        81: "умеренные ливни",
        82: "сильные ливни",
        85: "снежные ливни",
        86: "сильные снежные ливни",
        95: "гроза",
        96: "гроза со слабым градом",
        99: "гроза с сильным градом"
    }

    return weather_map.get(weather_code, None)


def save_weather_report(api_key=None, filename="weather_report.txt"):
    """
    Главная функция: получает геолокацию, погоду и сохраняет в файл
    """
    geo = get_user_geolocation(api_key)
    if not geo or 'latitude' not in geo or 'longitude' not in geo:
        return False

    weather = get_weather(geo['latitude'], geo['longitude'])
    if not weather:
        return False

    # Округляем значения
    temperature = round(weather.get('temperature', 0))
    wind_speed = round(weather.get('windspeed', 0))

    city = geo.get('city', 'Неизвестно')
    temp_sign = "+" if temperature >= 0 else ""
    conditions = weather.get('conditions')

    report_lines = [
        f"в городе {city}",
        f"{temp_sign}{temperature}",
        f"ветер {wind_speed} км в час"
    ]

    if conditions:
        report_lines.append(conditions)

    report = "\n".join(report_lines)

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        return True
    except Exception as e:
        return False

if save_weather_report():
    print("Отчет о погоде сохранен в файле")
else :
    print("Ошибка в работе программы")
