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

modes = {
    0: 'add',
    1: 'interactive',
    2: 'settings',
}
mode = 0

def mode_text():
    return modes[ mode ]

# visual toggles
curve_on = True
handles_on = True
points_on = True

@window.event
def on_mouse_drag( x, y, dx, dy, buttons, modifiers ):
    global curve
    global mode
    global selected_pt
    global selected_part
    if buttons == mouse.RIGHT and mode == 1:
        if selected_pt is not None:
            curve.transform_node( selected_pt, selected_part, moveTo=( x, y ) )
    

@window.event
def on_mouse_press( x, y, buttons, modifiers ):
    global curve
    global mode
    global selected_pt
    global selected_part
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
                        return
            selected_pt = None
            selected_part = None


@window.event
def on_key_press( symbols, modifiers ):
    global mode
    global curve
    global selected_pt
    global curve_on
    global points_on
    global handles_on

    if symbols == key.A:
        mode = 0
    elif symbols == key.I:
        mode = 1
    elif symbols == key.S:
        mode = 2
    elif symbols == key.BACKSPACE:
        curve.del_point()
    elif symbols == key.D and mode == 1:
        if selected_pt is not None:
            curve.del_point( idx=selected_pt )
    
    if mode == 2:
        if symbols == key.C:
            curve_on = not curve_on
        elif symbols == key.P:
            points_on = not points_on
        elif symbols == key.H:
            handles_on = not handles_on

def draw_handles():
    global curve
    glColor3f( 1.0, 1.0, 1.0 )
    for node in curve.nodes():
        h1 = node[0], node[1]
        h2 = node[4], node[5]
        glBegin( GL_LINE_STRIP )
        glVertex2f( *h1 )
        glVertex2f( *h2 )
        glEnd()

def draw_points():
    global curve
    global selected_pt
    global selected_part
    glPointSize( 10.0 )
    glBegin( GL_POINTS )
    for idx, pt in enumerate( curve.get_points() ):
        if selected_pt is not None and ( idx == selected_pt * 3 + selected_part ):
            glColor3f( 0.0, 0.0, 1.0 )
        else:
            glColor3f( 0.0, 1.0, 0.0 )
        glVertex2f( *pt )
    glEnd()

def draw_curve():
    global curve
    glBegin( GL_LINE_STRIP )
    glColor3f( 1.0, 0.0, 0.0 )
    for vert in curve.get_vertices( 50 ):
        glVertex2f( *vert )
    glEnd()

def draw_content():
    global handles_on, curve_on, points_on

    if handles_on:
        draw_handles()

    if points_on:
        draw_points()

    if curve_on:
        draw_curve()

def draw_mode():
    pyglet.text.Label( "-- %s --" % mode_text(),
            font_name="Courier New", 
            font_size=16, x=0, y=0, 
            anchor_x='left', 
            anchor_y='bottom' ).draw()

def draw_ui():
    draw_mode()

@window.event
def on_draw():
    glClear( GL_COLOR_BUFFER_BIT )
    draw_content()
    draw_ui()

pyglet.app.run()    
