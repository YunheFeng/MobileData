from shapely.geometry import LineString, Point

from common import *

def line_dist(boundary1, boundary2):
    line1 = LineString([boundary1[0], boundary1[1]])
    line2 = LineString([boundary2[0], boundary2[1]])
    l_dist = line1.distance(line2)

    return l_dist

def boundary_dist(tower_pair1, tower_pair2, boundaries, calculated_pairs):
    dist = None
    if (tower_pair1, tower_pair2) in calculated_pairs:
        dist = calculated_pairs[(tower_pair1, tower_pair2)]
    elif (tower_pair2, tower_pair1) in calculated_pairs:
        dist = calculated_pairs[(tower_pair2, tower_pair1)]
    elif tower_pair1 in boundaries and tower_pair2 in boundaries:
        dist = line_dist(boundaries[tower_pair1], boundaries[tower_pair2])
        calculated_pairs[(tower_pair1, tower_pair2)] = dist

    return dist

def adj_site_dist(tower_pair, adjacent_sites, boundaries, calculated_pairs):
    ''' For consecutive records that are in disadjacent towers

    Find the nearest pair of boundaries of src/dst tower
    return the distance between, and both boundaries
    '''

    # dont need to half the distance for consistancy anymore
    min_dist = None
    for site_src in adjacent_sites[tower_pair[0]]:
        for site_dst in adjacent_sites[tower_pair[1]]:
            dist = boundary_dist(site_src, site_dst, boundaries, calculated_pairs)
            if min_dist == None or dist < min_dist:
                min_dist = dist
                adj_site_src = site_src
                adj_site_dst = site_dst

    return min_dist, adj_site_src, adj_site_dst


def calc_dist(compressed_sessions, boundaries):
    '''calculate distance lower bound and estimated distance

    since we are not including cross boundary gaps in the duration 
    of cross the tower, so we only calculate the path in the tower
    range when using virtual boundaries

    calculate the dist_lb and jump_dist (for disadjacent boundaries)
    '''

    cnt = 0
    # buffer to avoid repeating calculations
    calculated_pairs = {}

    # collect boundaries by towers
    # so that if we know a tower, we know all its boundaries
    adjacent_sites = {}
    for tower_pair in boundaries:
        if tower_pair[0] not in adjacent_sites:
            adjacent_sites[tower_pair[0]] = []
        adjacent_sites[tower_pair[0]].append(tower_pair)
        if tower_pair[1] not in adjacent_sites:
            adjacent_sites[tower_pair[1]] = []
        adjacent_sites[tower_pair[1]].append(tower_pair)

    for compressed_session in compressed_sessions:
        for agg_record in compressed_session:
            if agg_record.io[0] != None and agg_record.io[1] != None:
                if agg_record.io[0] < agg_record.pos:
                    tower_pair1 = (agg_record.io[0], agg_record.pos)
                else:
                    tower_pair1 = (agg_record.pos, agg_record.io[0])
                if agg_record.io[1] < agg_record.pos:
                    tower_pair2 = (agg_record.io[1], agg_record.pos)
                else:
                    tower_pair2 = (agg_record.pos, agg_record.io[1])

                dist = boundary_dist(tower_pair1, tower_pair2, boundaries, calculated_pairs)
                if dist != None:
                    # only contains real boundary
                    agg_record.dist_lb = dist
                    adj_pair1 = tower_pair1
                    adj_pair2 = tower_pair2
                else:
                    # contains virtual boundary
                    tower_pair1_dist = None
                    tower_pair2_dist = None
                    between_boundary_dist = None

                    if tower_pair1 not in boundaries:
                        tower_pair1_dist, tower_pair1_src, tower_pair1_dst = \
                                adj_site_dist(tower_pair1, adjacent_sites, \
                                boundaries, calculated_pairs)
                    else:
                        tower_pair1_dist = None
                        tower_pair1_src = tower_pair1
                        tower_pair1_dst = tower_pair1

                    if tower_pair2 not in boundaries:
                        tower_pair2_dist, tower_pair2_src, tower_pair2_dst = \
                                adj_site_dist(tower_pair2, adjacent_sites, \
                                boundaries, calculated_pairs)
                    else:
                        tower_pair2_dist = None
                        tower_pair2_src = tower_pair2
                        tower_pair2_dst = tower_pair2

                    if agg_record.io[0] < agg_record.pos:
                        adj_pair1 = tower_pair1_dst
                    else:
                        adj_pair1 = tower_pair1_src
                    if agg_record.io[1] < agg_record.pos:
                        adj_pair2 = tower_pair2_dst
                    else:
                        adj_pair2 = tower_pair2_src

                    between_boundary_dist = boundary_dist(adj_pair1, adj_pair2, \
                            boundaries, calculated_pairs)
                    if between_boundary_dist != None:
                        agg_record.dist_lb = between_boundary_dist

                    if tower_pair1_dist != None:
                        if tower_pair1_dist == 0:
                            tower_pair1_dist = None
                    if tower_pair2_dist != None:
                        if tower_pair2_dist == 0:
                            tower_pair2_dist = None
                    agg_record.jump_dist = (tower_pair1_dist, tower_pair2_dist)

                # covert dot distance to kilo meter
                prior_dist = coordinate_dist(adj_pair1[0], adj_pair1[1])
                post_dist = coordinate_dist(adj_pair2[0], adj_pair2[1])
                agg_record.dist_est = (prior_dist + post_dist) / 2

                # discard the voronoi distance error
                if agg_record.dist_lb > agg_record.dist_est:
                    agg_record.dist_lb = 0

        # fill in the jump dist for first and last one
        compressed_session[0].jump_dist = \
                (None, compressed_session[1].jump_dist[0])
        compressed_session[-1].jump_dist = \
                (compressed_session[-2].jump_dist[1], None)

