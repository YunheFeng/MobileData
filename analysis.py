from speedest import get_speed

max_bin_cnt = 20
max_detailed_bin_cnt = 200
max_speed_bin_cnt = 8
speed_per_bin = 20

def session_basic_analysis(sessions):
    print '-------Session Basic Analysis-------'
    session_cnt = len(sessions)
    record_cnt = 0
    total_dur = 0
    total_vol = 0
    record_per_bin = 10
    record_cnt_dist = [0] * max_bin_cnt
    dur_per_bin = 360
    duration_dist = [0] * max_bin_cnt

    for session in sessions:
        record_cnt += len(session)
        total_dur += session[-1].time - session[0].time
        for record in session:
            total_vol += record.vol

        record_cnt_index = min(len(session) / record_per_bin, max_bin_cnt - 1)
        record_cnt_dist[record_cnt_index] += 1

        duration = session[-1].time - session[0].time
        duration_index = min(int(duration / dur_per_bin), max_bin_cnt - 1)
        duration_dist[duration_index] += 1

    print 'Number of sessions: {0}'.format(session_cnt)
    print 'Number of records: {0}'.format(record_cnt)
    print 'Total active time: {0}'.format(total_dur)
    print 'Total volume of data access: {0}'.format(total_vol)
    print 'Session record count distribution ({0} records per bin):'.format(\
            record_per_bin)
    print record_cnt_dist
    print 'Session duration distribution ({0} seconds per bin):'.format(\
            dur_per_bin)
    print duration_dist
    print ''

def data_access_analysis(sessions, city):
    print '-------Data Access Analysis-------'
    da_fn = 'results/data_access_{0}.txt'.format(city)
    with open(da_fn, 'w') as da:
        for session in sessions:
            da.write('{0}\n'.format(len(session)))

def app_category_analysis(sessions):
    print '-------App Category Analysis-------'
    app_session_cnt = {}
    app_record_cnt = {}
    app_vol = {}
    for session in sessions:
        session_mask =  set()
        for record in session:
            app_cat = int(record.app_cat[0])
            if app_cat not in app_record_cnt:
                app_record_cnt[app_cat] = 0
            app_record_cnt[app_cat] += 1
            if app_cat not in app_vol:
                app_vol[app_cat] = 0
            app_vol[app_cat] += record.vol
            session_mask.add(app_cat)
        for app_cat in session_mask:
            if app_cat not in app_session_cnt:
                app_session_cnt[app_cat] = 0
            app_session_cnt[app_cat] += 1
    
    print 'Apps total record count, vol and user count'
    for app_cat in app_record_cnt:
        print app_cat, app_record_cnt[app_cat], app_vol[app_cat], app_session_cnt[app_cat]

def example_user_analysis(sessions, compressed_sessions):
    print '-------Example User Analysis-------'
    eu_fn = 'results/example_user.txt'
    with open(eu_fn, 'w') as euf:
        for session, compressed_session in zip(sessions, compressed_sessions):
            tower_set = set()
            for record in session:
                tower_set.add(record.pos)
            if len(tower_set) > 4 and \
                    len(compressed_session) == 7 and \
                    len(session) > 70:
                for record in session:
                    euf.write('{0} {1} {2}\n'.format(record.time, \
                            record.pos[0], record.pos[1]))
                break


def wired_point_analysis(sessions):
    print '-------Wired Point Analysis-------'
    vol_per_bin = 1000
    vol_dist = [0] * max_bin_cnt
    vol_max = 0
    vol_min = 100000000000
    for session in sessions:
        for record in session:
            if record.app_cat[0] != 7:
                continue
            index = min(int(record.vol / vol_per_bin), max_bin_cnt - 1)
            vol_dist[index] += 1
            if record.vol > vol_max:
                vol_max = record.vol
            if record.vol < vol_min:
                vol_min = record.vol

    print 'Volume maximum:', vol_max
    print 'Volume minimum:', vol_min
    print 'Volume distribution:'
    print vol_dist

