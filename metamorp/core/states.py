'''
Application states.

@author: igor
'''
from metamorp.core.state_machine import AbstractState, AbstractTransition
from docutils.statemachine import StateMachine



class LassoSelection(AbstractState):
    """
    State for free-form lasso selection.
    """
    name = "Lasso selection"
    

class FreeDraw(AbstractState):
    """
    State for free-form drawing of the new type/model instance.
    """
    name = "Free draw"


class MoveSelection(AbstractState):
    """
    State for moving single element or selection of elements.
    """
    name = "Move selection"




class FromLassoSelectionToMoveSelection(AbstractTransition):
    
    def on_transition(self):
        """
        
        """

def get_state_machine():        
    state_machine = StateMachine()    
    
    
