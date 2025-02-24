from argparse import ArgumentParser
from wiliot_deployment_tools.gw_certificate.gw_certificate import GWCertificate, GW_CERT_VERSION
from wiliot_deployment_tools.gw_certificate.tests import TESTS
from wiliot_deployment_tools.gw_certificate.tests.throughput import STRESS_DEFAULT_PPS

from wiliot_deployment_tools.gw_certificate.tests.uplink import UplinkTest
from wiliot_deployment_tools.gw_certificate.tests.throughput import StressTest

def filter_tests(tests_names):
    chosen_tests = []
    if tests_names == []:
        return TESTS
    for test_class in TESTS:
        for test_name in tests_names:
            if test_name in test_class.__name__.lower() and test_class not in chosen_tests:
                chosen_tests.append(test_class)
    return chosen_tests

def main():
    usage = (
        "usage: wlt-gw-certificate [-h] -owner OWNER -gw GW\n"
        f"                          [-tests {{connection, uplink, downlink, stress}}] [-update] [-pps {STRESS_DEFAULT_PPS}]"
        )

    parser = ArgumentParser(prog='wlt-gw-certificate',
                            description=f'Gateway Certificate {GW_CERT_VERSION} - CLI Tool to test Wiliot GWs', usage=usage)

    required = parser.add_argument_group('required arguments')
    required.add_argument('-owner', type=str, help="Owner ID", required=True)
    required.add_argument('-gw', type=str, help="Gateway ID", required=True)
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('-suffix', type=str, help="Topic suffix", default='', required=False)
    optional.add_argument('-tests', type=str, choices=['connection', 'uplink', 'downlink', 'actions', 'stress'], help="Tests to run", required=False, nargs='+', default=[])
    optional.add_argument('-update', action='store_true', help='Update test board firmware', default=False, required=False)
    optional.add_argument('-pps', type=int, help='Single packets-per-second rate to simulate in the stress test',
                          choices=STRESS_DEFAULT_PPS, default=None, required=False)
    optional.add_argument('-agg', type=int, help='Aggregation time [seconds] the Uplink stages wait before processing results',
                          default=0, required=False)
    args = parser.parse_args()

    tests = filter_tests(args.tests)
    topic_suffix = '' if args.suffix == '' else '-'+args.suffix

    if args.pps != None and StressTest not in tests:
        parser.error("Packets per second (-pps) flag can only be used when 'stress' is included in test list (e.g. -tests stress)")
    if args.agg != 0 and UplinkTest not in tests:
        parser.error("Aggregation time (-agg) flag can only be used when 'uplink' is included in test list (e.g. -tests uplink)")

    gwc = GWCertificate(gw_id=args.gw, owner_id=args.owner, topic_suffix=topic_suffix, tests=tests, update_fw=args.update,
                        stress_pps=args.pps, aggregation_time=args.agg)
    gwc.run_tests()
    gwc.create_results_html()

def main_cli():
    main()

if __name__ == '__main__':
    main()
    