def compressed_session_basic_analysis(compressed_sessions):
    print '-------Compressed Session Basic Analysis-------'
    compressed_session_cnt = len(compressed_sessions)
    record_cnt = 0
    total_vol = 0
    travelled_tower_dist = [0] * max_bin_cnt

    for compressed_session in compressed_sessions:
        travelled_towers = set()
        for agg_record in compressed_session:
            record_cnt += agg_record.record_cnt
            for app_grp in agg_record.app_access:
                total_vol += agg_record.app_access[app_grp]
            travelled_towers.add(agg_record.pos)

        travelled_tower_index = min(len(travelled_towers), max_bin_cnt - 1)
        travelled_tower_dist[travelled_tower_index] += 1

    print 'Number of compressed sessions: {0}'.format(compressed_session_cnt)
    print 'Number of records: {0}'.format(record_cnt)
    print 'Total volume of data access: {0}'.format(total_vol)
    print 'User number of travelled towers distribution:'
    print travelled_tower_dist
    print ''

def estimated_speed_basic_analysis(compressed_sessions, rules):
    print '-------Estimated Speed Basic Analysis-------'
    # all unit are in number of records
    record_cnt = 0
    record_wlb_cnt = 0
    record_wzerolb_cnt = 0
    record_westspeed_cnt = 0
    record_wcompensatespeed_cnt = 0
    record_wspeed_cnt = 0
    speed_per_bin = 8
    speed_est_dist = [0] * max_bin_cnt
    speed_lb_dist = [0] * max_bin_cnt
    speed_ratio_dist = [0] * max_bin_cnt
    speed_diff_per_bin = 5
    speed_diff_dist = [0] * max_bin_cnt
    speed_est_pass_dist = [0] * max_bin_cnt
    speed_lb_pass_dist = [0] * max_bin_cnt

    for compressed_session in compressed_sessions:
        for agg_record in compressed_session:
            record_cnt += agg_record.record_cnt

            if agg_record.dist_lb != None:
                record_wlb_cnt += agg_record.record_cnt
                if agg_record.dist_lb == 0:
                    record_wzerolb_cnt += agg_record.record_cnt

            if agg_record.speed != (None, None):
                record_westspeed_cnt += agg_record.record_cnt
                
            if agg_record.compensate_speed != (None, None):
                record_wcompensatespeed_cnt += agg_record.record_cnt

            if agg_record.speed != (None, None) or \
                    agg_record.compensate_speed != (None, None):
                record_wspeed_cnt += agg_record.record_cnt

            # for estimated speed only
            if agg_record.speed != (None, None):
                speed_est_index = min(int(agg_record.speed[1] /\
                        speed_per_bin), max_bin_cnt - 1)
                speed_est_dist[speed_est_index] += agg_record.record_cnt

                speed_lb_index = min(int(agg_record.speed[0] /\
                        speed_per_bin), max_bin_cnt - 1)
                speed_lb_dist[speed_lb_index] += agg_record.record_cnt

                if agg_record.speed[0] == 0:
                    # speed[1] cloud not be 0
                    speed_ratio_index = max_bin_cnt - 1
                else:
                    speed_ratio_index = min(int(agg_record.speed[1] /\
                            agg_record.speed[0]), max_bin_cnt - 1)
                speed_ratio_dist[speed_ratio_index] += agg_record.record_cnt

                speed_diff = agg_record.speed[1] - agg_record.speed[0]
                speed_diff_index = min(int(speed_diff / speed_diff_per_bin), \
                        max_bin_cnt - 1)
                speed_diff_dist[speed_diff_index] += agg_record.record_cnt

            speed_range = get_speed(agg_record, rules)
            if speed_range != None:
                speed_est_pass_index = min(int(speed_range[1] /\
                        speed_per_bin), max_bin_cnt - 1)
                speed_est_pass_dist[speed_est_pass_index] += \
                        agg_record.record_cnt

                speed_lb_pass_index = min(int(speed_range[0] /\
                        speed_per_bin), max_bin_cnt - 1)
                speed_lb_pass_dist[speed_lb_pass_index] += \
                        agg_record.record_cnt



    print 'NOR with distance lower bound: {0}'.format(record_wlb_cnt)
    print 'NOR with zero distance lower bound: {0}'.format(record_wzerolb_cnt)
    print 'NOR with estimated speed: {0}'.format(record_westspeed_cnt)
    print 'NOR with compensate speed: {0}'.format(record_wcompensatespeed_cnt)
    print 'NOR with either speed: {0}'.format(record_wspeed_cnt)
    print 'Estimated speed distribution ({0} km/h per bin):'.format(\
            speed_per_bin)
    print speed_est_dist
    print 'Speed lower bound distribution ({0} km/h per bin):'.format(\
            speed_per_bin)
    print speed_lb_dist
    print 'Speed ratio distribution:'
    print speed_ratio_dist
    print 'Speed difference distribution ({0} km/h per bin):'.format(\
            speed_diff_per_bin)
    print speed_diff_dist
    print 'Passed estimated speed distribution ({0} km/h per bin):'.format(\
            speed_per_bin)
    print speed_est_pass_dist
    print 'Passed speed lower bound distribution ({0} km/h per bin):'.format(\
            speed_per_bin)
    print speed_lb_pass_dist
    print ''

