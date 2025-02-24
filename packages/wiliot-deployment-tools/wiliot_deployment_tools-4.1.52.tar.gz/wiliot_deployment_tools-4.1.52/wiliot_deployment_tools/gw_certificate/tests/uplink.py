import copy
import datetime
import os
import time
from typing import Literal
import pandas as pd
import plotly.express as px
import tabulate
from wiliot_deployment_tools.ag.ut_defines import BRIDGE_ID, NFPKT, PAYLOAD, RSSI, LAT, LNG
from wiliot_deployment_tools.api.extended_api import GatewayType
from wiliot_deployment_tools.common.debug import debug_print
from wiliot_deployment_tools.gw_certificate.api_if.gw_capabilities import GWCapabilities
from wiliot_deployment_tools.gw_certificate.tests.static.coupling_defines import INCREMENTAL_STAGE_ADVA
from wiliot_deployment_tools.interface.ble_simulator import BLESimulator
from wiliot_deployment_tools.interface.if_defines import BRIDGES, DEFAULT_DELAY, LOCATION
from wiliot_deployment_tools.interface.uart_if import UARTInterface
from wiliot_deployment_tools.gw_certificate.tests.static.uplink_defines import *
from wiliot_deployment_tools.interface.mqtt import MqttClient, Serialization
from wiliot_deployment_tools.interface.pkt_generator import BrgPktGenerator, BrgPktGeneratorNetwork, TagPktGenerator, apply_adva_bitmask
from wiliot_deployment_tools.gw_certificate.tests.static.generated_packet_table import TEST_COUPLING, TEST_UPLINK, TEST_UNIFIED, CouplingRunData, UplinkRunData, UnifiedRunData, SensorRunData, MgmtRunData, PacketTableHelper
from wiliot_deployment_tools.gw_certificate.tests.generic import PassCriteria, PERFECT_SCORE, MINIMUM_SCORE, INCONCLUSIVE_MINIMUM, INIT_INCONCLUSIVE_MINIMUM, GenericTest, GenericStage
from wiliot_deployment_tools.interface.packet_error import PacketError
from wiliot_deployment_tools.gw_certificate.api_if.api_validation import MESSAGE_TYPES, validate_message
from wiliot_deployment_tools.gw_certificate.tests.static.generated_packet_table import CSV_NAME
import pkg_resources


# HELPER DEFINES
TABLE_SUFFIX = "Table"
ERR_SUM_MISSING_PKTS = "Insufficient amount of packets were scanned & uploaded by the gateway. "
ERR_SUM_INVALID_TS = "Invalid timestamps were uploaded by the gateway. "

# HELPER FUNCTIONS

def process_payload(packet:dict):
    payload = packet[PAYLOAD]
    payload = payload.upper()
    if len(payload) == 62 and payload[:4] == '1E16':
        payload = payload [4:]
    # big2little endian
    if payload[:4] == 'FCC6':
        payload = 'C6FC' + payload[4:]
    packet[PAYLOAD] = payload
    return packet

