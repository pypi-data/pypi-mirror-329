from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Location(_message.Message):
    __slots__ = ("lat", "lng")
    LAT_FIELD_NUMBER: _ClassVar[int]
    LNG_FIELD_NUMBER: _ClassVar[int]
    lat: float
    lng: float
    def __init__(self, lat: _Optional[float] = ..., lng: _Optional[float] = ...) -> None: ...

class Value(_message.Message):
    __slots__ = ("integerValue", "numberValue", "stringValue", "boolValue")
    INTEGERVALUE_FIELD_NUMBER: _ClassVar[int]
    NUMBERVALUE_FIELD_NUMBER: _ClassVar[int]
    STRINGVALUE_FIELD_NUMBER: _ClassVar[int]
    BOOLVALUE_FIELD_NUMBER: _ClassVar[int]
    integerValue: int
    numberValue: float
    stringValue: str
    boolValue: bool
    def __init__(self, integerValue: _Optional[int] = ..., numberValue: _Optional[float] = ..., stringValue: _Optional[str] = ..., boolValue: bool = ...) -> None: ...

class GatewayData(_message.Message):
    __slots__ = ("gatewayId", "timestamp", "packets", "location")
    class Packet(_message.Message):
        __slots__ = ("payload", "timestamp", "sequenceId", "rssi", "aliasBridgeId")
        PAYLOAD_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        SEQUENCEID_FIELD_NUMBER: _ClassVar[int]
        RSSI_FIELD_NUMBER: _ClassVar[int]
        ALIASBRIDGEID_FIELD_NUMBER: _ClassVar[int]
        payload: bytes
        timestamp: int
        sequenceId: int
        rssi: int
        aliasBridgeId: str
        def __init__(self, payload: _Optional[bytes] = ..., timestamp: _Optional[int] = ..., sequenceId: _Optional[int] = ..., rssi: _Optional[int] = ..., aliasBridgeId: _Optional[str] = ...) -> None: ...
    GATEWAYID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PACKETS_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    gatewayId: str
    timestamp: int
    packets: _containers.RepeatedCompositeFieldContainer[GatewayData.Packet]
    location: Location
    def __init__(self, gatewayId: _Optional[str] = ..., timestamp: _Optional[int] = ..., packets: _Optional[_Iterable[_Union[GatewayData.Packet, _Mapping]]] = ..., location: _Optional[_Union[Location, _Mapping]] = ...) -> None: ...

class UplinkMessage(_message.Message):
    __slots__ = ("gatewayStatus", "gatewayInfo", "gatewayLogs", "actionStatus")
    GATEWAYSTATUS_FIELD_NUMBER: _ClassVar[int]
    GATEWAYINFO_FIELD_NUMBER: _ClassVar[int]
    GATEWAYLOGS_FIELD_NUMBER: _ClassVar[int]
    ACTIONSTATUS_FIELD_NUMBER: _ClassVar[int]
    gatewayStatus: GatewayStatus
    gatewayInfo: GatewayInfo
    gatewayLogs: GatewayLogs
    actionStatus: ActionStatus
    def __init__(self, gatewayStatus: _Optional[_Union[GatewayStatus, _Mapping]] = ..., gatewayInfo: _Optional[_Union[GatewayInfo, _Mapping]] = ..., gatewayLogs: _Optional[_Union[GatewayLogs, _Mapping]] = ..., actionStatus: _Optional[_Union[ActionStatus, _Mapping]] = ...) -> None: ...

class GatewayStatus(_message.Message):
    __slots__ = ("gatewayId", "gatewayType", "downlinkSupported", "bridgeOtaUpgradeSupported", "apiVersion", "version", "bleSwVersion", "interfaceSwVersion", "location", "config", "bleAddress")
    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Value, _Mapping]] = ...) -> None: ...
    GATEWAYID_FIELD_NUMBER: _ClassVar[int]
    GATEWAYTYPE_FIELD_NUMBER: _ClassVar[int]
    DOWNLINKSUPPORTED_FIELD_NUMBER: _ClassVar[int]
    BRIDGEOTAUPGRADESUPPORTED_FIELD_NUMBER: _ClassVar[int]
    APIVERSION_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    BLESWVERSION_FIELD_NUMBER: _ClassVar[int]
    INTERFACESWVERSION_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    BLEADDRESS_FIELD_NUMBER: _ClassVar[int]
    gatewayId: str
    gatewayType: str
    downlinkSupported: bool
    bridgeOtaUpgradeSupported: bool
    apiVersion: int
    version: str
    bleSwVersion: str
    interfaceSwVersion: str
    location: Location
    config: _containers.MessageMap[str, Value]
    bleAddress: str
    def __init__(self, gatewayId: _Optional[str] = ..., gatewayType: _Optional[str] = ..., downlinkSupported: bool = ..., bridgeOtaUpgradeSupported: bool = ..., apiVersion: _Optional[int] = ..., version: _Optional[str] = ..., bleSwVersion: _Optional[str] = ..., interfaceSwVersion: _Optional[str] = ..., location: _Optional[_Union[Location, _Mapping]] = ..., config: _Optional[_Mapping[str, Value]] = ..., bleAddress: _Optional[str] = ...) -> None: ...

class GatewayInfo(_message.Message):
    __slots__ = ("entries",)
    class EntriesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Value, _Mapping]] = ...) -> None: ...
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.MessageMap[str, Value]
    def __init__(self, entries: _Optional[_Mapping[str, Value]] = ...) -> None: ...

class GatewayLogs(_message.Message):
    __slots__ = ("logs",)
    LOGS_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, logs: _Optional[_Iterable[str]] = ...) -> None: ...

