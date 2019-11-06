#!/usr/bin/python3
import pyglet
from pyglet.gl import *
from pyglet.window import mouse, key
from BezierCurve import *

w = 1000
h = 1000
n_rows = 10
n_cols = 10
res = 10

window = pyglet.window.Window( width=w, height=h )

row_h = h / n_rows
col_w = w / n_cols

row_ctrl_coords = [ [ [
       (col * col_w, (row+1) * row_h ),
       ((col+.33 ) * col_w, (row+1) * row_h ),
       ((col+.33 ) * col_w, (row+1.25) * row_h ),
       ((col+.66 ) * col_w, (row+1.25) * row_h ),
       ((col+.66 ) * col_w, (row+1) * row_h ),
       ((col+1 ) * col_w, (row+1) * row_h ) ] for col in range(n_cols) ] for row in range(n_rows-1)]

row_paths = [ [ BezierPath( order=3, smooth=True ) for _ in range(n_cols) ] for _ in range(n_rows-1) ]

for ri, row in enumerate(row_paths):
    for ci, path in enumerate(row):
        for coord in row_ctrl_coords[ri][ci]:
            path.add_anchor( coord )

col_ctrl_coords = [ [ [
       ((col+1) * col_w, (row) * row_h ),
       ((col+1 ) * col_w, (row+.33) * row_h ),
       ((col+1.25 ) * col_w, (row+.33) * row_h ),
       ((col+1.25 ) * col_w, (row+.66) * row_h ),
       ((col+1 ) * col_w, (row+.66) * row_h ),
       ((col+1 ) * col_w, (row+1) * row_h ) ] for row in range(n_rows) ] for col in range(n_cols-1)]

col_paths = [ [ BezierPath( order=3, smooth=True ) for _ in range(n_rows) ] for _ in range(n_cols-1) ]

for ci, col in enumerate(col_paths):
    for ri, path in enumerate(col):
        for coord in col_ctrl_coords[ci][ri]:
            path.add_anchor( coord )

@window.event
def on_mouse_drag( x, y, dx, dy, buttons, modifiers ):
    pass

@window.event
def on_mouse_press( x, y, buttons, modifiers ):
    pass

@window.event
def on_key_press( symbols, modifiers ):
    pass

def draw_content():
    global row_ctrl_coords
    global row_paths
    global res

#    glPointSize( 10.0 )
#    glBegin( GL_POINTS )
#    glColor3f( 0.0, 0.0, 1.0 )
#    for row in row_ctrl_coords:
#        for ctrls in row:
#            for ctrl in ctrls:
#                glVertex2f( *ctrl )
#    glEnd()
#
#    glPointSize( 10.0 )
#    glBegin( GL_POINTS )
#    glColor3f( 0.0, 0.0, 1.0 )
#    for col in col_ctrl_coords:
#        for ctrls in col:
#            for ctrl in ctrls:
#                glVertex2f( *ctrl )
#    glEnd()

    for row in row_paths:
        for path in row:
            glBegin( GL_LINE_STRIP )
            glColor3f( 1.0, 0.0, 0.0 )
            for vert in path.rasterize( res ):
                glVertex2f( *vert )
            glEnd()

    for col in col_paths:
        for path in col:
            glBegin( GL_LINE_STRIP )
            glColor3f( 1.0, 0.0, 0.0 )
            for vert in path.rasterize( res ):
                glVertex2f( *vert )
            glEnd()

def draw_ui():
    pass

@window.event
def on_draw():
    glClear( GL_COLOR_BUFFER_BIT )
    draw_content()
    draw_ui()

pyglet.app.run()    
