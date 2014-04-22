'''
MetaMoRP IDE
'''
import kivy
kivy.require('1.8.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ListProperty


class Root(Widget):
    background_color = ListProperty([0.3, 0.8, 0, 1])
    
    def best_fit(self):
        print("Best fit")

    def cut(self):
        print("Cut")
    
    def copy(self):
        print("Copy")
    
    def paste(self):
        print("Paste")


class MetaMoRPApp(App):
    kv_directory = 'design'
    

if __name__ == '__main__':
    MetaMoRPApp().run()