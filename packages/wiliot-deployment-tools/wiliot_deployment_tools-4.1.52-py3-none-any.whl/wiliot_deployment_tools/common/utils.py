# External libraries
import math
import pandas as pd
import numpy as np
import datetime
from collections import defaultdict


from wiliot_deployment_tools.common.debug import is_databricks

try:
    from zoneinfo import ZoneInfo  # will run only in python 3.9+
except ImportError:
    from backports.zoneinfo import ZoneInfo  # backport to python < 3.9

# CSV Parsing
def get_ref_tags(csv_filepath):
    # TODO - fix to insert header if not given
    """
        returns an array of tags externalIds from a csv including one column of all the tags
        :type csv_filepath: string
        :param csv_filepath: filepath to csv with one column including all the tags
        output type: array
        output param: array of tags externalIds from a csv
    """
    tags_list = pd.read_csv(csv_filepath)
    tags_list = tags_list.to_dict()
    res = defaultdict(list)
    for key in tags_list.keys():
        for idx in tags_list[key]:
            if type(tags_list[key][idx]) == str and len(tags_list[key][idx]) == 31:
                res[key].append(tags_list[key][idx])
    return res

def get_bridges_from_csv(csv_filepath):
    """
        :type csv_filepath: string
        :param csv_filepath: bridges names csv file path
    """
    if csv_filepath is None:
        return None
    bridges_df = pd.read_csv(csv_filepath)
    zones_dict = bridges_df.to_dict('list')
    return zones_dict

# Date & Time Related
def convert_datetime_to_timestamp(year=2022, month=1, day=1, hour=0, minute=0, seconds=0, micro_secs=0,
                                hours_from_utc=0):
    """
    returns the timestamp of Israeli datetime
    :type year: int
    :param year: year of desired datetime
    :type month: int
    :param month: month of desired datetime
    :type day: int
    :param day: day of desired datetime
    :type hour: int
    :param hour: hour of desired datetime
    :type minute: int
    :param minute: minute of desired datetime
    :type seconds: int
    :param seconds: seconds of desired datetime
    :type micro_secs: int
    :param micro_secs: micro seconds of desired datetime
    :type hours_from_utc: int
    :param hours_from_utc: hours difference from UTC timezone
    :returns: timestamp in UTC
    """

    dt = datetime.datetime(year, month, day, hour, minute, seconds, micro_secs)
    # getting the timestamp
    ts = datetime.datetime.timestamp(dt)
    # if runs in data bricks - subtract hours_from_utc hours to transfer to relevant time zone
    if is_databricks():
        ts = ts - 3600 * hours_from_utc
    # convert to ms
    ts_in_ms = math.ceil(ts * 1000)
    return ts_in_ms

def mstimestamp_to_timezone(timestamp, timezone='Israel', milli=True, hour=True, return_datetime=False):
    """
    :type timestamp: float / str / int
    :param timestamp: millisecond timestamp
    :type timezone: str
    :param timezone: ZoneInfo Timestamp name, defaults to Israel
    :type milli: bool
    :param milli: if false, omits millisecond from result
    :type return_datetime: bool
    :param return_datetime: whether to return datetime
    :rtype: str | datetime
    :return: String of datetime in timezone | datetime object in timezone
    """
    server_timezone = ZoneInfo("Etc/UTC")
    chosen_timezone = ZoneInfo(timezone)
    if timestamp == 0 or np.isnan(timestamp):
        return None
    try:
        timestamp = float(timestamp)
    except ValueError as e:
        raise ValueError(f'Timestamp {timestamp} could not be converted to float!' + e)
    dt = datetime.datetime.fromtimestamp(timestamp / 1000)
    dt.replace(tzinfo=server_timezone)
    if return_datetime:
        return dt.astimezone(chosen_timezone)
    if hour:
        if milli:
            dt = dt.astimezone(chosen_timezone).strftime('%Y-%m-%d %H:%M:%S.%f %Z')
        else:
            dt = dt.astimezone(chosen_timezone).strftime('%Y-%m-%d %H:%M:%S %Z')
    else:
        dt = dt.astimezone(chosen_timezone).strftime('%Y-%m-%d')
    return dt