class ActionStatus(_message.Message):
    __slots__ = ("action", "status")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    action: int
    status: int
    def __init__(self, action: _Optional[int] = ..., status: _Optional[int] = ...) -> None: ...

class DownlinkMessage(_message.Message):
    __slots__ = ("txPacket", "gatewayAction", "bridgeUpgrade", "gatewayConfig", "customBroker", "customMessage")
    TXPACKET_FIELD_NUMBER: _ClassVar[int]
    GATEWAYACTION_FIELD_NUMBER: _ClassVar[int]
    BRIDGEUPGRADE_FIELD_NUMBER: _ClassVar[int]
    GATEWAYCONFIG_FIELD_NUMBER: _ClassVar[int]
    CUSTOMBROKER_FIELD_NUMBER: _ClassVar[int]
    CUSTOMMESSAGE_FIELD_NUMBER: _ClassVar[int]
    txPacket: TxPacket
    gatewayAction: GatewayAction
    bridgeUpgrade: BridgeUpgrade
    gatewayConfig: GatewayConfig
    customBroker: CustomBroker
    customMessage: CustomMessage
    def __init__(self, txPacket: _Optional[_Union[TxPacket, _Mapping]] = ..., gatewayAction: _Optional[_Union[GatewayAction, _Mapping]] = ..., bridgeUpgrade: _Optional[_Union[BridgeUpgrade, _Mapping]] = ..., gatewayConfig: _Optional[_Union[GatewayConfig, _Mapping]] = ..., customBroker: _Optional[_Union[CustomBroker, _Mapping]] = ..., customMessage: _Optional[_Union[CustomMessage, _Mapping]] = ...) -> None: ...

class TxPacket(_message.Message):
    __slots__ = ("payload", "maxRetries", "maxDurationMs")
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    MAXRETRIES_FIELD_NUMBER: _ClassVar[int]
    MAXDURATIONMS_FIELD_NUMBER: _ClassVar[int]
    payload: bytes
    maxRetries: int
    maxDurationMs: int
    def __init__(self, payload: _Optional[bytes] = ..., maxRetries: _Optional[int] = ..., maxDurationMs: _Optional[int] = ...) -> None: ...

class GatewayAction(_message.Message):
    __slots__ = ("action",)
    ACTION_FIELD_NUMBER: _ClassVar[int]
    action: str
    def __init__(self, action: _Optional[str] = ...) -> None: ...

class BridgeUpgrade(_message.Message):
    __slots__ = ("rebootPacket", "txMaxDurationMs", "txMaxRetries", "bridgeId", "versionUuid", "upgradeBlSd", "imageDirUrl")
    REBOOTPACKET_FIELD_NUMBER: _ClassVar[int]
    TXMAXDURATIONMS_FIELD_NUMBER: _ClassVar[int]
    TXMAXRETRIES_FIELD_NUMBER: _ClassVar[int]
    BRIDGEID_FIELD_NUMBER: _ClassVar[int]
    VERSIONUUID_FIELD_NUMBER: _ClassVar[int]
    UPGRADEBLSD_FIELD_NUMBER: _ClassVar[int]
    IMAGEDIRURL_FIELD_NUMBER: _ClassVar[int]
    rebootPacket: bytes
    txMaxDurationMs: int
    txMaxRetries: int
    bridgeId: str
    versionUuid: str
    upgradeBlSd: bool
    imageDirUrl: str
    def __init__(self, rebootPacket: _Optional[bytes] = ..., txMaxDurationMs: _Optional[int] = ..., txMaxRetries: _Optional[int] = ..., bridgeId: _Optional[str] = ..., versionUuid: _Optional[str] = ..., upgradeBlSd: bool = ..., imageDirUrl: _Optional[str] = ...) -> None: ...

class GatewayConfig(_message.Message):
    __slots__ = ("version", "bleSwVersion", "interfaceSwVersion", "location", "config")
    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Value, _Mapping]] = ...) -> None: ...
    VERSION_FIELD_NUMBER: _ClassVar[int]
    BLESWVERSION_FIELD_NUMBER: _ClassVar[int]
    INTERFACESWVERSION_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    version: str
    bleSwVersion: str
    interfaceSwVersion: str
    location: Location
    config: _containers.MessageMap[str, Value]
    def __init__(self, version: _Optional[str] = ..., bleSwVersion: _Optional[str] = ..., interfaceSwVersion: _Optional[str] = ..., location: _Optional[_Union[Location, _Mapping]] = ..., config: _Optional[_Mapping[str, Value]] = ...) -> None: ...

class CustomBroker(_message.Message):
    __slots__ = ("customBroker", "port", "brokerUrl", "username", "password", "updateTopic", "statusTopic", "dataTopic")
    CUSTOMBROKER_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    BROKERURL_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    UPDATETOPIC_FIELD_NUMBER: _ClassVar[int]
    STATUSTOPIC_FIELD_NUMBER: _ClassVar[int]
    DATATOPIC_FIELD_NUMBER: _ClassVar[int]
    customBroker: bool
    port: int
    brokerUrl: str
    username: str
    password: str
    updateTopic: str
    statusTopic: str
    dataTopic: str
    def __init__(self, customBroker: bool = ..., port: _Optional[int] = ..., brokerUrl: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., updateTopic: _Optional[str] = ..., statusTopic: _Optional[str] = ..., dataTopic: _Optional[str] = ...) -> None: ...

class CustomMessage(_message.Message):
    __slots__ = ("entries",)
    class EntriesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Value, _Mapping]] = ...) -> None: ...
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.MessageMap[str, Value]
    def __init__(self, entries: _Optional[_Mapping[str, Value]] = ...) -> None: ...