# HELPER CLASSES
class TimestampsHelper(PacketTableHelper):
    def __init__(self):
        self.ts_errors = []
        super().__init__()

    def set_adv_timestamp(self, data_payload, timestamp):
        self.set_field(data_payload, ADV_TIMESTAMP, timestamp)

    def set_adv_timestamp_current(self, data_payload):
        cur_ts = time.time_ns() // 1_000_000
        self.set_field(data_payload, ADV_TIMESTAMP, cur_ts)

    def get_adv_timestamp(self, data_payload):
        return self.get_field(data_payload, ADV_TIMESTAMP)
    
    def get_advertised_entries(self):
        """
        return the lines that contains a packets advertied already. These has the 'adv_timestamp' field.
        """
        return self.table.loc[self.table[ADV_TIMESTAMP].notna()]
    
    def validate_timestamps(self, received_pkts:list):
        packets_sent_df = self.get_advertised_entries().copy()

        # Convert received packets into a DataFrame for vectorized processing
        received_df = pd.DataFrame(received_pkts)
        received_df = received_df[[PAYLOAD, TIMESTAMP]]
        received_df[TIMESTAMP] = pd.to_numeric(received_df[TIMESTAMP], errors='coerce')

        # Map payloads to their received timestamps
        payload_to_ts = received_df.groupby(PAYLOAD)[TIMESTAMP].first().to_dict()

        # Calculate adv_duration once
        def calculate_adv_duration(row):
            if pd.notna(row['duplication']) and pd.notna(row['time_delay']):
                return row['duplication'] * row['time_delay']
            return DEFAULT_DELAY

        packets_sent_df['adv_duration'] = packets_sent_df.apply(calculate_adv_duration, axis=1)

        # Validate timestamps using vectorized operations
        def validate_row(row):
            if row[PAYLOAD] in payload_to_ts:
                received_ts = payload_to_ts[row[PAYLOAD]]
                advertised_ts = row[ADV_TIMESTAMP]
                adv_duration = row['adv_duration']

                min_accepted_ts = int(advertised_ts - (adv_duration + TS_DEVIATION))
                max_accepted_ts = int(advertised_ts + TS_TOLERANCE + TS_DEVIATION)

                if not (min_accepted_ts < received_ts < max_accepted_ts):
                    self.ts_errors.append(
                        f"Timestamp {received_ts} is too far off the accepted range "
                        f"{min_accepted_ts}-{max_accepted_ts} for payload: {row[PAYLOAD]}"
                    )
                return received_ts
            return None

        packets_sent_df[REC_TIMESTAMP] = packets_sent_df.apply(validate_row, axis=1)

        # Validate no 2 packets hold the same timestamp
        if REC_TIMESTAMP in packets_sent_df.columns:
            duplicates = packets_sent_df[REC_TIMESTAMP].value_counts()
            duplicated_ts = duplicates[duplicates > 1].index

            for ts in duplicated_ts:
                self.ts_errors.append(f"Multiple packets were uploaded with identical timestamp (ts = {int(ts)})")

    def add_ts_errs_to_report(self, stage:GenericStage):
        for idx, ts_err in enumerate(self.ts_errors):
            stage.add_to_stage_report(ts_err)
            if idx == 3 and (len(self.ts_errors) - 1) > idx:
                stage.add_to_stage_report(f'Additional errors ({len(self.ts_errors) - 1 - idx}) are suppressed to avoid clutter')
                break
    
    def is_ts_error(self) -> bool:
        return len(self.ts_errors) > 0


# TEST STAGES

class UplinkTestError(Exception):
    pass

