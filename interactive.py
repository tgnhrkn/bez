#!/usr/bin/python3
import pyglet
from pyglet.gl import *
from pyglet.window import mouse, key
from bez import *
from util import *
from BezierCurve import *

w = 1000
h = 1000
window = pyglet.window.Window( width=w, height=h )

order=3
path = BezierPath( order=order, smooth=True, symmetric=False )
selected_pt = None
res = 50


modes = {
    0: 'add',
    1: 'interactive',
    2: 'settings',
}
mode = 0

def mode_text():
    return modes[ mode ]

# visual toggles
path_on = True
handles_on = True
points_on = True

@window.event
def on_mouse_drag( x, y, dx, dy, buttons, modifiers ):
    global path
    global mode
    global selected_pt
    global selected_part
    if buttons == mouse.RIGHT and mode == 1:
        if selected_pt is not None:
            selected_pt.move( ( x, y ) )
    

@window.event
def on_mouse_press( x, y, buttons, modifiers ):
    global path
    global mode
    global selected_pt
    global selected_part
    global order
    if buttons == mouse.RIGHT and mode == 1:
        if selected_pt is not None:
            selected_pt.move( ( x, y ) )

    if buttons == mouse.LEFT:
        if mode == 0:
            path.add_anchor( ( x, y ), order=order )
        elif mode == 1:
            for ctrl in path.controls():
                if pt_dist( ctrl.coords(), ( x, y ) ) <= 5.0:
                    selected_pt = ctrl
                    return
            selected_pt = None


@window.event
def on_key_press( symbols, modifiers ):
    global mode
    global path
    global selected_pt
    global path_on
    global points_on
    global handles_on
    global order

    if symbols == key.A:
        mode = 0
    elif symbols == key.I:
        mode = 1
    elif symbols == key.S:
        mode = 2
    elif symbols == key.BACKSPACE:
        path.del_point()
    elif symbols == key.D and mode == 1:
        if selected_pt is not None:
            path.del_point( idx=selected_pt )
    
    if mode == 2:
        if symbols == key.C:
            path_on = not path_on
        elif symbols == key.P:
            points_on = not points_on
        elif symbols == key.H:
            handles_on = not handles_on
        elif symbols == key.UP:
            order += 1
        elif symbols == key.DOWN:
            order = max( 2, order - 1 )

def draw_handles():
    global path
    glColor3f( 1.0, 1.0, 1.0 )
    for anchor in path.anchors:
        
        if anchor.ctrl1:
            glBegin( GL_LINE_STRIP )
            glVertex2f( *anchor.ctrl1.coords() )
            glVertex2f( *anchor.anchor.coords() )
            glEnd()

        if anchor.ctrl2:
            glBegin( GL_LINE_STRIP )
            glVertex2f( *anchor.ctrl2.coords() )
            glVertex2f( *anchor.anchor.coords() )
            glEnd()


def draw_points():
    global path
    global selected_pt
    glPointSize( 10.0 )
    glBegin( GL_POINTS )
    for ctrl in path.controls():
        if selected_pt is ctrl:
            glColor3f( 0.0, 0.0, 1.0 )
        else:
            glColor3f( 0.0, 1.0, 0.0 )
        glVertex2f( *ctrl.coords() )
    glEnd()

def draw_path():
    global path
    global res
    glBegin( GL_LINE_STRIP )
    glColor3f( 1.0, 0.0, 0.0 )
    for vert in path.rasterize( res ):
        glVertex2f( *vert )
    glEnd()

def draw_content():
    global handles_on, path_on, points_on

    if handles_on:
        draw_handles()

    if points_on:
        draw_points()

    if path_on:
        draw_path()

def draw_mode():
    pyglet.text.Label( "-- %s --" % mode_text(),
            font_name="Courier New", 
            font_size=16, x=0, y=0, 
            anchor_x='left', 
            anchor_y='bottom' ).draw()

def draw_order():
    global order
    global w
    pyglet.text.Label( "order = %i" % (order),
            font_name="Courier New",
            font_size=16, x=w, y=0,
            anchor_x='right',
            anchor_y='bottom' ).draw()

def draw_ui():
    draw_mode()
    draw_order()

@window.event
def on_draw():
    glClear( GL_COLOR_BUFFER_BIT )
    draw_content()
    draw_ui()

pyglet.app.run()    