def speed_estimation(compressed_sessions, rules):
    ''' estimate the speed

    both distance and time could be inaccurate.
    so the speed is not a value but a range.
    the more strict the range is, the more accurate the estimation is.
    '''

    compressed_sessions = raw_speed_estimation(compressed_sessions)
    # compressed_sessions = speed_consistency(compressed_sessions, rules)
    return compressed_sessions

def raw_speed_estimation(compressed_sessions):
    ''' estimate the speed use real boundaries (adjacent tower)

    speed is a range [dist_lb / loose_duration, dist_est / strict_duration]
    where loose duration is the last record time of previous tower and 
    first record time of next tower.
    '''

    # in case duration is 0
    security_minimum = 0.000001

    # estimate speed for every pair of strict boundaries
    for compressed_session in compressed_sessions:
        buff_begin = None
        buff_end = None
        for index, agg_record in enumerate(compressed_session):
            if agg_record.io[0] != None and agg_record.jump_dist[0] == None:
                if buff_begin != None:
                    buff_end = index
                    dist_est_sum = 0
                    dist_lb_sum = 0
                    for buff_ix in range(buff_begin, buff_end):
                        # use same jump for est and lb, might not be accurate
                        dist_est_sum += compressed_session[buff_ix].dist_est 
                        dist_lb_sum += compressed_session[buff_ix].dist_lb 
                        if buff_ix < buff_end - 1:
                            dist_est_sum += \
                                    compressed_session[buff_ix].jump_dist[1] 
                            dist_lb_sum += \
                                    compressed_session[buff_ix].jump_dist[1] 

                    prev_record = compressed_session[buff_begin - 1]
                    begin_record = compressed_session[buff_begin]
                    end_record = compressed_session[buff_end - 1]
                    next_record = compressed_session[buff_end]
                    strict_dur = end_record.duration[1] - \
                            begin_record.duration[0] + security_minimum
                    # add a larger min to ensure fail the rule
                    loose_dur = next_record.duration[0] - \
                            prev_record.duration[1] + security_minimum * 10

                    speed_est_avg = dist_est_sum / \
                            ((strict_dur + loose_dur) / 2) * 3600 # km/h
                    speed_lb_avg = dist_lb_sum / loose_dur * 3600 # km/h
                    for buff_ix in range(buff_begin, buff_end):
                        compressed_session[buff_ix].speed = \
                                (speed_lb_avg, speed_est_avg)
                        compressed_session[buff_ix].strict_dur = strict_dur
                        compressed_session[buff_ix].loose_dur = loose_dur
                buff_begin = index

    return compressed_sessions


