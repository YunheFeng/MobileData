import math
import sys

def get_range_filter(city):
    if city == 'xuzhou':
        return (116.3125865, 118.5518742, 33.6544586, 35.0449691) # xuzhou
    elif city == 'yancheng':
        return (119.2390122, 121.0090342, 32.5371512, 34.4769842) # yancheng
    elif city == 'taizhou':
        return (119.6331762, 120.5933622, 31.9243942, 33.2172242) # taizhou
    elif city == 'fengxian':
        return (116.3125865, 118.5518742, 33.6544586, 35.0449691) # xuzhou
    else:
        return None

# basic data structure
class DataEntry:
    def __init__(self, time, pos, app_cat, vol):
        self.time = time # float
        self.pos = pos # tuple of float, lng and lat
        self.app_cat = app_cat # only the highest catogory
        self.vol = vol # int
        self.agg_ID = None # related agg_data_entry

class AggDataEntry:
    def __init__(self, ID, duration, pos, io, app_access_cnt, app_access_vol, record_cnt):
        self.ID = ID # a unique identifier
        self.duration = duration # tuple of float, start and end time
        self.pos = pos # tuple of float, lng and lat
        self.io = io # tuple of tuple of float, in and out tower
        self.app_access_cnt = app_access_cnt # dictionary of app_cat:cnt 
        self.app_access_vol = app_access_vol # dictionary of app_cat:vol 
        self.record_cnt = record_cnt # how many records
        self.dist_lb = None
        self.dist_est = None
        self.strict_dur = None
        self.loose_dur = None
        self.jump_dist = (None, None)
        self.speed = (None, None)
        self.compensate_speed = (None, None)

class WindowStat:
    def __init__(self):
        self.total = 0
        self.hash_table = {}

    def add(self, key, value):
        if key not in self.hash_table:
            self.hash_table[key] = 0
        self.hash_table[key] += value
        self.total += value

    def remove(self, key, value):
        self.hash_table[key] -= value
        if self.hash_table[key] == 0:
            del self.hash_table[key]
        self.total -= value

    def stat(self):
        max_cnt = 0
        max_key = None
        for key in self.hash_table:
            if self.hash_table[key] > max_cnt:
                max_cnt = self.hash_table[key]
                max_key = key
        ratio = float(max_cnt) / self.total
        return max_key, ratio

# basic data structure for rules
class Rules:
    def __init__(self, \
            pc_window_len, \
            pc_density, \
            pf_range_filter, \
            pf_min_tower, \
            sc_window_len, \
            sc_dur_req, \
            cv_dist_ratio_threshold, \
            cv_duration_ratio_threshold \
            ) :
        # preprocessing rules
        self.pc_window_len = pc_window_len
        self.pc_density = pc_density
        self.pf_range_filter = pf_range_filter
        self.pf_min_tower = pf_min_tower
        # speed rules
        self.sc_window_len = sc_window_len
        self.sc_dur_req = sc_dur_req
        self.cv_dist_ratio_threshold = cv_dist_ratio_threshold
        self.cv_duration_ratio_threshold = cv_duration_ratio_threshold

    def __eq__(self, other):
        if self.pc_window_len == other.pc_window_len and \
                self.pc_density == other.pc_density and \
                self.pf_range_filter == other.pf_range_filter and \
                self.pf_min_tower == other.pf_min_tower and \
                self.sc_window_len == other.sc_window_len and \
                self.sc_dur_req == other.sc_dur_req and \
                self.cv_dist_ratio_threshold == \
                other.cv_dist_ratio_threshold and \
                self.cv_duration_ratio_threshold == \
                other.cv_duration_ratio_threshold:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self == other

# parsing trace utility
def is_number(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

# various keys
def get_sort_key(item):
    return item.time

def get_app_group(record):
    return record.app_cat

# common functions
def coordinate_dist(pos1, pos2):
    if pos1 == pos2:
        return 0

    lat1 = pos1[1] * math.pi / 180
    lng1 = pos1[0] * math.pi / 180
    lat2 = pos2[1] * math.pi / 180
    lng2 = pos2[0] * math.pi / 180

    C = math.sin(lat1) * math.sin(lat2) + \
            math.cos(lat1) * math.cos(lat2) * math.cos(lng1 - lng2)
    R = 6371.004 # km, earth radiance
    dist = R * math.acos(C)

    return dist

