'''
Created on Apr 15, 2014

@author: igor
'''
from kivy.graphics import Color, Line, PushState, PopState
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ListProperty, NumericProperty, BooleanProperty


class PrimitiveShape(RelativeLayout):
    """
    Base class for basic shapes used for building visual representation
    of model instances.
    """
    color = ListProperty([0.4, 0.2, 0.1, 1])
    pos = ListProperty([0,0])

    
class CircleShape(PrimitiveShape):
    """
    """
    radius = NumericProperty(50)
    
    def __init__(self, radius=50, *args, **kwargs):
        super(CircleShape, self).__init__(*args, **kwargs)
        self.radius = radius
        with self.canvas:
            Color(*self.color)
            Line(ellipse=(0, 0, self.radius, self.radius))
    
    
class RectangleShape(PrimitiveShape):
    """
    """
    rect_size = ListProperty([100,50])
    
    def __init__(self, *args, **kwargs):
        super(RectangleShape, self).__init__(*args, **kwargs)
        with self.canvas:
            Color(*self.color)
            Line(rectangle=(0, 0, self.rect_size[0], self.rect_size[1]))

    
class EllipseShapeWidget(PrimitiveShape):
    """
    """
    radius_x = NumericProperty(100)
    radius_y = NumericProperty(50)
    
# class StrokeShapeWidget(PrimitiveShape):
#     """
#     This widget
#     """
#     points = ListProperty([])
#     def add_to_canvas(self, canvas):
#     


class MInstWidget(RelativeLayout):
    """
    This class represents MoRP model instance.
    E.g. for language StateMachine with the concept State this
    will be representation of the concrete State instance (e.g. "Closed")
    
    Graphical representation consists of generic graphic primitives (Line,
    Rectangle, Circle, Ellipse, Text...) each having its own style properties
    (line thickness, color, fill color, font...)
    This primitives and properties are part of the language for MetaMoRP
    configuration.
    """
    
    selected = BooleanProperty(False)
    
    def __init__(self, *args, **kwargs):
        super(MInstWidget, self).__init__(*args, **kwargs)
        self.touch = None
        
        self.add_widget(CircleShape(50))
        self.add_widget(RectangleShape())
        self.size = (100, 50)
       
        # Instructions for selection rectangle 
        self.selection_instructions = [ 
               PushState(),
               Color(1, 0, 0, 0.5),
               Line(points=[-10, -10, -10, self.size[1] + 10,\
                        self.size[0] + 10, self.size[1] + 10, \
                        self.size[0] + 10, -10, -10, -10], \
                        closed=True, width=1, dash_size=10, dash_offset=3),
               PopState()
        ]
        
    @property
    def diagram(self):
        return self._diagram
    
    def on_parent(self, *args):
        self._diagram = self.parent.parent
        
    def on_selected(self, widget, value):
        """
        On selection change toggle selection rectangle.
        """
        if self.selected:
            for inst in self.selection_instructions:
                self.canvas.add(inst)
        else:
            for inst in self.selection_instructions:
                self.canvas.remove(inst)
    
    def on_touch_down(self, touch):
        if self.diagram.state == "normal" and \
            len(self.parent.touches)==1:
            if self.collide_point(touch.x, touch.y):
                # Toggle selection
                touch.grab(self)
                touch.ud['hit'] = self
                touch.ud['old_select_state'] = self.selected
                self.selected = True
                return True
        
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            if not 'moved' in touch.ud:
                # If not moved toggle selection state
                self.selected = not touch.ud['old_select_state']
            touch.ungrab(self)
            return True