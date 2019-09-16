#!/usr/bin/python3

from bez import *
from util import *
import numpy as np

def test_lin_eqn():
    x1, y1, x2, y2 = 1, 1, 5, 5
    eqn = lin_eqn( x1, y1, x2, y2 )

    print( eqn( 3 ) )

def test_clock_rot():
    pt = 5, 10
    center = 5,5
    theta = 45

    res = rotate_pt_clock( pt, center, theta )
    print( res )

def test_lerp():
    s = 10
    e = 20
    n = 3
    res = lerp( s, e, n )
    print( res )

def test_lerp_pts():
    s = ( 10, 10 )
    end = ( 20, 50 )
    n = 3
    res = lerp_pts( s, end, n )
    print( res )

def test_ang_bet():
    s = ( 0,2 )
    e = ( 2,-1 )
    res = angle_between( s, e, ( 1, 1 ) )
    print( res )
    
test_ang_bet()
