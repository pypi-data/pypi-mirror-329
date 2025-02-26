import enum

class OrderType(enum.Enum):
    LIMIT = "Limit"
    MARKET = "Market"
    STOP = "Stop"
    STOP_MARKET = "StopMarket"
    TAKE_PROFIT = "TakeProfit"
    TAKE_PROFIT_MARKET = "TakeProfitMarket"

class TimeInForce(enum.Enum):
    GTC = "GTC"
    FOK = "FOK"
    IOC = "IOC"
    POST_ONLY = "PostOnly"

class OrderSide(enum.Enum):
    LONG = "Long"
    SHORT = "Short"

class MarketSymbol(enum.Enum):
    BTCUSD = "BTCUSD"
    ETHUSD = "ETHUSD"