def time_interval_analysis(sessions, city):
    print '-------Time Interval Analysis-------'
    ti_fn = 'results/time_interval_{0}.txt'.format(city)
    with open(ti_fn, 'w') as tif:
        for session in sessions:
            last_record = None
            for record in session:
                if last_record != None:
                    tif.write('{0}\n'.format(record.time - last_record.time))
                last_record = record

def speed_record_analysis(compressed_sessions, rules):
    print '-------Speed Record Analysis-------'
    speed_record_total = 0
    speed_record_filtered_total = 0
    speed_record_dist = [0] * max_detailed_bin_cnt 
    speed_record_filtered_dist = [0] * max_detailed_bin_cnt 
    for compressed_session in compressed_sessions:
        for agg_record in compressed_session:
            speed_range = get_speed(agg_record, rules)
            if speed_range == None:
                if agg_record.speed != (None, None):
                    speed_est = min(agg_record.speed[1], \
                            max_detailed_bin_cnt - 1)
                    speed_record_filtered_total += agg_record.record_cnt
                    speed_record_filtered_dist[int(speed_est)] += \
                            agg_record.record_cnt
            else:
                speed_est = speed_range[1]
                if speed_est > max_detailed_bin_cnt - 1:
                    continue
                speed_record_total += agg_record.record_cnt
                speed_record_dist[int(speed_est)] += agg_record.record_cnt

    '''
    speed_record_dist = [item / float(speed_record_total) \
            for item in speed_record_dist]
    speed_record_filtered_dist = [item / float(speed_record_filtered_total) \
            for item in speed_record_filtered_dist]
    '''

    print 'Number of records that have speed estimates: {0}'.\
            format(speed_record_total)
    print 'Number of records that have been filtered: {0}'.\
            format(speed_record_filtered_total)
    print 'Distribution of speed estimates:'
    print speed_record_dist
    print 'Distribution of filtered speed estimates:'
    print speed_record_filtered_dist

def speed_usage_pattern_analysis(sessions, compressed_sessions, rules):
    print '-------Speed Usage Pattern Analysis-------'
    speed_gap_dist = []
    speed_vol_dist = []
    speed_gap_sum_dist = [0] * max_speed_bin_cnt
    speed_vol_sum_dist = [0] * max_speed_bin_cnt
    speed_cnt_dist = [0] * max_speed_bin_cnt

    for session, compressed_session in zip(sessions, compressed_sessions):
        index = 0
        agg_record = None
        speed = None
        last_record = None
        last_record_speed = None
        for record in session:
            while agg_record == None or agg_record.ID != record.agg_ID:
                agg_record = compressed_session[index]
                speed_range = get_speed(agg_record, rules)
                if speed_range != None:
                    speed = speed_range[1]
                else:
                    speed = None
                index += 1
            if last_record_speed != None and speed != None and \
                    last_record_speed == speed:
                speed_index = int(speed / speed_per_bin)
                if speed_index > max_speed_bin_cnt - 1:
                    continue
                speed_gap_sum_dist[speed_index] += \
                        record.time - last_record.time
                speed_vol_sum_dist[speed_index] += record.vol
                speed_cnt_dist[speed_index] += 1

            last_record = record
            last_record_speed = speed

    for vol_sum, gap_sum, cnt in zip(\
            speed_vol_sum_dist, speed_gap_sum_dist, speed_cnt_dist):
        if cnt != 0:
            speed_gap_dist.append(gap_sum / cnt)
            speed_vol_dist.append(vol_sum / cnt)
        else:
            print gap_sum
            speed_gap_dist.append(0)

    print 'Distribution of gaps for various speed:'
    print speed_gap_dist
    print 'Distribution of vols for various speed:'
    print speed_vol_dist

