import copy
import datetime
from enum import Enum
import json
import logging
import time
from typing import Literal, Union
import uuid
import paho.mqtt.client as mqtt
import ssl
import base64
from wiliot_deployment_tools.ag.ut_defines import PACKETS, PAYLOAD, MGMT_PKT, SIDE_INFO_PKT, GW_ID, NFPKT, GW_LOGS, UNIFIED_PKT
from wiliot_deployment_tools.ag.wlt_types_ag import GROUP_ID_BRG2GW, GROUP_ID_SIDE_INFO, GROUP_ID_UNIFIED_PKT
from wiliot_deployment_tools.ag.wlt_types_data import DATA_DEFAULT_GROUP_ID, DataPacket
from wiliot_deployment_tools.common.debug import debug_print
from wiliot_deployment_tools.common import wltPb_pb2
from google.protobuf.message import DecodeError
from google.protobuf.json_format import MessageToDict, Parse, ParseError, ParseDict



DATA_PKT = 'data_pkt'

class CustomBrokers(Enum):
    HIVE = 'broker.hivemq.com'
    EMQX = 'broker.emqx.io'
    ECLIPSE = 'mqtt.eclipseprojects.io'
    
def get_broker_url(broker):
        try:
            broker_url = CustomBrokers[broker.upper()].value
            debug_print(f"Broker URL: {broker_url}")
            return broker_url
        except KeyError:
            raise KeyError(f"Broker '{broker}' not found in CustomBrokers.")

class Serialization(Enum):
    UNKNOWN = "unknown"
    JSON = "JSON"
    PB = "Protobuf"

class GwAction(Enum):
    DISABLE_DEV_MODE = "DevModeDisable"
    REBOOT_GW ="rebootGw"
    GET_GW_INFO ="getGwInfo"

class WltMqttMessage:
    def __init__(self, body, topic):
        self.body = body
        self.mqtt_topic = topic
        self.mqtt_timestamp = datetime.datetime.now()
        self.body_ex = copy.deepcopy(body)
        self.is_unified = False
        if "data" in self.mqtt_topic and PACKETS in self.body_ex.keys():
            for pkt in self.body_ex[PACKETS]:
                data_pkt = DataPacket()
                data_pkt.set(pkt[PAYLOAD])
                if data_pkt.pkt != None:
                    if data_pkt.hdr.group_id == GROUP_ID_BRG2GW:
                        pkt[MGMT_PKT] = copy.deepcopy(data_pkt)
                if data_pkt.hdr.group_id == GROUP_ID_SIDE_INFO:
                    pkt[SIDE_INFO_PKT] = copy.deepcopy(data_pkt)
                if data_pkt.hdr.group_id == DATA_DEFAULT_GROUP_ID:
                    pkt[DATA_PKT] = copy.deepcopy(data_pkt)
                if data_pkt.hdr.group_id == GROUP_ID_UNIFIED_PKT:
                    pkt[UNIFIED_PKT] = copy.deepcopy(data_pkt)
                    self.is_unified = True

    def __repr__(self) -> str:
        if self.body_ex != {}:
            return str(self.body_ex)
        return str(self.body)


class WltMqttMessages:
    def __init__(self):
        self.data = []
        self.status = []
        self.update = []
        self.all = []

    def insert(self, pkt):
        self.all.append(pkt)
        if "data" in pkt.mqtt_topic:
            self.data.append(pkt)
        elif "status" in pkt.mqtt_topic:
            self.status.append(pkt)
        elif "update" in pkt.mqtt_topic:
            self.update.append(pkt)
            
    def __repr__(self) -> str:
        return f'Data {self.data} \n Status {self.status} \n Update {self.update}'
            
