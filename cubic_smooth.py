#!/usr/bin/python3
import pyglet
from pyglet.gl import *
from pyglet.window import mouse, key
from bez import *

window = pyglet.window.Window( 1000, 1000 )

curve = Smooth_Cubic_Curve()

@window.event
def on_mouse_press( x, y, buttons, modifiers ):
    global curve
    if buttons == mouse.LEFT:
        curve.add_point( x, y )

@window.event
def on_draw():
    glClear( GL_COLOR_BUFFER_BIT )
    glPointSize( 10.0 )

    # Draw curve
    glBegin( GL_LINE_STRIP )
    glColor3f( 1.0, 0.0, 0.0 )
    for vert in curve.get_vertices( 10 ):
        glVertex2f( *vert )
    glEnd()

    # Draw points
    glBegin( GL_POINTS )
    glColor3f( 0.0, 1.0, 0.0 )
    for pt in curve.get_points():
        glVertex2f( *pt )
    glEnd()

pyglet.app.run()    
