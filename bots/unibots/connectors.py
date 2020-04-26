from typing import Union
from unibots.sdk.alice import AliceRequest, AliceResponse, AliceSDK
from unibots.sdk.vk import VKRequest, VKResponse, VKSDK
from unibots.sdk.telegram import TelegramRequest, TelegramResponse, TelegramSDK


RequestConnector = Union[AliceRequest, TelegramRequest, VKRequest]
ResponseConnector = Union[AliceResponse, TelegramResponse, VKResponse]
SDKConnector = Union[AliceSDK, TelegramSDK, VKSDK]