def check_record(record):
    if record == None:
        return False
    elif record.speed == (None, None):
        return False
    else:
        return True

def speed_consistency(compressed_sessions, rules):
    ''' for records in each tower, find compensate

    this is useful when the a tower has very loose estimated speed range 
    find a near (bound by time) tower with suffcient long duration and 
    strict speed range to help estimate the speed of the user
    '''
    for compressed_session in compressed_sessions:
        front = 0 # The first element that have not processed
        rare = 0 
        front_record = None # front landmark
        rare_record = None # rare landmark
        for index, agg_record in enumerate(compressed_session):
            if agg_record.dist_lb == None:
                continue
            if front_record == None or \
                    front_record.duration[0] < agg_record.duration[1]:
                # not exist or expired
                front_record = None
                #catch up
                while(front < len(compressed_session) and \
                        compressed_session[front].duration[0] < \
                        agg_record.duration[1]):
                    front += 1
                while(front < len(compressed_session) and \
                        compressed_session[front].duration[0] - \
                        agg_record.duration[1] <= rules.sc_window_len):
                    # in the window
                    temp_record = compressed_session[front]
                    if temp_record.duration[1] - \
                            temp_record.duration[0] >= rules.sc_dur_req:
                        # longer than duration requirement
                        front_record = temp_record
                        break
                    else:
                        front += 1

            if rare_record == None or \
                    agg_record.duration[0] - \
                    rare_record.duration[1] >= rules.sc_window_len:
                # not exist or expired
                rare_record = None
                while(rare < index and agg_record.duration[0] - \
                        compressed_session[rare].duration[1] > \
                        rules.sc_window_len):
                    rare += 1
                while(rare < index and \
                        compressed_session[rare].duration[1] <= \
                        agg_record.duration[0]):
                    temp_record = compressed_session[rare]
                    if temp_record.duration[1] - \
                            temp_record.duration[0] >= rules.sc_dur_req:
                        rare_record = temp_record
                        break
                    else:
                        rare += 1

            if check_valid(front_record, rules) == False:
                front_record = None
            if check_valid(rare_record, rules) == False:
                rare_record = None
            
            if front_record != None and rare_record != None:
                agg_record.compensate_speed = combine_speed_range(\
                        front_record.speed, rare_record.speed)
            if front_record != None and rare_record == None:
                agg_record.compensate_speed = front_record.speed
            elif rare_record != None and front_record == None:
                agg_record.compensate_speed = rare_record.speed

    return compressed_sessions

def check_valid(agg_record, rules):
    if agg_record == None:
        return False
    if agg_record.dist_lb == None:
        return False
    if agg_record.speed == (None, None):
        return False
    if agg_record.dist_est == 0:  
        # strange error due to the trace, ignore
        return False
    if agg_record.dist_lb / agg_record.dist_est < \
            rules.cv_dist_ratio_threshold:
        return False
    if agg_record.strict_dur / agg_record.loose_dur < \
            rules.cv_duration_ratio_threshold:
        return False
    return True

def get_speed(agg_record, rules):
    speed_lb = None
    speed_est  = None

    if check_valid(agg_record, rules) == True:
        speed_lb, speed_est = combine_speed_range(\
                agg_record.speed, agg_record.compensate_speed)
    else:
        speed_lb = agg_record.compensate_speed[0]
        speed_est = agg_record.compensate_speed[1]

    if speed_lb == None or speed_est == None:
        return None

    return (speed_lb, speed_est)

def combine_speed_range(sr1, sr2):
    if sr2 == (None, None):
        return sr1
    if sr1 == (None, None):
        return sr2

    if sr1[0] <= sr2[1] and sr2[0] <= sr1[1]:
        # range agree
        speed_lb = max(sr1[0], sr2[0])
        speed_est = min(sr1[1], sr2[1])
        speed_range = (speed_lb, speed_est)
    else:
        # range disagree
        speed_range = sr1

    return speed_range
