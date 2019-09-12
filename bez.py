import numpy as np

def multi_quad_bez( ctrl_pts, res ):
    if len( ctrl_pts ) % 2 == 0:
        ctrl_pts = list( [ x for x in ctrl_pts[:-1] ] ) 

    draw_pts = []
    for i in range( ( len( ctrl_pts ) - 1 ) // 2 ) :
        p1, p2, p3 = ctrl_pts[i * 2], ctrl_pts[i * 2 +1], ctrl_pts[i * 2+2]
        draw_pts += quad_bez( p1, p2, p3, res )
    return draw_pts

def quad_bez( p0, p1, p2, res ):
    
    curve_x = lambda t: (1 - t) * ( (1 - t) * p0[0] + t * p1[0] ) + t * ( ( 1 - t ) * p1[0] + t * p2[0] )
    curve_y = lambda t: (1 - t) * ( (1 - t) * p0[1] + t * p1[1] ) + t * ( ( 1 - t ) * p1[1] + t * p2[1] )

    step = 1 / res

    t = 0.0
    pts = []
    while t <= 1.0:
        pts.append( ( curve_x( t ), curve_y( t ) ) )
        t += step

    return pts

def multi_cube_bez( ctrl_pts, res ):
    if len( ctrl_pts ) < 4:
        return []
    
    if ( len( ctrl_pts ) - 1 ) % 3 != 0:
        n_curves = ( len( ctrl_pts ) - 1 ) // 3 + 1
        n_pts = 1 + ( n_curves - 1) * 3
        ctrl_pts = list( [ x for x in ctrl_pts[0:n_pts] ] )

    draw_pts = []
    for i in range( ( len( ctrl_pts ) - 1 ) // 3 ):
        p1 = ctrl_pts[ i * 3 ]
        p2 = ctrl_pts[ i * 3 + 1 ]
        p3 = ctrl_pts[ i * 3 + 2 ]
        p4 = ctrl_pts[ i * 3 + 3 ]
        draw_pts += cube_bez( p1, p2, p3, p4, res )
    return draw_pts

def cube_bez( p0, p1, p2, p3, res ):
    q1 = quad_bez( p0, p1, p2, res )
    q2 = quad_bez( p1, p2, p3, res )

    cube_x = []
    cube_y = []
    idx = 0
    t = 0.0
    step = 1 / res
    while t <= 1.0:
        q1_pt, q2_pt = q1[idx], q2[idx]
        cube_x.append( ( 1 - t ) * q1_pt[0] + t * q2_pt[0] )
        cube_y.append( ( 1 - t ) * q1_pt[1] + t * q2_pt[1] )
        t += step 
        idx += 1

    return list( zip( cube_x, cube_y ) )


def lin_eqn( x1, y1, x2, y2 ):
    m = ( y2 - y1 ) / ( x2 - x1 )
    b = y1 - ( m * x1 )
    return lambda x: m * x + b

def get_mid( pt1, pt2 ):
    x = ( pt1[0] + pt2[0] ) / 2
    y = ( pt1[1] + pt2[1] ) / 2
    return ( x, y )

class Smooth_Quad_Curve():
    
    def __init__( self ):
        self.points = []

    def add_point( self, x, y ):
        if len( self.points ) == 0:
            self.points.append( (x, y) )
            return
        
        if len( self.points ) == 1:
            midpoint = get_mid( self.points[0], (x, y) )
            self.points.append( midpoint )
            self.points.append( (x, y) )
            return
        
        ctrl_pt = x1, y1 = self.points[ -2 ]
        thru_pt = x2, y2 = self.points[ -1 ]

        eqn = lin_eqn( x1, y1, x2, y2 )

        new_ctl_x = 2 * x2 - x1
        new_ctl_y = eqn( new_ctl_x )

        self.points.append( ( new_ctl_x, new_ctl_y ) )
        self.points.append( ( x, y ) )


    def get_vertices( self, res ):
        return multi_quad_bez( self.points, res )

    def get_points( self ):
        return list( [x for x in self.points ] )

def mirror_pt( pt1, center ):
    if pt1[0] == center[0]:
        x = pt1[0]
        y = 2 * center[1] - pt1[1]
        return (x, y)
    else:
        eqn = lin_eqn( *pt1, *center )
        x = 2 * center[0] - pt1[0]
        y = eqn( x )
        return ( x, y )

def handles( x, y, dist ):
    h1x, h1y = (( x - dist ), y)
    h2x, h2y = mirror_pt( ( h1x, h1y ), ( x, y ) )
    return [ h1x, h1y, h2x, h2y ]

def rotate_pt_clock( pt, center, theta ):
    theta = np.radians( theta )
    np_pt = np.array( pt )
    np_center = np.array( center )

    np_pt = np_pt - np_center
    c, s = np.cos( theta ), np.sin( theta )
    R = np.array( ( ( c, s ), ( -s, c ) ) )
    fpt = ( R @ np_pt ) + np_center
    if type( pt ) is type( () ):
        return ( fpt[0], fpt[1] )
    else:
        return [ fpt[0], fpt[1] ]

class Smooth_Cubic_Curve():
    def __init__( self ):
        # [ c1x, c1y, ax, xy, c2x, c2y ]
        self.points = []

    def add_point( self, x, y ):
        hdls = handles( x, y, 30 )
        self.points.append( hdls[ 0:2 ] + [ x, y ] + hdls[ 2:4 ] )

    def del_point( self, idx=-1 ):
        if idx < -1:
            return

        if len( self.points ) == 0 or idx >= len( self.points ):
            return

        del self.points[ idx ]

    def _points_tupled( self ):
        tuppts = []
        for cac in self.points:
            tuppts += [ ( cac[0], cac[1] ), ( cac[2], cac[3] ), ( cac[4], cac[5] ) ]
        return tuppts

    def get_vertices( self, res ):
        all_pts = self._points_tupled()
        all_pts = all_pts[1:-1]
        return multi_cube_bez( all_pts, res )

    def get_points( self ):
        return self._points_tupled()

    def nodes( self ):
        return list( [x for x in self.points ] )

    def transform_node( self, node, part, rotation=None, extend=None, translation=None, moveTo=None ):
        nd = self.points[ node ]
        
        if translation is not None and moveTo is not None:
            raise Exception( "Cannot translate and moveTo" )

        # handle moveTo
        if moveTo is not None:
            dx = moveTo[0] - nd[ part * 2 ]
            dy = moveTo[1] - nd[ part * 2 + 1 ]
            translation = ( dx, dy ) 
        
        # handle translate
        if translation is not None:
            if part == 1:
                for i in range( 3 ):
                    nd[ i * 2 ] += translation[0]
                    nd[ i * 2 + 1 ] += translation[1]
            else:
                nd[ part * 2 ] += translation[0]
                nd[ part * 2 + 1 ] += translation[1]
                otherx, othery = mirror_pt( ( nd[ part * 2 ], nd[ part * 2 + 1] ), ( nd[2], nd[3] ) )
                if part == 0:
                    nd[ 4 ] = otherx
                    nd[ 5 ] = othery
                else:
                    nd[ 0 ] = otherx
                    nd[ 1 ] = othery

        # TODO
        # handle rotation
        # handle extend
                
