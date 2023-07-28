import requests


def what_weather(city):
    url = f'https://wttr.in/{city}'
    weather_parameters = {
        'format': 2,
        'M': ''
    }

    try:
        response = requests.get(url, params=weather_parameters, verify=False)
    except requests.ConnectionError:
        return '<error> – сетевая ошибка'

    if response.status_code == 200:
        return response.text
    else:
        return '<error> – город не найден'
