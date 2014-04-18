'''
Created on Apr 15, 2014

@author: igor
'''
from kivy.uix.scatter import ScatterPlane
from kivy.properties import ListProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from metamorp.ui.item import MInstWidget


class Diagram(ScatterPlane):
    state = StringProperty("readonly")
    
    def __init__(self, *args, **kwargs):
        super(Diagram, self).__init__(do_rotation=False, 
                                      do_translation=True,
                                      *args, **kwargs)
        
        self.add_widget(DiagramWidget())
        

class DiagramWidget(FloatLayout):
    
    
    def __init__(self, *args, **kwargs):
        super(DiagramWidget, self).__init__(*args, **kwargs)

    def on_touch_down(self, touch):
#         self.add_widget(ItemWidget(pos=touch.pos)) 
        if self.parent.state == "draw":
            self.add_widget(MInstWidget(pos=touch.pos)) 
        else:
            return super(FloatLayout, self).on_touch_down(touch)
