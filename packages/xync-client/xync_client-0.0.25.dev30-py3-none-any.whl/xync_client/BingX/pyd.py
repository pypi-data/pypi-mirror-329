from pydantic import BaseModel
from typing import List

class User(BaseModel):
    nickname: str
    avatar: str
    phone: bool
    email: bool
    # payMethods: dict


class AvailableVolume(BaseModel):
    tradeUSDTNum30: float


class Price(BaseModel):
    asset: str
    fiat: str
    value: str


class OrderLimitsIn(BaseModel):
    minAmount: str
    maxAmount: str


class PmEpyd(BaseModel):
    id: int
    name: str
    mainColor: str
    icon: str
    number: int

class UserPaymentMethod(BaseModel):
    id: int
    paymentMethodId: int
    paymentMethodName: str
    paymentMethodIcon: str
    mainColor: str

class PaymentMethod(BaseModel):
    id: int
    name: str
    icon: str
    mainColor: str
    userPaymentMethodList: List[UserPaymentMethod]

class Ads(BaseModel):
    orderNo: str
    tradeRecent: int
    type: int
    asset: str
    fiat: str
    fiatSymbol: str
    totalNumber: float
    availableAmount: float
    priceType: int
    fixPrice: float
    floatRatio: float
    price: float
    minAmount: float
    maxAmount: float
    assetPrecision: int
    fiatPrecision: int
    pricePrecision: int
    paymentMethodList: List[PaymentMethod]
    termsDesc: str
    hidePaymentInfo: int
    nickName: str
    merchantUid: str
    restStatus: int
    onlineStatus: bool
    merchantOnlineHint: str
    avatarUrl: str
    tradeNum30: int
    expireMinute: int
    status: int
    autoReplyMsg: str
    formatPrice: str
    formatMinAmount: str
    formatMaxAmount: str
    promotionAdvert: bool
    promotionAdvertOnline: bool
    promotionAdvertEnableChange: bool
    isCanBeSubsidized: bool
    merchantKycType: int
    merchantVerificationType: int
    isUserMatchCondition: bool
    notMatchConditionReason: str