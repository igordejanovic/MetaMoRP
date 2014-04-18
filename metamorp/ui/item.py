'''
Created on Apr 15, 2014

@author: igor
'''
from kivy.graphics import Color, Line 
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ListProperty, NumericProperty


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
    
    def __init__(self, *args, **kwargs):
        super(MInstWidget, self).__init__(*args, **kwargs)
        self.touch = None
        
        self.add_widget(CircleShape(50))
        self.add_widget(RectangleShape())
        self.size = (100, 50)
    
    def _remember_pos(self, touch):
        touch.ud['old_x'] = touch.x
        touch.ud['old_y'] = touch.y

    def on_touch_down(self, touch):
        if self.parent.parent.state == "readonly" and \
            len(self.parent.touches)==1:
            if self.collide_point(touch.x, touch.y):
                # If dragging is detected remember touch
                # that started it
                self.touch = touch
                self._remember_pos(touch)
                return True
        
    def on_touch_move(self, touch):
        if self.touch == touch:
            self.pos = (self.pos[0] + (touch.x-touch.ud['old_x']),
                        self.pos[1] + (touch.y-touch.ud['old_y']))
            self._remember_pos(touch)
            return True
        
    def on_touch_up(self, touch):
        if self.touch == touch:
            self.touch = None
            return True
        