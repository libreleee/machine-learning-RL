import time
import tkinter as tk
import tkinter.font
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import numpy as np

global label

global maxRowCnt
MAX_ROW =120 

class Env(tk.Tk):

    premaxStrike = 0
    ohlc = {'strike': 0, 'code': '', 'dir': 0, 'strike': 0, 'o': 0.00, 'h': 0.0, 'l': 0.00, 'c': 0.00}

    codeValCall15, codeValCall20 , codeValCall30 = '', '', ''
    codeValPutt15, codeValPutt20 , codeValPutt30 = '', '', ''

    dfCall = pd.DataFrame([ohlc])
    dfPutt = pd.DataFrame([ohlc])

    def __init__(self, _maxRowCnt):
        super(Env, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.action_size = len(self.action_space)
        self.geometry('{0}x{1}'.format(700, 600))
        self.configure(background='white')
        #scrollbar = tk.Scrollbar()
        #scrollbar.pack(side='right', fill='y')

        self.counter = 0
        self.rewards = []
        self.goal = []

        self.maxRowCnt = _maxRowCnt
        #self.shapes = self.load_images()
        self.canvas = self._build_canvas()



    def _build_canvas(self):
      
        # Set the canvas scrolling region
        canvas.config(scrollregion=canvas.bbox("all"))
        #canvas.pack()

        #return canvas
        return


    def reset(self):
        self.update()
        time.sleep(0.5)

    def step(self, action):
        self.counter += 1
        #self.render()

        done = False
        reward = 0

        return reward, done

    def render(self):
    
        self.update()


    def drawLabel(self):
        global label

    def updatePrice(self,istrike, ohlc):

        start = istrike['maxStrike']
     