class MqttClient:

    def __init__(self, gw_id, owner_id, logger_filepath=None, topic_suffix='', serialization=Serialization.UNKNOWN, broker='hive'):
        # Set variables
        self.gw_id = gw_id
        self.owner_id = owner_id
        self.broker_url = get_broker_url(broker)
        
        # Configure logger
        logger = logging.getLogger('mqtt')
        logger.setLevel(logging.DEBUG)
        if logger_filepath is not None:
            # create file handler which logs even debug messages
            fh = logging.FileHandler(logger_filepath)
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s | %(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            logger.propagate = False # Do not send logs to 'root' logger
            debug_print(f'MQTT Logger initialized at {logger_filepath}')
        self.logger = logger
        
        # Configure Paho MQTT Client
        client_id = f'GW_Certificate_{uuid.uuid4()}'
        self.userdata = {'messages': WltMqttMessages(), 'gw_seen': False , 'logger': self.logger, 'serialization': serialization, 'published': []}
        # Try-except is temporary until old users are up to date
        try:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id, userdata=self.userdata)
        except AttributeError:
            print("\nGW Certificate now runs with latest paho-mqtt!\nPlease upgrade yours to version 2.0.0 (pip install --upgrade paho-mqtt)\n")
            raise
        self.client.enable_logger(logger=self.logger)
        self.client.on_message = on_message
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.on_subscribe = on_subscribe
        self.client.on_unsubscribe = on_unsubscribe
        self.client.on_publish = on_publish
        self.client.on_log = on_log
        self.client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
        debug_print(f'Connecting to MQTT broker: tls://{self.broker_url}:8883, Keepalive=60')
        self.client.connect(self.broker_url, port=8883, keepalive=60)
        # Set Topics
        self.update_topic = f"update{topic_suffix}/{owner_id}/{gw_id}"
        debug_print(f'Subscribe to {self.update_topic}...')
        self.client.subscribe(self.update_topic)
        self.data_topic = f"data{topic_suffix}/{owner_id}/{gw_id}"
        debug_print(f'Subscribe to {self.data_topic}...')
        self.client.subscribe(self.data_topic)
        self.status_topic = f"status{topic_suffix}/{owner_id}/{gw_id}"
        debug_print(f'Subscribe to {self.status_topic}...')
        self.client.subscribe(self.status_topic)
        self.client.loop_start()
        while(not self.client.is_connected()):
            debug_print(f'Waiting for MQTT connection...')
            time.sleep(1)
        debug_print('Connected to MQTT.')
    
    def get_serialization(self):
        """
        return serialization type
        """
        return self.userdata['serialization']
    
    # Downstream Interface
    def send_action(self, action:GwAction):
        """
        Send an action to the gateway
        :param action: GwAction - Required
        """
        assert isinstance(action, GwAction), 'Action Must be a GWAction!'
        # JSON
        if self.get_serialization() in {Serialization.UNKNOWN, Serialization.JSON}:
            raw_payload = json.dumps({"action": action.value})
            self.userdata['published'].append(raw_payload.encode('utf-8'))
            message_info = self.client.publish(self.update_topic, payload=raw_payload)
            print('PublishJSON')
        # PB
        if self.get_serialization() in {Serialization.UNKNOWN, Serialization.PB}:
            payload = wltPb_pb2.DownlinkMessage()
            payload.gatewayAction.action = action.value
            raw_payload = payload.SerializeToString()
            self.userdata['published'].append(raw_payload)
            message_info = self.client.publish(self.update_topic, payload=raw_payload)
            print('PublishPB')
        message_info.wait_for_publish()
        return message_info
    
    def send_payload(self, payload, topic:Literal['update', 'data', 'status']='update'):
        """
        Send a payload to the gateway
        :type payload: dict [JSON] / str [PB]
        :param payload: payload to send
        :type topic: Literal['update', 'data', 'status']
        :param topic: defualts to update
        """
        def cast_to_proto(payload: Union[str, dict, wltPb_pb2.DownlinkMessage]):
            if isinstance(payload, wltPb_pb2.DownlinkMessage):
                return payload

            if isinstance(payload, str):
                payload = json.loads(payload)
            # payload is now a dictionary

            def add_proto_field_type(d):
                for key, value in list(d.items()):
                    if isinstance(value, int):
                        d[key] = {"integerValue": value}
                    elif isinstance(value, float):
                        d[key] = {"numberValue": value}
                    elif isinstance(value, str):
                        d[key] = {"stringValue": value}
                    elif isinstance(value, bool):
                        d[key] = {"boolValue": value}
                    elif isinstance(value, dict):
                        add_proto_field_type(value)  # Recursively handle nested dictionaries

            if 'gatewayConfig' in payload:
                config = payload['gatewayConfig'].get('config', {})
                add_proto_field_type(config)
            
            pb_message = wltPb_pb2.DownlinkMessage()
            ParseDict(payload, pb_message, ignore_unknown_fields=True)

            return pb_message
            
        topic = {'update': self.update_topic,
                 'data': self.data_topic, 
                 'status': self.status_topic}[topic]
        # JSON
        if self.get_serialization() in {Serialization.UNKNOWN, Serialization.JSON}:
            try:
                raw_payload = json.dumps(payload)
                # Add published payload to published list
                self.userdata['published'].append(raw_payload.encode('utf-8'))
                message_info = self.client.publish(topic, raw_payload)
            except TypeError as e:
                if self.get_serialization() != Serialization.UNKNOWN:
                    debug_print(f'Cannot pack payload as JSON!: {payload}')
                    raise e
        # PB
        if self.get_serialization() in {Serialization.UNKNOWN, Serialization.PB}:
            try:
                pb_message = cast_to_proto(payload)
                raw_payload = pb_message.SerializeToString()
                # Add published payload to published list
                self.userdata['published'].append(raw_payload)
                message_info = self.client.publish(topic, raw_payload)
            except ParseError as e:
                if self.get_serialization() != Serialization.UNKNOWN:
                    debug_print(f'Cannot parse payload as PB message!: {payload}')
                    raise e
        message_info.wait_for_publish()
        return message_info
    
    def advertise_packet(self, raw_packet, tx_max_duration=800, use_retries=False):
        if len(raw_packet) < 62:
            if len(raw_packet) == 54:
                raw_packet = 'C6FC' + raw_packet
            if len(raw_packet) == 58:
                raw_packet = '1E16' + raw_packet
        if len(raw_packet) > 62:
            raw_packet = raw_packet[-62:]
        
        assert len(raw_packet) == 62, 'Raw Packet must be 62 chars long!'

        if self.get_serialization() == Serialization.PB: # PB Serialization
            payload = wltPb_pb2.DownlinkMessage()
            payload.txPacket.payload = bytes.fromhex(raw_packet)
            payload.txPacket.maxRetries = int(tx_max_duration / 100)
            payload.txPacket.maxDurationMs = tx_max_duration
        
        else: # JSON Serialization    
            if use_retries:
                payload = {
                    'action': 0, # Advertise BLE Packet
                    'txPacket': raw_packet, # Raw Packet
                    'txMaxRetries': tx_max_duration / 100, # Tx Max Retries
                }
            else:
                payload = {
                'txPacket': raw_packet, # Raw Packet
                'txMaxDurationMs': tx_max_duration, # Tx Max Duration
                'action': 0 # Advertise BLE Packet
            }
        
        self.send_payload(payload, topic='update')
        return payload

    def check_gw_seen(self):
        return self.userdata['gw_seen']
    
    def get_gw_info(self):
        self.flush_messages()
        self.send_action(GwAction.GET_GW_INFO)
        time.sleep(5)
        debug_print('---GW INFO---')
        try:
            gw_info = self.userdata['messages'].status[0]
            debug_print(gw_info)
            self.flush_messages()
            return gw_info
        except IndexError:
            debug_print('No GW INFO')
            self.flush_messages()
            return False
        
    def get_gw_configuration(self):
        self.flush_messages()
        self.send_action(GwAction.REBOOT_GW)
        debug_print('---GW CONFIG---')
        try:
            debug_print(self.userdata['messages'].status)
            return True
        except KeyError:
            return False
            
    def exit_custom_mqtt(self, mqtt_mode:Literal['automatic', 'manual' ,'legacy']):
        if mqtt_mode == 'legacy':
            return self.send_action(GwAction.DISABLE_DEV_MODE)
        elif mqtt_mode == 'automatic':
            custom_mqtt = {
                "customBroker": False,
                "brokerUrl": "",
                "port": 8883,
                "username": "",
                "password": "",
                "updateTopic": f"update/{self.owner_id}/{self.gw_id}",
                "statusTopic": f"status/{self.owner_id}/{self.gw_id}",
                "dataTopic": f"data/{self.owner_id}/{self.gw_id}"
                }
            if self.get_serialization() in {Serialization.UNKNOWN, Serialization.JSON}:
                self.send_payload(custom_mqtt)
            if self.get_serialization() in {Serialization.UNKNOWN, Serialization.PB}:
                self.send_payload({'customBroker': custom_mqtt})
        elif mqtt_mode == 'manual':
            debug_print(f"Make sure GW {self.gw_id} is set to Wiliot MQTT broker")
            return True
    
    # Packet Handling
    def flush_messages(self):
        self.userdata = {'messages': WltMqttMessages(), 'gw_seen': False , 'logger': self.logger, 'serialization':self.get_serialization(), 'published':[]}
        self.client.user_data_set(self.userdata)
    
    def get_all_messages_from_topic(self, topic:Literal['status', 'data', 'update']):
        return getattr(self.userdata['messages'], topic)
    
    def get_all_pkts_from_topic(self, topic:Literal['status', 'data', 'update']):
        pkts = []
        if topic == 'data':
            for p in eval(f'self.userdata["messages"].{topic}'):
                gw_id = p.body_ex[GW_ID] if GW_ID in p.body_ex else ""
                if PACKETS in p.body_ex:
                    for pkt in p.body_ex[PACKETS]:
                        pkt[GW_ID] = gw_id
                        pkts += [pkt]
            return pkts
    
    def get_status_message(self):
        messages = self.get_all_messages_from_topic('status')
        for message in messages:
            if GW_LOGS not in message.body_ex.keys():
                return message.body_ex
        return None
    
    def get_coupled_tags_pkts(self):
        return [p for p in self.get_all_pkts_from_topic('data') if NFPKT in p]
    
    def get_uncoupled_tags_pkts(self):
        return [p for p in self.get_all_pkts_from_topic('data') if NFPKT not in p]
    
    def get_all_tags_pkts(self):
        return [p for p in self.get_all_pkts_from_topic('data')]

