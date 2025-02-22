from enum import Enum, IntEnum
class AdjustFlag(Enum):
    PostAdjust = "1"
    PreAdjust = "2"
    NoAdjust = "3"

class FilterType(IntEnum):
    NoFilter = 0
    ShareFilter = 1 << 0
    IndexFilter = 1 << 1
    OtherFilter = 1 << 2
    ConvertibleBondFilter = 1 << 3
    ETFFilter = 1 << 4
    NotDilisted = 1 << 5
    # NoFilter = ShareFilter | IndexFilter | OtherFilter | ConvertibleBondFilter | ETFFilter

class StockType(Enum):
    Share = '1'
    Index = '2'
    Other = '3'
    ConvertibleBond = '4'
    ETF = '5'

class RequestFrequency(Enum):
    FiveMinutsK = '5'
    FifteenMinutsK = '15'
    ThirtyMinutsK = '30'
    HourK = '60'
    DayK = 'd'
    WeekK = 'w'
    MonthK = 'm'