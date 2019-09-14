#!/usr/bin/python3
import pyglet
from pyglet.gl import *
from pyglet.window import mouse, key
from bez import *
import sys
from BezierCurve import BezierCurve
from util import *
import random

h = 1000
w = 1000
window = pyglet.window.Window( height=h, width=w )
order = 3 if len( sys.argv ) < 2 else int( sys.argv[1] )
selected = None
res = 10 if len( sys.argv ) < 3 else int( sys.argv[2] )
offset_w = w / 10
offset_h = h / 10
init_pts = list( [ ( int( random.uniform( offset_w, w - offset_w ) ), int( random.uniform( offset_h, h - offset_h ) ) ) for _ in range( order + 1 ) ] )
bez_curve = BezierCurve( order, init=init_pts )

@window.event
def on_mouse_drag( x, y, dx, dy, buttons, modifiers ):
    global selected
    global bez_curve
    if buttons == mouse.RIGHT:
        if selected is not None:
            bez_curve.move_ctrl( selected, x, y )
    
@window.event
def on_mouse_press( x, y, buttons, modifiers ):
    global selected
    global bez_curve
    if buttons == mouse.LEFT:
        for idx, pt in enumerate( bez_curve.control_coords() ):
            if pt_dist( pt, ( x, y ) ) <= 5.0:
                selected = idx
                return
        selected = None


@window.event
def on_draw():
    global bez_curve
    glClear( GL_COLOR_BUFFER_BIT )
    glPointSize( 10.0 )

    glBegin( GL_LINE_STRIP )

    glColor3f( 1.0, 0.0, 0.0 )
    for pt in bez_curve.rasterize( res ):
        glVertex2f( *pt )
    glEnd()

    glBegin( GL_POINTS )
    for idx, pt in enumerate( bez_curve.control_coords() ):
        if idx == selected:
            glColor3f( 0.0, 0.0, 1.0 )
        else:
            glColor3f( 0.0, 1.0, 0.0 )

        glVertex2f( *pt )
    glEnd()

pyglet.app.run()    
