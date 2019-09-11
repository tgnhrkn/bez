#!/usr/bin/python3
import pyglet
from pyglet.gl import *
from pyglet.window import mouse, key
from bez import *

window = pyglet.window.Window( 1000, 1000 )
ctl_pts = []

@window.event
def on_mouse_press( x, y, buttons, modifiers ):
    global ctl_pts
    ctl_pts.append( ( x, y ) )

@window.event
def on_draw():
    glClear( GL_COLOR_BUFFER_BIT )
    glPointSize( 10.0 )

    glBegin( GL_LINE_STRIP )
    glColor3f( 1.0, 0.0, 0.0 )
    for pt in multi_cube_bez( ctl_pts, 10 ):
        glVertex2f( *pt )
    glEnd()

    glBegin( GL_POINTS )
    glColor3f( 0.0, 1.0, 0.0 )
    for pt in ctl_pts:
        glVertex2f( *pt )
    glEnd()

pyglet.app.run()    
