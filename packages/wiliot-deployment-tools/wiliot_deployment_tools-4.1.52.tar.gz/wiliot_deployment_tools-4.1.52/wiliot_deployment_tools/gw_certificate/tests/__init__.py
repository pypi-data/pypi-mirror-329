from wiliot_deployment_tools.gw_certificate.tests.downlink import DownlinkTest 
from wiliot_deployment_tools.gw_certificate.tests.connection import ConnectionTest
from wiliot_deployment_tools.gw_certificate.tests.uplink import UplinkTest
from wiliot_deployment_tools.gw_certificate.tests.actions import ActionsTest
from wiliot_deployment_tools.gw_certificate.tests.throughput import StressTest

TESTS = [ConnectionTest, UplinkTest, DownlinkTest, ActionsTest, StressTest]