class GenericUplinkStage(GenericStage):
    def __init__(self, mqttc:MqttClient, ble_sim:BLESimulator, gw_capabilities:GWCapabilities, stage_name,
                **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(stage_name=stage_name, **self.__dict__)
                
        # Clients
        self.mqttc = mqttc
        self.ble_sim = ble_sim

        # Packets list
        self.local_pkts = []
        self.mqtt_pkts = []
        
        # GW Capabilities
        self.gw_capabilities = gw_capabilities
        
        # Packet Error / Run data
        self.packet_error = PacketError()
        self.run_data = UplinkRunData
        
        # Unified stage
        self.run_data_unified = UnifiedRunData

        self.ts_records = TimestampsHelper()

    def prepare_stage(self, reset_ble_sim=True):
        super().prepare_stage()
        self.mqttc.flush_messages()
        if reset_ble_sim:
            self.ble_sim.set_sim_mode(True) 

    def fetch_mqtt_from_stage(self):
        mqtt_pkts = self.mqttc.get_all_tags_pkts()
        # self.mqtt_packets is a list of pkt jsons: [{timestamp:..., aliasbr.. payload...}, {...}]
        self.mqtt_pkts = list(map(lambda p: process_payload(p), mqtt_pkts))
    
    ## TODO - REWRITE
    def compare_local_mqtt(self):
        self.fetch_mqtt_from_stage()
        local_pkts_df = pd.DataFrame(self.local_pkts, columns=[PAYLOAD, 'duplication', 'time_delay', 'aliasBridgeId'])
        mqtt_pkts_df = pd.DataFrame(self.mqtt_pkts)
        comparison = local_pkts_df

        if PAYLOAD not in mqtt_pkts_df.columns:
            mqtt_pkts_df[PAYLOAD] = ''
        received_pkts_df = pd.merge(local_pkts_df[PAYLOAD], mqtt_pkts_df[PAYLOAD], how='inner')
        
        received_pkts = set(received_pkts_df[PAYLOAD])

        self.pkts_received_count = pd.Series.count(received_pkts_df)
        unique_received_count = len(received_pkts)
        self.pkts_filtered_out_count = self.pkts_received_count - unique_received_count

        comparison[RECEIVED] = comparison[PAYLOAD].isin(received_pkts)
        comparison['pkt_id'] = comparison[PAYLOAD].apply(lambda x: x[-8:])
        self.comparison = comparison
                
    def generate_stage_report(self):
        """
        Generates report for the stage
        """
        self.compare_local_mqtt()
        self.ts_records.validate_timestamps(self.mqtt_pkts)

        num_pkts_sent = len(self.comparison)
        num_pkts_received = self.comparison['received'].eq(True).sum()
        self.stage_pass = num_pkts_received / num_pkts_sent * PERFECT_SCORE
        if self.stage_pass < self.pass_min:
            self.error_summary = ERR_SUM_MISSING_PKTS
        if self.ts_records.is_ts_error():
            self.stage_pass = min(self.stage_pass, self.inconclusive_min)
            self.error_summary += ERR_SUM_INVALID_TS

        self.add_report_header()
        self.add_to_stage_report(f'Number of unique packets sent: {num_pkts_sent}')
        self.add_to_stage_report(f'Number of unique packets received: {num_pkts_received}')
        self.add_to_stage_report(f'Number of total packets received: {self.pkts_received_count}')
        self.add_to_stage_report(f'Number of duplicates out of total: {self.pkts_filtered_out_count}\n')

        not_received = self.comparison[self.comparison[RECEIVED]==False][REPORT_COLUMNS]
        if len(not_received) > 0:
            self.add_to_stage_report('Packets not received:')
            self.add_to_stage_report(tabulate.tabulate(not_received, headers='keys', showindex=False))

        self.ts_records.add_ts_errs_to_report(self)

        self.comparison.to_csv(self.csv_path)
        self.add_to_stage_report(f'Stage data saved - {self.csv_path}')
        debug_print(self.report)
        
        # Generate HTML
        table_html = self.template_engine.render_template('table.html', dataframe=self.comparison.to_html(table_id=self.stage_name + TABLE_SUFFIX),
                                                          table_id=self.stage_name + TABLE_SUFFIX)
        self.report_html = self.template_engine.render_template('stage.html', stage=self, 
                                                                stage_report=self.report.split('\n'), table=table_html)
        
        return self.report

class ManagementPacketStage(GenericUplinkStage):  
    def __init__(self, **kwargs):
        self.stage_tooltip = "Simulates management advertisements from a single bridge. Expects the gateway to scan & upload them"
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.run_data = MgmtRunData().data

    def run(self):
        super().run()
        for index, row in self.run_data.iterrows():
            data = row[ADVA_PAYLOAD]
            # cur_ts = time.time_ns() // 1_000_000
            self.local_pkts.append((row[PAYLOAD], row['duplication'], row['time_delay'], row['adva']))
            self.ble_sim.send_packet(raw_packet=data, duplicates=row['duplication'], delay=row['time_delay'])
            self.ts_records.set_adv_timestamp_current(data)
        time.sleep(10)
    
    def generate_stage_report(self):
        self.compare_local_mqtt()
        self.ts_records.validate_timestamps(self.mqtt_pkts)

        num_pkts_sent = len(self.comparison)
        num_pkts_received = self.comparison['received'].eq(True).sum()
        self.stage_pass = num_pkts_received / num_pkts_sent * PERFECT_SCORE
        if self.stage_pass < self.pass_min:
            self.error_summary = ERR_SUM_MISSING_PKTS
        if self.ts_records.is_ts_error():
            self.stage_pass = min(self.stage_pass, self.inconclusive_min)
            self.error_summary += ERR_SUM_INVALID_TS

        self.add_report_header()
        self.add_to_stage_report(f'Number of unique packets sent: {num_pkts_sent}')
        self.add_to_stage_report(f'Number of unique packets received: {num_pkts_received}\n')

        not_received = self.comparison[self.comparison[RECEIVED]==False][REPORT_COLUMNS]
        if len(not_received) > 0:
            self.add_to_stage_report('Packets not received:')
            self.add_to_stage_report(tabulate.tabulate(not_received, headers='keys', showindex=False))
            self.add_to_stage_report('Check the CSV for more info')
        
        self.ts_records.add_ts_errs_to_report(self)

        self.comparison.to_csv(self.csv_path)
        self.add_to_stage_report(f'Stage data saved - {self.csv_path}')
        debug_print(self.report)
        
        # Generate HTML
        self.report_html = self.template_engine.render_template('stage.html', stage=self, 
                                                                stage_report=self.report.split('\n'))
        
        return self.report

class DataPacketStage(GenericUplinkStage):  

    def __init__(self, **kwargs):
        self.stage_tooltip = "Simulates advertisements from three bridges. Expects the gateway to scan & upload them"
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.run_data = UnifiedRunData().data
    
    def run(self):
        super().run()
        for index, row in self.run_data.iterrows():
            data = row[ADVA_PAYLOAD]
            # cur_ts = time.time_ns() // 1_000_000
            self.local_pkts.append((row[PAYLOAD], row['duplication'], row['time_delay'], row['adva']))
            self.ble_sim.send_packet(raw_packet=data, duplicates=row['duplication'], delay=row['time_delay'])
            self.ts_records.set_adv_timestamp_current(data)
        time.sleep(5)



class SensorPacketStage(GenericUplinkStage):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.pkt_gen = BrgPktGenerator()
        self.stage_tooltip = "Simulates sensor packets advertisements. Expects the gateway to scan & upload them"
        self.error_summary = ERR_SUM_MISSING_PKTS

    def run(self):

        def remove_pre_uuid(payload:str) -> str:
            return payload[16:]
        
        super().run()
        run_data = SensorRunData()
        run_data = run_data.data
        for index, row in run_data.iterrows():
            data = row[ADVA_PAYLOAD]
            si = row['si']
            # Save to local_pkts once for data and once for side info. Each with corresponding adva.
            self.local_pkts.append((row[PAYLOAD], row['duplication'], row['time_delay'], apply_adva_bitmask(row['bridge_id'], 'random_static')))
            self.local_pkts.append((remove_pre_uuid(row['si']), row['duplication'], row['time_delay'], row['adva']))
            self.ble_sim.send_data_si_pair(data_packet=data, si_packet=si, duplicates=row['duplication'], delay=row['time_delay'])
            self.ts_records.set_adv_timestamp_current(data)
        time.sleep(5)
        
    def compare_local_mqtt(self):
        self.fetch_mqtt_from_stage()
        local_pkts_df = pd.DataFrame(self.local_pkts, columns=[PAYLOAD, 'duplication', 'time_delay', 'aliasBridgeId'])
        mqtt_pkts_df = pd.DataFrame(self.mqtt_pkts)
        comparison = local_pkts_df

        if not set(SHARED_COLUMNS) <= set(mqtt_pkts_df.columns):
            missing_columns = list(set(SHARED_COLUMNS) - set(mqtt_pkts_df.columns))
            for missing_column in missing_columns:
                if missing_column in OBJECT_COLUMNS:
                    mqtt_pkts_df[missing_column] = ''
                if missing_column in INT64_COLUMNS:
                    mqtt_pkts_df[missing_column] = 0
        received_pkts_df = pd.merge(local_pkts_df[SHARED_COLUMNS], mqtt_pkts_df[SHARED_COLUMNS], how='inner')
        
        received_pkts = set(received_pkts_df[PAYLOAD])

        self.pkts_received_count = pd.Series.count(received_pkts_df)
        unique_received_count = len(received_pkts)
        self.pkts_filtered_out_count = self.pkts_received_count - unique_received_count

        comparison[RECEIVED] = comparison[PAYLOAD].isin(received_pkts)
        comparison['pkt_id'] = comparison['payload'].apply(lambda x: x[-8:])
        self.comparison = comparison
        
    def generate_stage_report(self):
        self.compare_local_mqtt()
        print(self.comparison)
        report = []
        num_pkts_sent = len(self.comparison)
        num_pkts_received = self.comparison['received'].eq(True).sum()
        pkt_id_pairs = self.comparison.groupby('pkt_id').filter(lambda x: x['received'].all() and len(x) == 2)
        unique_pkt_ids = pkt_id_pairs['pkt_id'].unique()
        num_pairs = len(unique_pkt_ids)
        
        if num_pairs > 1:
            self.stage_pass = PERFECT_SCORE
        else:
            self.stage_pass = MINIMUM_SCORE
            
        self.add_report_header()
        self.add_to_stage_report((f'Number of sensor packets sent: {int(num_pkts_sent / 2)}'))
        self.add_to_stage_report((f'Number of sensor packets received correctly: {num_pairs}\n'))

        not_received = self.comparison[self.comparison[RECEIVED]==False][REPORT_COLUMNS]
        if len(not_received) > 0:
            self.add_to_stage_report('Packets not received:')
            self.add_to_stage_report(tabulate.tabulate(not_received, headers='keys', showindex=False))
        self.comparison.to_csv(self.csv_path)
        self.add_to_stage_report(f'Stage data saved - {self.csv_path}')
        debug_print(self.report)
        
        # Generate HTML
        table_html = self.template_engine.render_template('table.html', dataframe=self.comparison.to_html(table_id=self.stage_name + TABLE_SUFFIX),
                                                          table_id=self.stage_name + TABLE_SUFFIX)
        self.report_html = self.template_engine.render_template('stage.html', stage=self, 
                                                                stage_report=self.report.split('\n'), table=table_html)
        
        return self.report
        
    
class ApiValidationStage(GenericUplinkStage):
    def __init__(self, **kwargs):
        self.stage_tooltip = "Validates the JSON structure of messages uploaded by the gateway in previous stages"
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
    
    def prepare_stage(self):
        super().prepare_stage(reset_ble_sim=False)
        self.mqttc.flush_messages()

    def generate_stage_report(self, **kwargs):
        report = []
        all_validations = []
        self.stage_pass = PERFECT_SCORE
                                
        # Set stage as FAIL if no messages were received:
        if len(self.all_messages_in_test) == 0:
            self.stage_pass = MINIMUM_SCORE
            self.error_summary = "No packets were received"

        for idx, message in enumerate(self.all_messages_in_test):
            message_body = message.body
            if len(message_body['packets']) == 0:
                continue
            validation = validate_message(MESSAGE_TYPES.DATA, message_body)
            errors = []
            for e in validation[1]:
                if e.message not in errors:
                    errors.append(e.message)
            all_validations.append({'valid':validation[0], 'errors': errors, 'message': message_body,})
            if not validation[0]:
                if 'Validation Errors:' not in report:
                    report.append('Validation Errors:')
                report.append(f'- Message (idx={idx}, json timestamp={message_body.get(TIMESTAMP)} Errors:')
                for e in errors:
                    report.append(e)
                self.stage_pass = MINIMUM_SCORE
                self.error_summary = "API (JSON strcture) is invalid"

        self.add_report_header()
        # Add all messages that failed to validate to report
        for line in report:
            self.add_to_stage_report(line)
        all_validations_df = pd.DataFrame(all_validations)
        all_validations_df.to_csv(self.csv_path)
        self.add_to_stage_report(f'Stage data saved - {self.csv_path}')
        debug_print(self.report)
        
        #Generate HTML
        table_html = self.template_engine.render_template('table.html', dataframe=all_validations_df.to_html(table_id=self.stage_name + TABLE_SUFFIX),
                                                          table_id=self.stage_name + TABLE_SUFFIX)
        self.report_html = self.template_engine.render_template('stage.html', stage=self, 
                                                                stage_report=self.report.split('\n'))
        return self.report

class SequentialSequenceIdStage(GenericUplinkStage):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.stage_tooltip = "Validates expected sequenceId in all packets"
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
    
    def prepare_stage(self):
        super().prepare_stage(reset_ble_sim=False)
        self.mqttc.flush_messages()

    def generate_stage_report(self, **kwargs):
        report = []
        self.stage_pass = PERFECT_SCORE
        required_sequenceId = None
        sequenceId_valid = True

        def is_sequenceId_incremental(idx, message):
            nonlocal required_sequenceId, sequenceId_valid
            packets = message['packets']

            # check that there is sequenceId in all packets
            packets_w_seqid = list(filter(lambda p: 'sequenceId' in p, packets))
            if len(packets_w_seqid) == 0:
                sequenceId_valid = False
                report.append(f'No sequenceId in message {idx}. Expected sequenceId in all packets')
                self.error_summary += 'No SequenceId in packets.'
                return False
            
            # initialize the required sequenceId 
            if idx == 0:
                first_pkt = packets[0]
                required_sequenceId = first_pkt['sequenceId'] 
            
            # check that for every packet in message the sequenceId is incremental:
            for pkt in packets:
                pkt_sequenceId = pkt['sequenceId']
                if pkt_sequenceId != required_sequenceId:
                    if sequenceId_valid == True:
                        report.append(f'SequenceId is not incremental. Expected sequenceId is {required_sequenceId} but the packet sequenceId is {pkt_sequenceId}')
                        self.stage_pass = MINIMUM_SCORE
                        self.error_summary = self.error_summary + 'SequenceId is not incremental. '
                        sequenceId_valid = False
                    break
                required_sequenceId += 1

        # Set message type according to coupling, location
        for idx, message in enumerate(self.all_messages_in_test):
            message_body = message.body
            is_sequenceId_incremental(idx=idx, message=message_body)

        self.add_report_header()
        self.add_to_stage_report(f"{'---SequenceId is incremental' if sequenceId_valid else '---SequenceId is NOT incremental'}")
        for line in report:
            self.add_to_stage_report(line)
        debug_print(self.report)
        
        #Generate HTML
        self.report_html = self.template_engine.render_template('stage.html', stage=self, 
                                                                stage_report=self.report.split('\n'))
        return self.report

class AliasBridgeIDStage(GenericUplinkStage):
    def __init__(self, **kwargs):
        self.stage_tooltip = "Validates the uploaded aliasBridgeId is as expected per payload"
        # Data extracted from the test csv
        self.all_test_payloads = None
        self.alias_bridge_id_df = None
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
    
    def prepare_stage(self):
        super().prepare_stage(reset_ble_sim=False)
        self.mqttc.flush_messages()

    def get_data_from_test_csv(self):
        relative_path = 'static/' + CSV_NAME
        csv_path = pkg_resources.resource_filename(__name__, relative_path)
        df = pd.read_csv(csv_path)
        uplink_tests_df = df[(df['test'] == 'unified') | (df['test'] == 'mgmt') | (df['test'] == 'sensor')].copy()

        # Store all test payloads
        all_payloads = uplink_tests_df[PAYLOAD]
        self.all_test_payloads = all_payloads.tolist()

        def _parser(row, desired:Literal['adva', 'without_adva']):
            if desired == 'adva':
                output_string = row.at[ADVA_PAYLOAD][:12]
            elif desired == 'without_adva':
                output_string = row.at[ADVA_PAYLOAD][12:]
            else:
                raise ValueError
            return output_string

        # Create data set for alias bridge verification
        alias_bridge_id_df = uplink_tests_df.copy()
        # alias_bridge_id_df['payload'] = alias_bridge_id_df.apply(lambda row: _parser(row, 'without_adva'), axis=1)
        # Take the adva from the payload
        alias_bridge_id_df['alias_bridge_id'] = alias_bridge_id_df['adva']
        # Convert bridge_id to little endian
        alias_bridge_id_df['alias_bridge_id'] = alias_bridge_id_df['alias_bridge_id'].apply(lambda x: ''.join(format(byte, '02X') for byte in bytes.fromhex(x)[::-1]))
        self.alias_bridge_id_df = alias_bridge_id_df
   
    def generate_stage_report(self, **kwargs):
        report = []
        self.stage_pass = PERFECT_SCORE
        self.get_data_from_test_csv()
        aliasBridgeId_valid = True
            
        def filter_non_test_packets(message):
            packets = message['packets']
            filtered_pkts = []
            for pkt in packets:
                pkt = process_payload(pkt)
                payload = pkt['payload']
                if any(payload in test_payload for test_payload in self.all_test_payloads):
                    filtered_pkts.append(pkt)
            message['packets'] = filtered_pkts
                    
        def is_alias_bridge_id_valid(message): 
            nonlocal aliasBridgeId_valid
            packets = message['packets']

            for pkt in packets:
                if 'aliasBridgeId' in pkt: 
                    pkt_payload = pkt['payload']
                    pkt_alias_bridge_id = pkt['aliasBridgeId']
                    validation_data = self.alias_bridge_id_df[self.alias_bridge_id_df['payload'].str.contains(pkt_payload, case=False)] 
                    if len(validation_data) != 1:
                        debug_print(f"validation_data unexpected len:{len(validation_data)}, for payload:{pkt_payload}")
                        return
                    required_bridge_id = validation_data.iloc[0]['alias_bridge_id']
                    if required_bridge_id != pkt_alias_bridge_id.upper():
                        report.append(f"Alias bridge ID of the packet does not match. The required alias bridge ID is {required_bridge_id} but the packet alias bridge ID is {pkt_alias_bridge_id}")
                        self.stage_pass = MINIMUM_SCORE
                        self.error_summary = "aliasBridgeId doesn't match the expected one of a packet. "
                        aliasBridgeId_valid = False 

        # Set stage as FAIL if no messages were received:
        if len(self.all_messages_in_test) == 0:
            self.stage_pass = MINIMUM_SCORE
            self.error_summary = "No packets were received"

        for idx, message in enumerate(self.all_messages_in_test):
            message_body = message.body
            filter_non_test_packets(message_body)
            if len(message_body['packets']) == 0:
                continue
            is_alias_bridge_id_valid(message=message_body)

        self.add_report_header()
        self.add_to_stage_report(f"{'---Alias bridge ID is valid' if aliasBridgeId_valid else '---Alias bridge ID is NOT valid'}")
        for line in report:
            self.add_to_stage_report(line)
        # Add all messages that failed to validate to report
        debug_print(self.report)
        
        #Generate HTML
        self.report_html = self.template_engine.render_template('stage.html', stage=self, 
                                                                stage_report=self.report.split('\n'))
        return self.report



class GeolocationStage(GenericUplinkStage):
    def __init__(self, **kwargs):
        self.stage_tooltip = "Checks if lat/lng were uploaded under 'location' (optional JSON key) in the uploaded data messages"
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.graph_html_path = os.path.join(self.test_dir, f'{self.stage_name}.html')

    
    def prepare_stage(self):
        super().prepare_stage(reset_ble_sim=False)
        self.mqttc.flush_messages()

    def generate_stage_report(self, **kwargs):
        locations_list = []
        locations_df = pd.DataFrame()
        self.stage_pass = MINIMUM_SCORE
        self.error_summary = "No coordinates were uploaded. "

        # Set message type according to coupling, location
        for message in self.all_messages_in_test:
            message = message.body
            timestamp = message[TIMESTAMP]
            if LOCATION in message.keys():
                loc = message[LOCATION]
                loc.update({TIMESTAMP:timestamp})
                locations_list.append(loc)
        num_unique_locs = 0
        if len(locations_list) > 0:
            self.stage_pass = PERFECT_SCORE
            self.error_summary = ''
            locations_df = pd.DataFrame(locations_list)
            num_unique_locs = locations_df[['lat', 'lng']].drop_duplicates().shape[0]
            fig = px.scatter_mapbox(locations_df, lat=LAT, lon=LNG, color='timestamp', zoom=10)
            fig.update(layout_coloraxis_showscale=False)
            fig.update_layout(scattermode="group", scattergap=0.95, mapbox_style="open-street-map")

        self.add_report_header()
        self.add_to_stage_report(f'Number of unique locations received: {num_unique_locs}')
        # Export all stage data
        locations_df.to_csv(self.csv_path)
        self.add_to_stage_report(f'Stage data saved - {self.csv_path}')
        if num_unique_locs > 0:
            fig.write_html(self.graph_html_path)
        debug_print(self.report)
        
        #Generate HTML
        graph_div = fig.to_html(full_html=False, include_plotlyjs='cdn') if num_unique_locs > 0 else "No graph to display"
        self.report_html = self.template_engine.render_template('stage.html', stage=self, 
                                                                stage_report=self.report.split('\n'), graph = graph_div)
        return self.report


# TEST CLASS
TX_STAGES = [ManagementPacketStage, DataPacketStage, SensorPacketStage]
UNCOUPLED_STAGES = [ManagementPacketStage, DataPacketStage, SensorPacketStage,
                    SequentialSequenceIdStage, AliasBridgeIDStage] 

class UplinkTest(GenericTest):
    def __init__(self, **kwargs):
        self.test_tooltip = "Stages related to gateway BLE scans & MQTT data uploads"
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, test_name=type(self).__name__)
        self.all_messages_in_test = []
        stages = UNCOUPLED_STAGES
        if self.mqttc.get_serialization() == Serialization.JSON:
            stages = stages + [ApiValidationStage]
        if self.gw_capabilities.geoLocationSupport:
            stages.append(GeolocationStage)
        self.stages = [stage(**self.__dict__) for stage in stages]
        

    def run(self):
        super().run()
        self.test_pass = PERFECT_SCORE
        for stage in self.stages:
            stage.prepare_stage()
            stage.run()
            if self.aggregation_time != 0 and type(stage) in TX_STAGES:
                debug_print(f"Waiting {self.aggregation_time} seconds for packets to be uploaded before processing results..")
                time.sleep(self.aggregation_time)
            self.add_to_test_report(stage.generate_stage_report())
            self.test_pass = PassCriteria.calc_for_test(self.test_pass, stage)
            self.all_messages_in_test.extend(self.mqttc.get_all_messages_from_topic('data'))
    