# MQTT Client callbacks

def on_connect(mqttc, userdata, flags, reason_code, properties):
    message = f'MQTT: Connection, RC {reason_code}'
    userdata['logger'].info(message)
    # Properties and Flags
    userdata['logger'].info(flags)
    userdata['logger'].info(properties)

def on_disconnect(mqttc, userdata, flags, reason_code, properties):
    if reason_code != 0:
        userdata['logger'].info(f"MQTT: Unexpected disconnection. {reason_code}")
    else:
        userdata['logger'].info('MQTT: Disconnect')
    userdata['logger'].info(flags)
    userdata['logger'].info(properties)

def on_subscribe(mqttc, userdata, mid, reason_codes, properties):
    userdata['logger'].info(f"MQTT: Subscribe, MessageID {mid}")
    for sub_result, idx in enumerate(reason_codes):
        userdata['logger'].info(f"[{idx}]: RC {sub_result}")
    userdata['logger'].info(properties)

def on_unsubscribe(mqttc, userdata, mid, reason_codes, properties):
    userdata['logger'].info(f"MQTT: Unsubscribe, MessageID {mid}")
    for sub_result, idx in enumerate(reason_codes):
        userdata['logger'].info(f"[{idx}]: RC {sub_result}")
    userdata['logger'].info(properties)

