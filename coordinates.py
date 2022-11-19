from geopy.geocoders import Nominatim
from geopy.distance import geodesic as geodist


class GetCords:
    def __init__(self, address, language='ru'):
        geolocator = Nominatim(user_agent="crd")
        self.cords = geolocator.geocode(address, language=language)


class GetAddress:
    def __init__(self, location, language='ru'):
        geolocator = Nominatim(user_agent='adr')
        self.address = geolocator.reverse(location, language=language)
        self.raw_address = geolocator.reverse(location, language=language).raw


class GetDistanceBetween:
    def __init__(self, locationFrom, locationTo):
        self.distance = geodist(locationFrom, locationTo).km