def convert_timestamp_to_datetime(timestamp, up_to_sec_res=False):
    """
    converts timestamp to datetime
    :param timestamp: timestamp
    :type timestamp: str
    :param up_to_sec_res: if true will return the datetime in a resolution of seconds
    :type up_to_sec_res: bool
    """
    num_digits = len(str(int(float(timestamp))))
    timestamp = float(timestamp)
    timestamp = timestamp * math.pow(10, ((num_digits*-1) + 10))
    dt = datetime.datetime.fromtimestamp(float(timestamp))
    if up_to_sec_res:
        dt = dt - datetime.timedelta(microseconds=dt.microsecond)
    return dt

def datetime_to_timezone(dt, timezone='Israel'):
    return dt.astimezone(ZoneInfo(timezone))


def current_timestamp():
    """returns current timestamp (UTC) in milliseconds"""
    return datetime.datetime.timestamp(datetime.datetime.now()) * 1000


def timestamp_timedelta(method=False, **kwargs):
    now = datetime.datetime.now()
    if method:
        calc = now + datetime.timedelta(**kwargs)
    else:
        calc = now - datetime.timedelta(**kwargs)
    return calc.timestamp() * 1000


def string_to_bool(string):
    if string == 'True':
        return True
    if string == 'False':
        return False
    else:
        raise ValueError('Value not equal to True or False!')


def filter_namedtuple(namedtuple, keys, val_type=int):
    """
    gets named tuple (from DataFrame.itertuples) and returns a dictionary of filtered keys from named tuple,
    filtering out keys which have NaN values
    :type namedtuple: Named Tuple
    :param namedtuple: named tuple to filter
    :type keys: list
    :param keys: keys to filter from named tuple
    :rtype: dict
    :return: dictionary of keys and values filtered from named tuple
    """
    d = dict()
    for k in keys:
        try:
            val = getattr(namedtuple, k)
            if pd.isna(val):
                continue
            if str(val).replace('.', '').isnumeric():
                val = val_type(val)
            d[k] = val
        except AttributeError:
            continue
    return d


def parse_si_packet(df):
    def from_twos_complement(value):
        if value>(pow(2,7)):
            return value-(1<<8)
        else:
            return value
    
    df['band'] = df.rawPacket.apply(lambda x: x[16:18])=="01"
    dfn = pd.DataFrame()
    # add column of output power
    for band in df['band'].unique():
        tmp = df[df['band']==band]
        if band:  # sub1g is 8 bit positive number
            tmp = tmp.assign(tx_outputpower=tmp.rawPacket.apply(lambda x: int(x[14:16], 16)))
        else:  # ble is 8 bit negative 2's complement number
            tmp = tmp.assign(tx_outputpower=tmp.rawPacket.apply(lambda x: from_twos_complement(int(x[14:16], 16))))
        dfn = pd.concat([dfn, tmp])
    # add columns of tx and rx antena
    df['tx_ant'] = df.rawPacket.apply(lambda x: x[18:20])
    df['rx_ant'] = df.rawPacket.apply(lambda x: x[20:22])
    df['rssi'] = -df['rssi']
    return df


def match_bridge_ids(bridge_ids, alias_bridge_ids):
    # Convert hex IDs to integers
    bridge_ints = {bid: int(bid, 16) for bid in bridge_ids}
    alias_ints = {abid: int(abid, 16) for abid in alias_bridge_ids}
    matches = {}
    for alias, alias_int in alias_ints.items():
        cnt = 0
        for bridge, bridge_int in bridge_ints.items():
            # Check if aliasBridgeId matches bridgeId exactly, or with the first bit modified
            if (alias_int == bridge_int or  alias_int == (bridge_int | 0xC00000000000)): 
                cnt = cnt + 1
                matches[alias] = bridge
        if alias not in matches:
            matches[alias] = None
    return matches