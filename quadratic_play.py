#!/usr/bin/python3
import pyglet
from pyglet.gl import *
from pyglet.window import mouse, key
from bez import *

window = pyglet.window.Window( 1000, 1000 )
p1, p2, p3 = ( 100, 100 ), ( 100, 500 ), ( 600, 500 )
pts = [ p1, p2, p3 ]
selected = 1

@window.event
def on_mouse_drag( x, y, dx, dy, buttons, modifiers ):
    global selected
    global pts

    if buttons == mouse.LEFT:
        pts[selected - 1] = (x, y)
    
@window.event
def on_key_press( symbol, modifiers ):
    global selected
    if symbol == key._1:
        selected = 1
    elif symbol == key._2:
        selected = 2
    elif symbol == key._3:
        selected = 3

@window.event
def on_draw():
    glClear( GL_COLOR_BUFFER_BIT )
    glPointSize( 10.0 )

    glBegin( GL_LINE_STRIP )

    glColor3f( 1.0, 0.0, 0.0 )
    for pt in multi_quad_bez( pts, 10 ):
        glVertex2f( *pt )
    glEnd()

    glBegin( GL_POINTS )
    glColor3f( 0.0, 1.0, 0.0 )
    for pt in pts:
        glVertex2f( *pt )
    glEnd()

pyglet.app.run()    
