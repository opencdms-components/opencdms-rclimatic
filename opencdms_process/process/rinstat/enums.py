from enum import Enum


class DateTimeFormats(Enum):
    HOURLY = "hourly"
    DAILY = "daily"
    PENTAD = "pentad"
    DEKADAL = "dekadal"
    MONTHLY = "monthly"
    ANNUAL_WITHIN_YEAR = "annual-within-year"
    ANNUAL = "annual"
    LONGTERM_MONTHLY = "longterm-monthly"
    LONGTERM_WITHIN_YEAR = "longterm-within-year"
    STATION = "station"
    OVERALL = "overall"


class Timespan(Enum):
    DEKAD = "dekad"
    DAILY = "daily"


class FileTypes(Enum):
    CSV = "csv"
    TEXT = "txt"


class FacetBy(Enum):
    STATIONS = "stations"
    ELEMENTS = "elements"
    STATIONS_ELEMENTS = "stations-elements"
    ELEMENTS_STATIONS = "elements-stations"
    NONE = "none"


class Position(Enum):
    IDENTITY = "identity"
    DODGE = "dodge"
    DODGE2 = "dodge2"
    STACK = "stack"
    FILL = "fill"
    LAYER = "layer"


class TimeseriesPlotType(Enum):
    LINE = "line"
    BAR = "bar"


class GGThemes(Enum):
    GREY = "grey"
    GRAY = "gray"
    BW = "bw"
    LINEDRAW = "linedraw"
    LIGHT = "light"
    MINIMAL = "minimal"
    CLASSIC = "classic"
