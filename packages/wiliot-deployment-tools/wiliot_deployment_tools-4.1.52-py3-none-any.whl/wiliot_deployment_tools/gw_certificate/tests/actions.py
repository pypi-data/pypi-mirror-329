import base64
import datetime
import json
import os
import time
import pandas as pd
import numpy as np
import plotly.express as px
import jinja2

from wiliot_deployment_tools.common.debug import debug_print
from wiliot_deployment_tools.interface.ble_sniffer import BLESniffer,BLESnifferContext
from wiliot_deployment_tools.interface.mqtt import MqttClient, GwAction
from wiliot_deployment_tools.gw_certificate.tests.generic import PassCriteria, PERFECT_SCORE, MINIMUM_SCORE, INCONCLUSIVE_MINIMUM, GenericTest, GenericStage, OPTIONAL
from wiliot_deployment_tools.gw_certificate.tests.static.references import GW_ACTIONS_DOC


class GenericActionsStage(GenericStage):
    def __init__(self, sniffer:BLESniffer, mqttc:MqttClient, stage_name, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(stage_name=stage_name, **self.__dict__)        
        
        #Clients
        self.mqttc = mqttc
        
        #Stage Params
        self.action = ""
        
        #Paths
        self.summary_csv_path = os.path.join(self.test_dir, f'{self.stage_name}_summary.csv')

        
    def prepare_stage(self):
        super().prepare_stage()
        self.mqttc.flush_messages()
    
    def generate_stage_report(self):
        self.add_report_header()

class GatewayInfoStage(GenericActionsStage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, stage_name=type(self).__name__)
        self.stage_tooltip = "Issues a Gateway Info action to the gateway. Expects the gateway to publish a response"
        self.error_summary = "Did not receive a response to the Gateway Info action"
        self.action = "getGwInfo"
        self.response = None
    
    def run(self):
        super().run()
        self.gw_info = self.mqttc.get_gw_info()

    def generate_stage_report(self):
        super().generate_stage_report()

        # Calculate whether stage pass/failed
        if not self.gw_info or "gatewayInfo" not in self.gw_info.body or len(self.gw_info.body) > 1:
            self.stage_pass = MINIMUM_SCORE
            self.add_to_stage_report(f'Did not receive a response to the Gateway Info action. For more info visit:')
            self.add_to_stage_report(f'{GW_ACTIONS_DOC}')
        else:
            self.stage_pass = PERFECT_SCORE
            self.response = repr(self.gw_info)
            self.add_to_stage_report('A Gateway Info response was receieved:')
            self.add_to_stage_report(self.response)

        # Export all stage data
        csv_data = {'Action': [self.action], 'Response': [self.response], 'Pass': [self.stage_pass > self.pass_min]}
        pd.DataFrame(csv_data).to_csv(self.summary_csv_path)
        self.add_to_stage_report(f'\nStage summary saved - {self.summary_csv_path}')
        debug_print(self.report)
        
        # Generate HTML
        self.report_html = self.template_engine.render_template('stage.html', stage=self, 
                                                                stage_report=self.report.split('\n'))
        return self.report


class RebootStage(GenericActionsStage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, stage_name=type(self).__name__)
        self.stage_tooltip = "Issues reboot action to the gateway. Expects it to reboot"
        self.error_summary = "The gateway did not reboot as expected"
        self.action = "rebootGw"
    
    def run(self):
        super().run()
        timeout = datetime.datetime.now() + datetime.timedelta(minutes=3)
        self.status_message = None

        self.mqttc.send_action(GwAction.REBOOT_GW)
        while datetime.datetime.now() < timeout and self.status_message is None:
            self.status_message = self.mqttc.get_status_message()
            time.sleep(5)

    def generate_stage_report(self):
        super().generate_stage_report()

        # Calculate whether stage pass/failed
        if (self.status_message is None or 
            (not any('gatewayconf' == key.lower() for key in self.status_message.keys()) and
             not any('gatewaystatus' == key.lower() for key in self.status_message.keys()))):
            self.stage_pass = MINIMUM_SCORE
            self.add_to_stage_report(f"The gateway did not validly reboot")
            self.add_to_stage_report(f"Gateways are expected to upload a status(configuration) message upon establishing MQTT connection, which wasn't received.")
        else:
            self.stage_pass = PERFECT_SCORE
            self.add_to_stage_report(f"Gateway rebooted and uploaded a configuration message, as expected.")
        
        # Export all stage data
        csv_data = {'Action': [self.action], 'Pass': [self.stage_pass > self.pass_min]}
        pd.DataFrame(csv_data).to_csv(self.summary_csv_path)
        self.add_to_stage_report(f'\nStage summary saved - {self.summary_csv_path}')

        # Generate HTML
        self.report_html = self.template_engine.render_template('stage.html', stage=self, 
                                                                stage_report=self.report.split('\n'))
        return self.report


STAGES = [GatewayInfoStage, RebootStage]

class ActionsTest(GenericTest):
    def __init__(self, **kwargs):        
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, test_name=type(self).__name__)
        self.test_tooltip = "Stages publishing different actions (via the 'update' topic). Optional"
        self.result_indication = OPTIONAL
        self.stages = [stage(**self.__dict__) for stage in STAGES]
    
    def run(self):
        super().run()
        self.test_pass = PERFECT_SCORE
        for stage in self.stages:
            stage.prepare_stage()
            stage.run()
            self.add_to_test_report(stage.generate_stage_report())
            self.test_pass = PassCriteria.calc_for_test(self.test_pass, stage)
