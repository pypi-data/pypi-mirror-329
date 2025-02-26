from typing import Literal, TypedDict, Union, List, Tuple, Dict, Optional
import desk.enum as enum

# WebSocket
TradeSubscription = TypedDict(
    "TradeSubscription", {"type": Literal["tradesV2"], "symbol": str})
OrderbookSubscription = TypedDict("OrderbookSubscription", {
                                  "type": Literal["l2BookV2"], "symbol": str})
MarkPriceSubscription = TypedDict("MarkPriceSubscription", {
                                  "type": Literal["markPricesV2"]})
IndexPriceSubscription = TypedDict("IndexPriceSubscription", {
                                   "type": Literal["indexPricesV2"]})

Subscription = Union[TradeSubscription, OrderbookSubscription,
                     MarkPriceSubscription, IndexPriceSubscription]

StreamMessage = TypedDict("StreamMessage", {
    "type": str
})

OrderbookData = TypedDict("OrderbookData", {
    "bids": List[Tuple[str, str]],
    "asks": List[Tuple[str, str]]
})

OrderbookStreamMessage = TypedDict("OrderbookStreamMessage", {
    "type": str,
    "symbol": str,
    "data": OrderbookData
})

TradeData = TypedDict("TradeData", {
    "price": str,
    "quantity": str,
    "side": str
})

TradeStreamMessage = TypedDict("TradeStreamMessage", {
    "type": str,
    "symbol": str,
    "data": TradeData
})

MarkPriceData = TypedDict("MarkPriceData", {
    "symbol": str,
    "mark_price": str,
    "index_price": str
})

MarkPricesMessage = TypedDict("MarkPricesMessage", {
    "type": str,
    "data": List[MarkPriceData]
})

MarkPricesResponse = TypedDict("MarkPricesResponse", {
    "symbol": str,
    "markPrice": str,
    "indexPrice": str
})

ParsedMarkPricesMessage = TypedDict("ParsedMarkPricesMessage", {
    "type": str,
    "data": List[MarkPricesResponse]
})

CollateralPriceData = TypedDict("CollateralPriceData", {
    "collateral_id": str,
    "asset": str,
    "price": str
})

CollateralPricesMessage = TypedDict("CollateralPricesMessage", {
    "type": str,
    "data": List[CollateralPriceData]
})

CollateralPricesResponse = TypedDict("CollateralPricesResponse", {
    "collateralId": str,
    "asset": str,
    "price": str
})

CollateralPrices = Dict[str, CollateralPricesResponse]

ParsedCollateralPricesMessage = TypedDict("ParsedCollateralPricesMessage", {
    "type": str,
    "data": List[CollateralPrices]
})

WsMessage = Union[CollateralPricesMessage, MarkPricesMessage, OrderbookStreamMessage,
                  ParsedCollateralPricesMessage, ParsedMarkPricesMessage, StreamMessage, TradeStreamMessage]

# Manage Order
OrderType = Literal[
    "Limit",
    "Market",
    "Stop",
    "StopMarket",
    "TakeProfit",
    "TakeProfitMarket"
]
Hex = str  # Assuming Hex is just a string type in Python

TimeInForce = Literal["GTC", "FOK", "IOC", "PostOnly"]
OrderSide = Literal["Long", "Short"] 

OrderRequest = TypedDict("OrderRequest", {
    "symbol": str,
    "broker_id": str,
    "subaccount": Hex,
    "amount": str,
    "price": str,
    "order_type": OrderType,
    "side": OrderSide,
    "nonce": str,
    "reduce_only": Optional[bool],
    "trigger_price": Optional[str],
    "is_conditional_order": Optional[bool],
    "time_in_force": Optional[TimeInForce | enum.TimeInForce],
    "wait_for_reply": bool,
    "client_order_id": Optional[str]
}, total=False)  # total=False makes all fields optional

CancelOrderRequest = TypedDict("CancelOrderRequest", {
    "symbol": str,
    "subaccount": Hex,
    "order_digest": Hex,
    "nonce": str,
    "is_conditional_order": bool,
    "wait_for_reply": bool,
    "client_order_id": Optional[str]
})

CancelAllOrdersRequest = TypedDict("CancelAllOrdersRequest", {
    "symbol": str,
    "subaccount": Hex,
    "nonce": str,
    "is_conditional_order": bool,
    "wait_for_reply": bool,
})

CreatePlaceOrderFn = TypedDict("CreatePlaceOrderFn", {
    "amount": str,
    "price": str,
    "side": OrderSide | enum.OrderSide,
    "symbol": str | enum.MarketSymbol,
    "orderType": OrderType | enum.OrderType,
    "reduceOnly": Optional[bool],
    "triggerPrice": Optional[str],
    "waitForReply": bool,
    "timeInForce": Optional[TimeInForce | enum.TimeInForce],
    "clientOrderId": Optional[str]
})  # total=False makes reduceOnly and triggerPrice optional

CancelOrderFn = TypedDict("CancelOrderFn", {
    "symbol": str,
    "orderDigest": Hex,
    "isConditionalOrder": bool,
    "waitForReply": bool,
    "clientOrderId": Optional[str]
})

CancelAllOrdersFn = TypedDict("CancelAllOrdersFn", {
    "symbol": str,
    "is_conditional_order": bool,
    "wait_for_reply": bool,
})


class PlaceOrderResponse(TypedDict):
    subaccount: str
    symbol: enum.MarketSymbol
    side: enum.OrderSide
    price: str
    quantity: str
    nonce: str
    order_type: enum.OrderType
    time_in_force: enum.TimeInForce
    order_digest: str
    filled_quantity: str
    avg_fill_price: str
    execution_fee: str
    client_order_id: str | None
    trigger_price: str | None


# Info

OrderSideType = Literal["BUY", "SELL"]

class CollateralInfo(TypedDict):
    asset: str
    collateral_id: str
    amount: str

class OpenOrderInfo(TypedDict):
    order_digest: str
    symbol: str
    side: OrderSideType
    price: str
    original_quantity: str
    remaining_quantity: str

class PositionInfo(TypedDict):
    symbol: str
    side: OrderSideType
    entry_price: str
    amount: str

class SubAccountSummary(TypedDict):
    open_orders: List[OpenOrderInfo]
    collaterals: List[CollateralInfo]
    positions: List[PositionInfo]
    account_margin: str
    collateral_value: str
    unrealized_pnl: str
    pending_funding_fee: str
    pending_borrowing_fee: str
    account_imr: str
    order_imr: str
    position_imr: str
    position_mmr: str