def on_message(mqttc, userdata, message):
    # Ignore messages published by MQTT Client
    if message.payload in userdata['published']:
        userdata['logger'].info(f'Received self-published payload - {message.topic}: {message.payload}')
        return
    # Try to parse message as JSON and determine if GW is working in JSON / PB mode
    if userdata['serialization'] == Serialization.UNKNOWN:
        try:
            payload = message.payload.decode("utf-8")
            userdata['logger'].info("Received JSON-Serialized packet - setting serialization to JSON")
            debug_print("##### Received JSON-Serialized packet - setting serialization to JSON #####")
            userdata['serialization'] = Serialization.JSON
        except (json.JSONDecodeError, UnicodeDecodeError):
            userdata['logger'].info("Received non-JSON-Serialized packet - setting serialization to PB")
            debug_print("##### Received non-JSON-Serialized packet - setting serialization to PB #####")
            userdata['serialization'] = Serialization.PB
    if userdata['serialization'] == Serialization.JSON:
        on_message_json(mqttc, userdata, message)
    if userdata['serialization'] == Serialization.PB:
        on_message_protobuf(mqttc, userdata, message)

def on_message_json(mqttc, userdata, message):
    payload = message.payload.decode("utf-8")
    data = json.loads(payload)
    userdata['messages'].insert(WltMqttMessage(data, message.topic))
    userdata['logger'].debug(f'{message.topic}: {payload}')
    if(userdata['gw_seen'] is False):
        userdata['gw_seen'] = True

