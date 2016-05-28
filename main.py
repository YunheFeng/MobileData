import sys
import cPickle as pickle
import argparse
import operator

from common import *

import preprocessing as pp
import voronoi as vor
import speedest as se
import analysis as an

def combine_all_city():
    sessions_xuzhou = pickle.load(open(\
                'results/check_points/sessions_xuzhou.txt', 'rb'))
    sessions_yancheng = pickle.load(open(\
                'results/check_points/sessions_yancheng.txt', 'rb'))
    sessions_taizhou = pickle.load(open(\
                'results/check_points/sessions_taizhou.txt', 'rb'))
    compressed_sessions_xuzhou = pickle.load(open(\
            'results/check_points/comp_sessions_xuzhou.txt', 'rb'))
    compressed_sessions_yancheng = pickle.load(open(\
            'results/check_points/comp_sessions_yancheng.txt', 'rb'))
    compressed_sessions_taizhou = pickle.load(open(\
            'results/check_points/comp_sessions_taizhou.txt', 'rb'))

    sessions = sessions_xuzhou + sessions_yancheng + sessions_taizhou
    compressed_sessions = compressed_sessions_xuzhou + \
            compressed_sessions_yancheng + compressed_sessions_taizhou 

    return sessions, compressed_sessions

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('city', type=str)
    arg_parser.add_argument('run_type', type=str)
    args = arg_parser.parse_args()
    # setup parameters
    city = args.city 
    rules = Rules(\
            pc_window_len = 60, \
            pc_density = 10, \
            pf_range_filter = get_range_filter(city), \
            pf_min_tower = 3, \
            sc_window_len = 60, \
            sc_dur_req = 300, \
            cv_dist_ratio_threshold = 0.6, \
            cv_duration_ratio_threshold = 0.6, \
            ) 
    # check points file names
    session_fn = 'results/check_points/sessions_{0}.txt'.format(city)
    compressed_session_fn = \
            'results/check_points/comp_sessions_{0}.txt'.format(city)

    if args.run_type == '1':
        print '\n::::::::::::::::Estimate Speed:::::::::::::::::\n'
        print '1. Preprocess data'
        # a session means whole data access of each user
        sessions, towers = pp.parse_traces('datasets/all_city/{0}'.format(city)) 
        sessions = pp.pre_filter(sessions, rules)
        # sessions are compressed to each tower
        compressed_sessions = pp.session_compression(sessions)

        print '2. Stimulate tower boundaries with Voronoi map'
        vmap = vor.voronoi_map(towers, city)
        vmap.equirectangular_projection()
        boundaries = vmap.calc_boundaries()
        sessions, compressed_sessions = \
                vmap.clean_excluded_data(sessions, compressed_sessions)

        print '3. Estimate distance lower bound based on tower boundaries'
        se.calc_dist(compressed_sessions, boundaries)

        print '4. Estimate speed range'
        se.speed_estimation(compressed_sessions, rules) 
        # an.estimated_speed_basic_analysis(compressed_sessions, rules)

        print '5. Output estimation results:'
        print '\t{0}'.format(session_fn)
        print '\t{0}'.format(compressed_session_fn)
        pickle.dump(sessions, open(session_fn, 'wb'))
        pickle.dump(compressed_sessions, open(compressed_session_fn, 'wb'))
        print ''

    elif args.run_type == '2':
        print '\n::::::::::::Calculate Speed and Usage Correlation:::::::::::::\n'
        print '1. Load check points (sessions, compressed sessions)'
        compressed_sessions = pickle.load(open(compressed_session_fn, 'rb'))
        compressed_sessions = se.speed_consistency(compressed_sessions, rules)

        print '2. Calculate correlations'
        speed_appcat_stat = \
                an.gather_speed_appcat_stat(compressed_sessions, rules)

        print '3. Output correlation results:'
        speed_appcat_cor_fn = 'results/speed_appcat_{0}.txt'.format(city)
        print '\t{0}'.format(speed_appcat_cor_fn)
        print ''
        # appcat_filter = [1, 2, 3, 4, 5, 6, 7, 15]
        appcat_filter = [(1,9), (2,20), (3,2), (4,3), (5,3), (6,2), (7,3), (15,3)]
        an.speed_appcat_analysis(speed_appcat_stat, \
                appcat_filter, speed_appcat_cor_fn)
        print ''

    elif args.run_type == '0' and city == 'all_city':
        print '\n::::::::::::::::Combine Multiple Cities:::::::::::::::::\n'
        sessions, compressed_sessions = combine_all_city();
        an.session_basic_analysis(sessions)
        pickle.dump(sessions, open(session_fn, 'wb'))
        pickle.dump(compressed_sessions, open(compressed_session_fn, 'wb'))
        print '\t{0}'.format(session_fn)
        print '\t{0}'.format(compressed_session_fn)
        print ''

    elif args.run_type == '-1':
        print '\n::::::::::::::::Special Topics:::::::::::::::::\n'
        print 'For city: ', city
        # sessions = pickle.load(open(session_fn, 'rb'))
        compressed_sessions = pickle.load(open(compressed_session_fn, 'rb'))
        an.speed_filter_analysis(compressed_sessions, rules)
        # compressed_sessions = se.speed_consistency(compressed_sessions, rules)
        # an.speed_usage_pattern_analysis(sessions, compressed_sessions, rules)
        # an.gap_distribution_analysis(sessions, compressed_sessions, rules)
        # an.time_interval_analysis(sessions, city)
        # an.example_user_analysis(sessions, compressed_sessions)
        print ''

    else:
        print '\n::::::::::::::::Invalid Run Type:::::::::::::::::\n'


