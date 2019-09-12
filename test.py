#!/usr/bin/python3

from bez import *
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
    
test_clock_rot()

