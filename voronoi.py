import sys
import math
import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Point

from common import *

class voronoi_map:
    def __init__(self, towers, city):
        self.sites = {}
        self.towers = towers
        self.city = city
        self.included_towers = set()

    def equirectangular_projection(self):
        ''' Map the coordinates to the euclidean space for easy calculations

        Errors are less than 1% for all towers.
        Distance can be calculated with the Pythagoras' theorem now
        '''

        R = 6371.004

        min_lng = None
        max_lng = None
        min_lat = None
        max_lat = None

        for tower in self.towers:
            if min_lng == None or min_lng > tower[0]:
                min_lng = tower[0]
            if max_lng == None or max_lng < tower[0]:
                max_lng = tower[0]
            if min_lat == None or min_lat > tower[1]:
                min_lat = tower[1]
            if max_lat == None or max_lat < tower[1]:
                max_lat = tower[1]

        theta = (min_lat + max_lat) / 2 * math.pi / 180
        compensate = math.cos(theta)
        for tower in self.towers:
            phi = tower[0] * math.pi / 180
            epslon = tower[1] * math.pi / 180
            x = phi * compensate * R
            y = epslon * R
            self.sites[tower] = (x, y)

    def calc_boundaries(self):
        ''' Collect all ridges in the voronoi map as the boundary

        return boundary dictionary, tower:boundary_end_points
        '''

        points = np.array(self.sites.values())
        boundaries = {}
        vor = Voronoi(points)

        site_to_tower = {}
        for tower in self.sites:
            site_to_tower[self.sites[tower]] = tower

        center = points.mean(axis=0)
        radius = points.ptp(axis=0).max()
        for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge
                end_points = (tuple(vor.vertices[v1]), tuple(vor.vertices[v2]))
            else:
                # ridge with infinite end, borrowed code
                t = points[p2] - points[p1] #tangent
                t /= np.linalg.norm(t) 
                n = np.array([-t[1], t[0]]) #normal - the perpendicular vector?
                midpoint = points[[p1, p2]].mean(axis=0)
                direction = np.sign(np.dot(midpoint - center, n)) * n 
                far_point = vor.vertices[v2] + direction * radius
                end_points = (tuple(vor.vertices[v2]), tuple(far_point))

            site_pair = (tuple(points[p1]), tuple(points[p2]))
            tower_pair = (site_to_tower[site_pair[0]], \
                    site_to_tower[site_pair[1]]) 
            self.included_towers.add(tower_pair[0])
            self.included_towers.add(tower_pair[1])
            boundaries[tower_pair] = end_points

        return boundaries

    def check_included(self, session):
        for record in session:
            if record.pos not in self.included_towers:
                return False
        return True

    def clean_excluded_data(self, sessions, compressed_sessions):
        ''' Some towers have no boundary at all, too close to others. 
        
        delete related records
        modify both sessions and compressed sessions
        '''

        sessions = [session for session in sessions \
                if self.check_included(session)]
        compressed_sessions = [session for session in compressed_sessions \
                if self.check_included(session)]

        return sessions, compressed_sessions