def gap_distribution_analysis(sessions, compressed_sessions, rules):
    print '-------Gap Distribution Analysis-------'
    speed_per_file = 20

    with open('20_gap.txt', 'w') as file20, \
            open('40_gap.txt', 'w') as file40, \
            open('60_gap.txt', 'w') as file60, \
            open('80_gap.txt', 'w') as file80, \
            open('100_gap.txt', 'w') as file100:
        filelist = [file20, file40, file60, file80, file100]
        for session, compressed_session in zip(sessions, compressed_sessions):
            index = 0
            agg_record = None
            speed = None
            last_record = None
            last_record_speed = None
            for record in session:
                while agg_record == None or agg_record.ID != record.agg_ID:
                    agg_record = compressed_session[index]
                    speed_range = get_speed(agg_record, rules)
                    if speed_range != None:
                        speed = speed_range[1]
                    else:
                        speed = None
                    index += 1
                if last_record_speed != None and speed != None \
                        and last_record_speed == speed:
                    speed_index = min(int(speed/speed_per_file),4)
                    gap = record.time - last_record.time
                    filelist[speed_index].write( \
                            '{0}\n'.format(gap))
                last_record = record
                last_record_speed = speed

def gather_speed_appcat_stat(compressed_sessions, rules):
    speed_appcat_stat = {}
    for compressed_session in compressed_sessions:
        for agg_record in compressed_session:
            speed_range = get_speed(agg_record, rules)
            if speed_range == None:
                continue
            speed_est = speed_range[1]

            for app_cat in agg_record.app_access_cnt:
                if app_cat not in speed_appcat_stat:
                    speed_appcat_stat[app_cat] = []
                speed_appcat_stat[app_cat].append((speed_est, \
                        agg_record.app_access_cnt[app_cat], \
                        agg_record.app_access_vol[app_cat], \
                        agg_record.duration[1] - agg_record.duration[0]))

    return speed_appcat_stat

def speed_appcat_analysis(\
        speed_appcat_stat, appcat_filter, speed_appcat_cor_fn):
    print '-------Appcat Speed Analysis-------'
    speed_appcat_record_sum = {}
    speed_appcat_vol_sum = {}
    speed_appcat_duration = {}
    speed_allcat_record_sum = [0] * max_speed_bin_cnt
    speed_allcat_vol_sum = [0] * max_speed_bin_cnt
    speed_allcat_duration = [0] * max_speed_bin_cnt

    appcat_index = 0
    for app_cat in speed_appcat_stat:
        if appcat_index < len(appcat_filter) and \
                app_cat == appcat_filter[appcat_index]:
            speed_appcat_record_sum[app_cat] = [0] * max_speed_bin_cnt
            speed_appcat_vol_sum[app_cat] = [0] * max_speed_bin_cnt
            speed_appcat_duration[app_cat] = [0] * max_speed_bin_cnt
            appcat_index += 1

    with open(speed_appcat_cor_fn, 'w') as out:
        for app_cat in speed_appcat_stat:
            for agg_stat in speed_appcat_stat[app_cat]:
                index = int(agg_stat[0] / speed_per_bin)
                if index > max_speed_bin_cnt - 1:
                    continue
                if app_cat in speed_appcat_record_sum:
                    speed_appcat_record_sum[app_cat][index] += agg_stat[1]
                    speed_appcat_vol_sum[app_cat][index] += agg_stat[1]
                    speed_appcat_duration[app_cat][index] += agg_stat[3]
                speed_allcat_record_sum[index] += agg_stat[1]
                speed_allcat_vol_sum[index] += agg_stat[2]
                speed_allcat_duration[index] += agg_stat[3]

            if app_cat in speed_appcat_record_sum:
                for record_sum in speed_appcat_record_sum[app_cat]:
                    out.write('{0},'.format(record_sum))
                out.write('\n')

        print 'Speed record correlation:'
        for record_sum, duration in \
                zip(speed_allcat_record_sum, speed_allcat_duration):
            print record_sum,
        print ''

        print 'Speed volume correlation:'
        for vol_sum, duration in \
                zip(speed_allcat_vol_sum, speed_allcat_duration):
            print float(vol_sum) / duration,
        print ''

