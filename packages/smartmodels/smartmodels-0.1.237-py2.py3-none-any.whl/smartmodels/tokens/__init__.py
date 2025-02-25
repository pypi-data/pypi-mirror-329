# tokens
# TODO: split into several files as the number of tokens grow

from enum import Enum


class StrEnum(str, Enum):
    """Enum where members are also (and must be) str"""


class NAMESPACES(StrEnum):
    COMFORT = "comfort"
    CONSUMPTION = "consumption"
    CONTACT = "contact"
    ENERGY = "energy"  # is consumption?
    INFRASTRUCTURE = "infrastructure"
    RADIATION = "radiation"  # is a TYPE?
    TRACKING = "tracking"
    TRAFFIC = "traffic"
    WARNINGS = "warning"
    WASTE = "waste"
    WATERING = "watering"  # is a TYPE?
    WEATHER = "weather"


class TYPES(StrEnum):
    AIR = "air"
    BUILDING = "building"
    CONTAINER = "container"
    ELECTRICITY = "electricity"
    ELECTROMAGNETIC = "electromagnetic"
    FLOOD = "flood"
    EARTHQUAKE = "earthquake"
    METEOROLOGICAL = "meteorological"
    NOISE = "noise"
    OCCUPANCY = "occupancy"
    PERSON = "people"
    POLLUTANTS = "pollutants"
    SOLAR = "solar"
    STRUCTURE = "structure"
    WATER = "water"
    XYLOPHAGES = "xylophages"


class LOCATION(StrEnum):
    ANY = "any"
    BUILDING = "building"
    INDOOR = "indoor"
    OUTDOOR = "outdoor"
    PARKING = "parking"

class METHOD(StrEnum):
    RSSI = "rssi"
    MOBILE = "mobile"
    CAMARA = "camara"


class ASPECT(StrEnum):
    EMAIL = "email"
    CAMPAIGN = "campaign"
    GENERAL = "general"
    SURVEY = "survey"
    TICKETING = "ticketing"
    QUALITY = "quality"

class APPLICATION(StrEnum):
    ODOO = "odoo"