def on_message_protobuf(mqttc, userdata, message):
    pb_message = None
    if 'status' in message.topic:
        # Try to decode UplinkMessage
        try:
            pb_message = wltPb_pb2.UplinkMessage()
            pb_message.ParseFromString(message.payload)
        except DecodeError as e: 
            userdata['logger'].debug(f'{message.topic}: An exception occured:\n{e}\n(could be a JSON msg or pb msg that is not UplinkMessage)###########')
            userdata['logger'].debug(f'Raw Payload: {message.payload}')
    elif 'data' in message.topic:
        # Try to decode GatewayData
        try:
            pb_message = wltPb_pb2.GatewayData()
            pb_message.ParseFromString(message.payload)
            # # Decode packets payloads as hex
            # for idx, packet in enumerate(pb_message.packets):
            #     pb_message.packets[idx].payload = packet.payload.hex().upper().encode('utf-8')
        except DecodeError as e: 
            userdata['logger'].debug(f'{message.topic}: An exception occured:\n{e}\n(could be a JSON msg or pb msg that is not UplinkMessage)###########')
            userdata['logger'].debug(f'Raw Payload: {message.payload}')
    else:
        userdata['logger'].debug(f'Message from update topic, not decoding')
        userdata['logger'].debug(f'{message.topic}: {message.payload}')
    if pb_message is not None:
        pb_message_dict = MessageToDict(pb_message)
        # Decode b64 packet payloads to hex
        if 'data' in message.topic and 'packets' in pb_message_dict.keys():
            for idx, packet in enumerate(pb_message_dict['packets']):
                pb_message_dict['packets'][idx]['payload'] = base64.b64decode(packet['payload']).hex().upper()
        userdata['messages'].insert(WltMqttMessage(pb_message_dict, message.topic))
        userdata['logger'].debug(f'{message.topic}: {pb_message.__class__.__name__}')
        userdata['logger'].debug(f'{pb_message_dict}')
        if(userdata['gw_seen'] is False):
            userdata['gw_seen'] = True

def on_publish(mqttc, userdata, mid, reason_code, properties):
    userdata['logger'].info(f"MQTT: Publish, MessageID {mid}, RC {reason_code}")
    userdata['logger'].info(properties)

def on_log(mqttc, userdata, level, buf):
    if (level < mqtt.MQTT_LOG_DEBUG):
        userdata['logger'].info(f"MQTT: Log level={level}, Msg={buf}")