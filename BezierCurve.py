import math


class ControlPoint():
    def __init__( self, x=0, y=0 ):
        self.x = x
        self.y = y

def binomial_coef( n, k ):
    return math.factorial( n ) // ( math.factorial( k ) * math.factorial( n - k ) )

def bernstein( i, n, t ):
    foo = binomial_coef( n, i ) * (( 1 - t )**(n-i)) * (t**i)
    return foo

class BezierCurve():
    def __init__( self, order, init=None ):
        self.order = order
        if init is not None and ( len( init ) == self.order + 1 ):
            self.ctrl_pts = list( [ ControlPoint(x=x, y=y) for x,y in init ] )
        else:
            self.ctrl_pts = list( [ ControlPoint() for _ in range( self.order + 1 ) ] )

    # Evaluate with Bernstein Sum
    def eval( self, t ):
        n = self.order
        x_sum, y_sum = 0.0, 0.0
        for i, pt in enumerate( self.ctrl_pts ):
            x_sum += pt.x * bernstein( i, n, t )
            y_sum += pt.y * bernstein( i, n, t )
        return ( x_sum, y_sum )
        
    def rasterize( self, res ):
        draw_pts = []
        step = 1 / res
        t = 0.0
        while t < 1.0:
            draw_pts.append( self.eval( t ) )
            t += step
        draw_pts.append( self.eval( 1.0 ) )
        return draw_pts

    def move_ctrl( self, i, x, y ):
        pt = self.ctrl_pts[i]
        pt.x = x
        pt.y = y
    
    def control_points( self ):
        return self.ctrl_pts

    def control_coords( self ):
        return list( [ (pt.x, pt.y) for pt in self.ctrl_pts ] )


        



        
