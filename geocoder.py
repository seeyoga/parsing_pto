from geopy import GoogleV3


def geocoder(place: str, api_key: str) -> list:
    """ Функция для получения координат по адресу """
    location = GoogleV3(api_key=api_key, timeout=5).geocode(place)
    return [location.latitude, location.longitude]
