from math import sqrt

def pt_dist( pt1, pt2 ):
    return sqrt( ( ( pt1[0] - pt2[0] )**2 ) + ( ( pt1[1] - pt2[1] )**2 ) )
