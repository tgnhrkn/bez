import math
from math import sqrt
import numpy as np

def pt_dist( pt1, pt2 ):
    return sqrt( ( ( pt1[0] - pt2[0] )**2 ) + ( ( pt1[1] - pt2[1] )**2 ) )

def lin_eqn( x1, y1, x2, y2 ):
    m = ( y2 - y1 ) / ( x2 - x1 )
    b = y1 - ( m * x1 )
    return lambda x: m * x + b

def lerp( s, e, n ):
    d = e - s
    n = n + 1
    subd = d / n
    pts = [ s + subd * i for i in range( n + 1 ) ]
    return list( pts )
    
def lerp_pts( s, e, n ):
    return list( zip( lerp( s[0], e[0], n ), lerp( s[1], e[1], n ) ) )

def binomial_coef( n, k ):
    return math.factorial( n ) // ( math.factorial( k ) * math.factorial( n - k ) )

def bernstein( i, n, t ):
    foo = binomial_coef( n, i ) * (( 1 - t )**(n-i)) * (t**i)
    return foo

def mirror_pt( pt1, center ):
    if pt1[0] == center[0]:
        x = pt1[0]
        y = 2 * center[1] - pt1[1]
        return (x, y)
    else:
        eqn = lin_eqn( *pt1, *center )
        x = 2 * center[0] - pt1[0]
        y = eqn( x )
        return ( x, y )

def get_mid( pt1, pt2 ):
    x = ( pt1[0] + pt2[0] ) / 2
    y = ( pt1[1] + pt2[1] ) / 2
    return ( x, y )

def rotate_pt_clock( pt, center, theta ):
    theta = np.radians( theta )
    np_pt = np.array( pt )
    np_center = np.array( center )

    np_pt = np_pt - np_center
    c, s = np.cos( theta ), np.sin( theta )
    R = np.array( ( ( c, s ), ( -s, c ) ) )
    fpt = ( R @ np_pt ) + np_center
    if type( pt ) is type( () ):
        return ( fpt[0], fpt[1] )
    else:
        return [ fpt[0], fpt[1] ]

def angle_between( pt1, pt2, center=(0.0, 0.0) ):
    pt1 = ( pt1[0] - center[0], pt1[1] - center[1] )
    pt2 = ( pt2[0] - center[0], pt2[1] - center[1] )
    ang1 = math.atan2( *pt1 )
    ang2 = math.atan2( *pt2 )
    return math.degrees( (ang1 - ang2 ) % (2 * math.pi ) )
