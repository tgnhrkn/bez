#!/usr/bin/python3
import pyglet
from pyglet.gl import *
from pyglet.window import mouse, key
from bez import *
from util import *

window = pyglet.window.Window( 1000, 1000 )

curve = Smooth_Cubic_Curve()
selected_pt = None
selected_part = None

# 0: add
# 1: interactive
mode = 0

@window.event
def on_mouse_press( x, y, buttons, modifiers ):
    global curve
    global mode
    global selected_pt
    global selected_part
    print( "Mouse pressed, mode = %i" % mode )
    
    if buttons == mouse.RIGHT and mode == 1:
        if selected_pt is not None:
            curve.transform_node( selected_pt, selected_part, moveTo=( x, y ) )


    if buttons == mouse.LEFT:
        if mode == 0:
            curve.add_point( x, y )
        elif mode == 1:
            for idx, node in enumerate( curve.nodes() ):
                for part in range( 3 ):
                    px = node[ part * 2 ]
                    py = node[ part * 2 + 1 ]
                    if pt_dist( ( px, py ), ( x, y ) ) <= 5.0:
                        selected_pt = idx
                        selected_part = part
                        print( "set selected_pt to %i, part to %i" % (selected_pt, selected_part ) )
                        return
            selected_pt = None
            selected_part = None
            print( "Set them back" )


@window.event
def on_key_press( symbols, modifiers ):
    global mode
    if symbols == key.A:
        mode = 0
    elif symbols == key.I:
        mode = 1

@window.event
def on_draw():
    global selected_pt
    global selected_part
    glClear( GL_COLOR_BUFFER_BIT )
    glPointSize( 10.0 )

    # Draw handles
    glColor3f( 1.0, 1.0, 1.0 )
    for node in curve.nodes():
        h1 = node[0], node[1]
        h2 = node[4], node[5]
        glBegin( GL_LINE_STRIP )
        glVertex2f( *h1 )
        glVertex2f( *h2 )
        glEnd()

    # Draw points
    glBegin( GL_POINTS )
    for idx, pt in enumerate( curve.get_points() ):
        if selected_pt is not None:
            print( "idx: %i" % idx )
            print( "math: %i" % (selected_pt * 3 + selected_part) )

        if selected_pt is not None and ( idx == selected_pt * 3 + selected_part ):
            print( "setting color" )
            glColor3f( 0.0, 0.0, 1.0 )
        else:
            glColor3f( 0.0, 1.0, 0.0 )
        glVertex2f( *pt )
    glEnd()

    # Draw curve
    glBegin( GL_LINE_STRIP )
    glColor3f( 1.0, 0.0, 0.0 )
    for vert in curve.get_vertices( 10 ):
        glVertex2f( *vert )
    glEnd()


pyglet.app.run()    
