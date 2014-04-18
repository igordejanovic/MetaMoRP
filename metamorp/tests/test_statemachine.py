'''
Created on Apr 14, 2014

@author: igor
'''
import unittest
from metamorp.core.state_machine import StateMachine, AbstractState,\
    AbstractTransition

class TestState(AbstractState):
    def __init__(self, *args, **kwargs):
        super(TestState, self).__init__(*args, **kwargs)
        self.on_entry_called = 0
        self.on_exit_called = 0
    def on_entry(self, event):
        self.on_entry_called = self.on_exit_called + 1
    def on_exit(self, event):
        self.on_exit_called = self.on_entry_called + 1

class TestTransition(AbstractTransition): 
    def __init__(self, *args, **kwargs):
        super(TestTransition, self).__init__(*args, **kwargs)
        self.can_traverse_called = 0
        self.on_transition_called = 0
    def can_traverse(self, event):
        self.can_traverse_called = self.on_transition_called + 1
        return True
    def on_transition(self, event):
        self.on_transition_called = self.can_traverse_called + 1

class Test(unittest.TestCase):

    def test_simple_transitions(self):
        self.state_machine = StateMachine()
        a = TestState("A")
        b = TestState("B")
        c = TestState("C")
        ab = TestTransition(a, b)
        bc = TestTransition(b, c)
        ca = TestTransition(c, a)
        self.state_machine.add_transition(ab)
        self.state_machine.add_transition(bc)
        self.state_machine.add_transition(ca)

        self.state_machine.current_state = a
        
        self.state_machine.dispatch_event(None)
        
        self.assertEqual(self.state_machine.current_state, b)
        self.assertEqual(a.on_entry_called, 1)
        self.assertEqual(a.on_exit_called, 2)
        self.assertEqual(ab.can_traverse_called, 1)
        self.assertEqual(ab.on_transition_called, 2)
        
        self.state_machine.dispatch_event(None)

        self.assertEqual(self.state_machine.current_state, c)
        self.assertEqual(a.on_entry_called, 1)
        self.assertEqual(a.on_exit_called, 2)
        self.assertEqual(ab.can_traverse_called, 1)
        self.assertEqual(ab.on_transition_called, 2)
        self.assertEqual(b.on_entry_called, 1)
        self.assertEqual(b.on_exit_called, 2)
        self.assertEqual(bc.can_traverse_called, 1)
        self.assertEqual(bc.on_transition_called, 2)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()