'''
Created on Apr 15, 2014

@author: igor
'''
from kivy.uix.scatter import ScatterPlane
from kivy.properties import ListProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line
from metamorp.ui.item import MInstWidget
from metamorp.core.utils import point_inside_polygon


class Diagram(ScatterPlane):
    state = StringProperty("normal")
    
    def __init__(self, *args, **kwargs):
        super(Diagram, self).__init__(do_rotation=False, 
                                      do_translation=True,
                                      *args, **kwargs)

class DiagramWidget(FloatLayout):
    
    def __init__(self, *args, **kwargs):
        super(DiagramWidget, self).__init__(*args, **kwargs)
        
        # For tracking multiple touches
        self.touches = set()
       
        # Line added to canvas when in lasso mode
        self.lasso_line = Line(points=[], width=1, dash_size=10, dash_offset=3)

    def _remember_pos(self, touch):
        touch.ud['old_x'] = touch.x
        touch.ud['old_y'] = touch.y
        
    def clear_selection(self):
        for child in self.children:
            child.selected = False
            
    def selected_items(self):
        return [child for child in self.children if child.selected]

    def on_touch_down(self, touch):

        self.touches.add(touch) 

        if self.parent.state == "lasso":
            touch.ud['lasso'] = [touch.x, touch.y]
            self.lasso_line.points = touch.ud['lasso']
            self.canvas.add(self.lasso_line)

        else:
            self._remember_pos(touch)
            return super(DiagramWidget, self).on_touch_down(touch)
        return True

    def on_touch_move(self, touch):
        
        # Record that the touch has moved
        touch.ud['moved'] = True

        # If state button is in lasso mode
        # start lasso.
        if self.parent.state == "lasso":
            touch.ud['lasso'].extend([touch.x, touch.y])
            self.lasso_line.points = touch.ud['lasso']
        else:
            # If item was touched move the selection
            if 'hit' in touch.ud:
                for child in self.children:
                    if child.selected:
                        # Move each child for touch delta vector
                        child.pos = (child.pos[0] + (touch.x-touch.ud['old_x']),
                                    child.pos[1] + (touch.y-touch.ud['old_y']))
                self._remember_pos(touch)
            else:
                return super(DiagramWidget, self).on_touch_move(touch)
        return True

    def on_touch_up(self, touch):
       
        handled = super(DiagramWidget, self).on_touch_up(touch)
        
        if not handled:
            if not 'hit' in touch.ud and not 'moved' in touch.ud \
                and self.parent.state=="normal":
                if self.selected_items():
                    # Clear selection if user touches canvas in normal mode
                    # and there is current selection
                    self.clear_selection()
                else:
                    # If there is no selection create new item
                    self.add_widget(MInstWidget(pos=touch.pos))
                
            if 'lasso' in touch.ud:
                # Select all items contained inside lasso
                for item in self.children:
                    # Take center of the item as reference point
                    if point_inside_polygon(item.center_x, item.center_y, touch.ud['lasso']):
                        item.selected = True
                # Return to normal mode when lasso touch is up
                self.canvas.remove(self.lasso_line)
                self.parent.parent.parent.ids.state_button.trigger_action()

        self.touches.discard(touch)
        
        return True