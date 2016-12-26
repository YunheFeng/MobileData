import os
import math
from collections import deque
from collections import OrderedDict
from copy import deepcopy

from common import *

def parse_traces(filename):
    ''' parse raw trace, save valid records for users and position for towers

    return record list as sessions, organized by user, sort by time
    return tower position list, (lng, lat), sort by position
    '''

    users = {}
    sessions = []
    towers = []
    for subdir, dirs, files in os.walk(filename):
        print subdir, ': ',
        for f in files:
            fn = os.path.join(subdir, f)
            sys.stdout.write('.')
            sys.stdout.flush()
            with open(fn) as curf:
                for line in curf:
                    segs = line.split(',')
                    if len(segs) != 18 \
                            or not is_number(segs[6]) \
                            or not is_number(segs[10]) \
                            or not is_number(segs[9]) \
                            or not is_number(segs[11]) \
                            or not is_number(segs[12]) \
                            or not is_number(segs[14]) \
                            or not is_number(segs[15]) :
                        continue
                    
                    # create variables
                    uid = segs[0]
                    # record: time, (lng, lat), (cat1, cat2), vol
                    # app_cat = int(segs[11])
                    app_cat = (int(segs[11]), int(segs[12]))
                    record = DataEntry(float(segs[6]), \
                            (float(segs[9]), float(segs[10])), \
                            app_cat, \
                            int(segs[14]) + int(segs[15]))
                            # float(segs[1]), float(segs[6]))

                    # add user records
                    if uid not in users:
                        users[uid] = []
                    users[uid].append(record)

                    # add towers
                    if record.pos not in towers:
                        towers.append(record.pos)

        print ''

        # sort record for each user by time
        for uid in users:
            sessions.append(sorted(users[uid], key=get_sort_key))

        # sort tower by position
        towers.sort()

    return sessions, towers

def check_in_range(session, rules):
    for record in session:
        if record.pos[0] < rules.pf_range_filter[0] or \
                record.pos[0] > rules.pf_range_filter[1]  or \
                record.pos[1] < rules.pf_range_filter[2] or \
                record.pos[1] > rules.pf_range_filter[3]:
            return False
    return True

def check_min_tower(session, rules):
    travelled_towers = set()
    for record in session:
        travelled_towers.add(record.pos)
    if len(travelled_towers) < rules.pf_min_tower:
        return False
    else:
        return True

def pre_filter(sessions, rules):
    ''' Filter records according to city range and minimum required towers

    delete unqualified session from session list
    user rule: pf_range_filter, pf_density
    '''

    sessions = [session for session in sessions \
            if check_in_range(session, rules) and \
            check_min_tower(session, rules)]

    return sessions

def special_filter(sessions):
    filtered_sessions = []
    for session in sessions:
        tower_list = set()
        for record in session:
            if record.pos not in tower_list:
                tower_list.add(record.pos)
        if len(tower_list) > 45:
            filtered_sessions.append(tower_list)

    return filtered_sessions

def make_agg_record(ID, start_record, end_record, last_tower_end_record, \
        record, app_access_cnt, app_access_vol, record_cnt):
    pos = start_record.pos
    in_tower = last_tower_end_record.pos
    out_tower = record.pos
    start_time = start_record.time
    end_time = end_record.time
    io = (in_tower, out_tower)
    duration = (start_time, end_time)
    agg_record = AggDataEntry(ID, duration, pos, io, \
            app_access_cnt, app_access_vol, record_cnt)

    return agg_record

def session_compression(sessions):
    ''' aggregate records according to tower for easy processing

    assign a aggregate ID to connect session with compressed session
    return compressed_session
    '''

    ID = 0
    compressed_sessions = []
    for session in sessions:
        compressed_session = []
        cur_tower = None
        end_record = DataEntry(None, None, None, None)
        record_cnt = 0
        # we dont count the first one and last one
        for record in session:
            if cur_tower != None and cur_tower != record.pos:
                agg_record = make_agg_record(ID, \
                        start_record, end_record, \
                        last_tower_end_record, record, \
                        app_access_cnt, app_access_vol, record_cnt)
                ID += 1
                compressed_session.append(agg_record)
            if cur_tower == None or cur_tower != record.pos:
                last_tower_end_record = end_record
                cur_tower = record.pos
                start_record = record
                app_access_cnt = {}
                app_access_vol = {}
                record_cnt = 0
            end_record = record
            if record.app_cat not in app_access_cnt:
                app_access_cnt[record.app_cat] = 0
                app_access_vol[record.app_cat] = 0
            app_access_cnt[record.app_cat] += 1 
            app_access_vol[record.app_cat] += record.vol
            record_cnt += 1
            record.agg_ID = ID
        # append last few agg_record to a single session
        record = DataEntry(None, None, None, None)
        agg_record = make_agg_record(ID, \
                start_record, end_record, \
                last_tower_end_record, record, \
                app_access_cnt, app_access_vol, record_cnt)
        ID += 1
        compressed_session.append(agg_record)

        # append to container
        compressed_sessions.append(compressed_session)

    return compressed_sessions

