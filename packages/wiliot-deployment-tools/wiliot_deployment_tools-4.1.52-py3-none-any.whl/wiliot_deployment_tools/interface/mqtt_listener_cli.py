from argparse import ArgumentParser
import datetime
import logging
import os
import time
from wiliot_deployment_tools.common.analysis_data_bricks import initialize_logger
from api_secrets import *
from wiliot_deployment_tools.interface.mqtt import MqttClient, Serialization
from wiliot_core.utils.utils import WiliotDir
from wiliot_deployment_tools.common import wltPb_pb2


class MqttListener(MqttClient):
    def __init__(self, gw_id, owner_id, logger_filepath=None, topic_suffix='', serialization=Serialization.UNKNOWN, broker='hive'):
        # Runtime
        self.env_dirs = WiliotDir()
        self.current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.mqtt_listener_dir = os.path.join(self.env_dirs.get_wiliot_root_app_dir(), 'mqtt_listener', self.current_datetime)
        self.env_dirs.create_dir(self.mqtt_listener_dir)
        self.mqtt_logger_filepath = os.path.join(self.mqtt_listener_dir, f'{self.current_datetime}_mqtt.log')
        super().__init__(gw_id, owner_id, self.mqtt_logger_filepath, topic_suffix, serialization, broker)
        logging.getLogger('mqtt').addHandler(logging.StreamHandler())
        
    def listen(self):
        
        def get_payload_to_publish():
            ret = wltPb_pb2.DownlinkMessage()
            ret.gatewayAction.action = "getGwInfo"
            return ret.SerializeToString()

        try:
            i = 0
            while True:
                pass
        except KeyboardInterrupt:
            pass
        finally:
            print('MQTT Listener stopped')
            self.client.disconnect()
            self.client.loop_stop()

def main(arguments):
    parser = ArgumentParser(prog='wlt-mqtt',
                            description='MQTT Listener - CLI Tool to listen to Wiliot topics on external MQTT Broker')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-owner', type=str, help="Owner ID", required=True)
    required.add_argument('-gw', type=str, help="Gateway ID", required=True)
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('-suffix', type=str, help="Topic suffix", default='', required=False)
    optional.add_argument('-broker', type=str, choices=['hive', 'emqx', 'eclipse'])
    args = parser.parse_args(args=arguments)
    topic_suffix = '' if args.suffix == '' else '-'+args.suffix
    mqtt = MqttListener(gw_id=args.gw, owner_id=args.owner, topic_suffix=topic_suffix, broker=args.broker)
    mqtt.listen()

def main_cli():
    main()

if __name__ == '__main__':
        args = [
        '-owner', WH_OWNERID, '-gw', 'GW0CDC7EDB10D0', '-broker', 'eclipse'
        ]
        main(args)
    