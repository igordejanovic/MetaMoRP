'''
Created on Apr 14, 2014

@author: igor
'''

class StateMachineException(Exception):
    pass

class StateMachine(object):
    """
    An implementation of simple state machine.
    
    State machine consists of finite number of states and transitions
    connecting two states (source->target).
    State machine must be in one of its states (attribute: current_state).
    
    If the transition can be traversed (can_traverse returns True for the given
    event) current state on_exit is called, than on_transition and lastly
    current state is set to the transition target_state and its on_enter
    is called. 
    """
    
    def __init__(self):
        self._current_state = None
        self.transitions_from_state = {}
        
    @property
    def current_state(self):
        return self._current_state
    
    @current_state.setter
    def current_state(self, state):
        self._current_state = state
        state.on_entry(None)
    
    def add_transition(self, transition):
        """
        
        """
        transitions = self.transitions_from_state.setdefault(
                                            transition.source_state, [])
        if not transition in transitions:
                transitions.append(transition)

        
    def dispatch_event(self, event):    
        """
        React to the event by trying to find the state
        transition which can be traversed.
        """
        try: 
            transitions = self.transitions_from_state[self.current_state]
        except KeyError:
            raise StateMachineException('State %s has no out transitions!'.format(
                                                                    self.current_state))
        for transition in transitions:
            if transition.can_traverse(event):
                self.current_state.on_exit(event)
                transition.on_transition(event)
                self.current_state = transition.target_state
                self.current_state.on_entry(event)
                break
        
        
class AbstractState():
    
    def __init__(self, name):
        self.name = name
    
    def on_entry(self, event):
        """
        Called on entry to the state.
        """

    def on_exit(self, event):
        """
        Called on exit from the state.
        """
         
class AbstractTransition():
    
    def __init__(self, source_state, target_state):
        """
        """
        self.source_state = source_state
        self.target_state = target_state
        
    def can_traverse(self, event):
        """
        For given event check if this transition can be traversed.
        Args:
            event(object): An object that represents an event.
        Returns:
            True or False
        """
    
    def on_transition(self, event):
        """
        Called on state transition.
        """