from matplotlib.widgets import Button
from copy import deepcopy
from buttons import _Button_callback
from visualizationPrimitives import PointsCollection , LinesCollection , Scene
import matplotlib.pyplot as plt
import json as js
import numpy as np
import matplotlib.colors as mcolors
    
class Plot:
    def __init__(self, scenes = [Scene()]):
        self.scenes = scenes
        
    def __configure_buttons(self):
        plt.subplots_adjust(bottom=0.2)
        ax_prev = plt.axes([0.6, 0.05, 0.15, 0.075])
        ax_next = plt.axes([0.76, 0.05, 0.15, 0.075])
        ax_run = plt.axes([0.44, 0.05, 0.15, 0.075])
        ax_import = plt.axes([0.28, 0.05, 0.15, 0.075])
        ax_add_rect = plt.axes([0.12, 0.05, 0.15, 0.075])
        b_import = Button(ax_import, 'Importuj')
        b_import.on_clicked(self.callback.importFromJS)
        b_add_rect = Button(ax_add_rect, 'Dodaj figurę')
        b_add_rect.on_clicked(self.callback.add_rect)
        b_run = Button(ax_run, 'Uruchom')
        b_run.on_clicked(self.callback.run)
        b_next = Button(ax_next, 'Następny')
        b_next.on_clicked(self.callback.next)
        b_prev = Button(ax_prev, 'Poprzedni')
        b_prev.on_clicked(self.callback.prev)
        return [b_import , b_add_rect ,b_run, b_prev, b_next]
    
    def add_scene(self, scene):
        self.scenes.append(scene)
    
    def add_scenes(self, scenes):
        self.scenes = self.scenes + scenes
    
    def draw(self):
        plt.close()
        fig = plt.figure()
        self.callback = _Button_callback(self.scenes)
        self.widgets = self.__configure_buttons()
        ax = plt.axes(autoscale_on = False)
        self.callback.set_axes(ax)
        fig.canvas.mpl_connect('button_press_event', self.callback.on_click)
        plt.show()
        self.callback.draw()
