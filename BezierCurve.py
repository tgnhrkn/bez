import math
from util import *


class ControlPoint():
    def __init__( self, x=0, y=0, anchor1=None, anchor2=None, is_anchor=False ):
        self.x = x
        self.y = y
        self.anchor1 = anchor1
        self.anchor2 = anchor2
        self.is_anchor = is_anchor
   
    def move( self, pt, who=None ):
        dx = pt[0] - self.x
        dy = pt[1] - self.y
        self.translate( dx, dy, who=who )

    def translate( self, dx, dy, who=None ):
        self.x += dx
        self.y += dy
        if self.is_anchor:
            self._update_anchor( dx, dy )
        else:
            self._update_refs( who=who )

    def attach_anchor( self, anchor ):
        self.is_anchor = True
        self.anchor1 = anchor
        self.anchor2 = None 

    def _update_anchor( self, dx, dy ):
        assert self.is_anchor and self.anchor1 and not self.anchor2
        self.anchor1.translate_handles( dx, dy )

    def _update_refs( self, who=None ):
        if self.anchor1:
            if who is not self.anchor1:
                self.anchor1.update_other_handle( moved=2 )
        if self.anchor2:
            if who is not self.anchor2:
                self.anchor2.update_other_handle( moved=1 )

    def coords( self ):
        return ( self.x, self.y )

class BezierCurve():
    def __init__( self, order, init=None ):
        self.order = order
        if init is not None:
            for pt in init:
                assert type( pt ) is type( ControlPoint() )

        if init is not None and ( len( init ) == self.order + 1 ):
            self.ctrl_pts = init
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

    def controls( self ):
        return self.ctrl_pts

    def control_coords( self ):
        return list( [ pt.tup() for pt in self.ctrl_pts ] )

class BezierAnchor():
    def __init__( self, anchor, ctrl1=None, ctrl2=None, smooth=False, symmetric=False ):
        self.ctrl1 = ctrl1
        if self.ctrl1:
            self.ctrl1.anchor2 = self

        self.anchor = anchor
        self.anchor.attach_anchor( self )

        self.ctrl2 = ctrl2
        if self.ctrl2:
            self.ctrl2.anchor1 = self

        self.smooth = smooth
        self.symmetric = symmetric


    def anchor_tup( self ):
        return self.anchor.tup()

    def set_handle( self, which, ctrl ):
        assert which == 1 or which == 2
        assert ctrl
        if which == 1:
            self.ctrl1 = ctrl
            self.ctrl1.anchor2 = self
        else:
            self.ctrl2 = ctrl
            self.ctrl2.anchor1 = self


    def translate_handles( self, dx, dy):
        if self.ctrl1:
            self.ctrl1.translate( dx, dy, who=self )
        
        if self.ctrl2:
            self.ctrl2.translate( dx, dy, who=self )

    def update_other_handle( self, moved ):

        assert moved == 1 or moved == 2  
        # moved = 1 -> curve 1 control moved
        # moved = 2 -> curve 2 control moved
        # ask the other handle to move if necessary

        # calculate place to move to and then ask it to move.
        # TODO: For now just do nothing
        if not self.smooth and not self.symmetric:
            return

        mvd = self.ctrl1 if moved == 1 else self.ctrl2
        other = self.ctrl2 if moved == 1 else self.ctrl1
        assert mvd
        if other is None:
            return 

        if self.smooth and self.symmetric:
            move_to = mirror_pt( mvd.coords(), self.anchor.coords() )
            other.move( move_to, who=self ) 
        elif self.smooth:
            angdiff = angle_between( mvd.coords(), other.coords(), center=self.anchor.coords() )
            move_to = rotate_pt_clock( other.coords(), self.anchor.coords(), angdiff - 180 )  
            other.move( move_to, who=self )
            
            

class BezierPath():
    def __init__( self, order=1, smooth=False, symmetric=False ):
        self.curves = []
        self.anchors = []
        self.order = order
        self.smooth = smooth
        self.symmetric = symmetric

    def del_anchor( self, which ):
        # TODO
        pass

    def add_anchor( self, pt, order=None, smooth=None, symmetric=None ):
        # if this is the first one, create a ControlPoint
        # and handle, setting up references accordingly

        # otherwise create a new handle, generate control points
        # hook control points up to their respective duders
        # and we're good to go
        if order is None:
            order = self.order
        
        if smooth is None:
            smooth = self.smooth

        if symmetric is None:
            symmetric = self.symmetric


        if len( self.anchors ) == 0:
            first_pt = ControlPoint( x=pt[0], y=pt[1] )
            first_an = BezierAnchor( anchor=first_pt, smooth=smooth, symmetric=symmetric )
            self.anchors.append( first_an )
            return
        
        # Generate new control points for the new curve, excluding the existing first point
        last_an = self.anchors[-1]
        last_ctrl_pt = last_an.anchor
        next_ctrls = list( [ ControlPoint( x=x, y=y ) for x, y in lerp_pts( last_ctrl_pt.coords(), pt, order - 1 )[1:] ] )

        # Attach the new P1 to the last anchor
        last_an.set_handle( which=2, ctrl=next_ctrls[0] )

        # Create new anchor looking at end of controls
        next_an = BezierAnchor( anchor=next_ctrls[-1], ctrl1=next_ctrls[-2], smooth=smooth, symmetric=symmetric )

        # Create the curve
        curve = BezierCurve( order=order, init=[ last_ctrl_pt ]+next_ctrls )

        self.curves.append( curve )
        self.anchors.append( next_an )

    def rasterize( self, res ):
        pts = []
        for curve in self.curves:
            pts += curve.rasterize( res )
        return pts

    def controls( self ):
        if len( self.curves ) == 0:
            if len( self.anchors ) == 1:
                return [ self.anchors[0].anchor ]
            else:
                return []
        ctrls = list( self.curves[0].controls() )
        for curve in self.curves[1:]:
            ctrls += curve.controls()[1:]
        return ctrls

