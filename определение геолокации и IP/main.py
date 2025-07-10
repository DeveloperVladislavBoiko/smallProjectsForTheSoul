import requests


def get_user_geolocation(api_key=None):
    """
    Определяет приблизительную геолокацию пользователя по его публичному IP-адресу.

    Параметры:
        api_key (str, optional): Ключ API для сервиса ipinfo.io (необязательно, но с ним больше запросов).

    Возвращает:
        dict: Словарь с данными о местоположении (город, страна, координаты и т. д.).
        None: В случае ошибки.
    """
    try:
        url = "https://ipinfo.io/json"
        params = {}
        if api_key:
            params["token"] = api_key

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()  # Проверка на ошибки HTTP

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


location = get_user_geolocation()  # Можно передать API-ключ, если есть
if location:
    print("Геолокация определена:")
    print(f"IP: {location.get('ip')}")
    print(f"Город: {location.get('city')}")
    print(f"Страна: {location.get('country')}")
    print(f"Координаты: {location.get('latitude')}, {location.get('longitude')}")
else:
    print("Не удалось определить геолокацию.")
