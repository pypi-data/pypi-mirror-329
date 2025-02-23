import requests

def get_weather_data(place, api_key=None):
    with requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={place}&appid={api_key}') as response:
        if response.status_code == 200:
            data = response.json()  # Получаем JSON-ответ
            
            # Формируем новый словарь с нужными данными
            result = {
                "name": data.get("name"),
                "coord": data.get("coord"),
                "country": data.get("sys", {}).get("country"),
                "feels_like": data.get("main", {}).get("feels_like"),
                "timezone": f"UTC+{data.get('timezone', 0) // 3600}"  # Преобразуем смещение в UTC
            }
            return result
        else:
            # Если запрос неудачен, возвращаем ошибку
            return {"error": f"Ошибка {response.status_code}: {response.text}"}

