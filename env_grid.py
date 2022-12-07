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
        global label

        def mouseClick(event, obj):
            event.widget.config(borderwidth=2, relief='solid')

        self.grid_rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        frame_main = tk.Frame(self, bg="whitesmoke")
        frame_main.grid(sticky='news')

        label1 = tk.Label(frame_main, text="Label 1", fg="green")
        label1.grid(row=0, column=0, pady=(5, 0), sticky='nw')
        label2 = tk.Label(frame_main, text="Label 2", fg="white", bg="lightblue2")
        label2.grid(row=1, column=0, pady=(5, 0), sticky='nw')
        label3 = tk.Label(frame_main, text="Label 3", fg="red")
        label3.grid(row=3, column=0, pady=5, sticky='nw')

        frame_canvas = tk.Frame(frame_main)
        frame_canvas.grid(row=2, column=1, pady=(5, 0), sticky='nw')
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        frame_canvas.grid_propagate(False)

        # Add a canvas in that frame
        canvas = tk.Canvas(frame_canvas, bg="white" )
        canvas.grid(row=0, column=0, sticky="news")
        # Link a scrollbar to the canvas
        sb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        sb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=sb.set)

        # Create a frame to contain the price label
        frame_price = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=frame_price, anchor='nw')

        font = tkinter.font.Font(family="굴림", size=10)
        cols = 9
        #rows =  MAX_ROW
        rows = self.maxRowCnt
        label =[[tk.Label() for j in range(cols)] for i in range(rows)]
        for i in range(rows):
            for j in  range(cols):
                if(j == 4):
                    #strike
                    label[i][4] = tk.Label(frame_price, width=6, height = 1, borderwidth=1, relief="flat", fg='Black', bg = 'lightblue2', font = font)
                    label[i][4].grid(row = i, column = 4)
                else:
                    label[i][j] = tk.Label(frame_price, width = 7, height = 1, borderwidth=1, relief="flat", fg='Black',bg='white', font=font)
                    label[i][j].grid(row=i, column=j)

                if(j != 4) :
                    label[i][j].bind("<Button>", lambda event, obj=label[i][j]: mouseClick(event, obj))

            #mouse evevt
            #labelCc[i].bind("<Button>", lambda event, obj=labelCc[i]: mouseClick(event, obj))

        window_col = 9
        window_row = 25
        frame_price.update_idletasks()
        # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
        cols_width = sum([label[0][j].winfo_width() for j in range(0, window_col)])
        rows_height = sum([label[i][0].winfo_height() for i in range(0, window_row)])
        frame_canvas.config(width=cols_width + sb.winfo_width(),height=rows_height)

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
        # 게임 속도 조정
        #time.sleep(0.05)
        self.update()

    #
    def drawLabel(self):
        global label

        strike = self.premaxStrike
        #for i in range(MAX_ROW):
          
        for i in range(self.maxRowCnt):
            for j in range(9):
                if(j == 4):
                    label[i][4]['text'] = "{:3.2f}".format(strike)
                else:
                    label[i][j]['text'] = ''
            strike -= 2.5

    def updatePrice(self,istrike, ohlc):

        start = istrike['maxStrike']
        if self.premaxStrike != start:
            self.premaxStrike = start
            self.drawLabel()

        loc = ohlc['strike']
        if(ohlc['strike'] % 10 == 2 or ohlc['strike'] % 10 == 7):
            loc = ohlc['strike'] +.5

        start1 = start
        if (start % 10 == 2 or start % 10 == 7):
            start1 = start + .5

        indx = (int)((start1 - loc) / 2.5)
        #if indx >= MAX_ROW or indx < 1:
        if indx >= self.maxRowCnt or indx < 1:
            return

        #CALL
        if ohlc['dir'] == "2":
            label[indx][0]['text'] = ohlc['l']
            label[indx][1]['text'] = ohlc['h']
            label[indx][2]['text'] = ohlc['o']
            label[indx][3]['text'] = "{:3.2f}".format(ohlc['c'])
            self.dfCall.loc[len(self.dfCall)] = ohlc
            #print(self.dfCall)
            if self.codeValCall15 == '':
                if (ohlc['c'] >= 1.50) and (ohlc['c'] < 2.0):
                    self.codeValCall15 = ohlc['code']
            if self.codeValCall20 == '':
                if (ohlc['c'] >= 2.0) and (ohlc['c'] < 3.0):
                    self.codeValCall20 = ohlc['code']
            if self.codeValCall30 == '':
                if (ohlc['c'] >= 3.0) and (ohlc['c'] < 4.0):
                    self.codeValCall30 = ohlc['code']
            #print("Call1.5: ", self.codeValCall15, " Call2.0: ", self.codeValCall20, " Call3.0: ", self.codeValCall30)

            #
            #
            xC = (self.dfCall[self.dfCall['code'] == self.codeValCall20])['c'].to_numpy()
            #print(x)

            if(len(xC) > 2):
                maxC = argrelextrema(xC, np.greater)[0]
                yC = [xC[i] for i in maxC]
                plt.subplot(211)
                plt.plot(xC)
                plt.plot(maxC, yC, 'rs')

                for a, b in zip(maxC, yC):
                    plt.text(a, b, "{:3.2f}".format(b))

                #plt.show(block=False)
                plt.draw()
                plt.pause(0.0001)
                #plt.clf()
        #PUT
        else:
            try:
                label[indx][5]['text'] = "{:3.2f}".format(ohlc['c'])
                label[indx][6]['text'] = ohlc['o']
                label[indx][7]['text'] = ohlc['h']
                label[indx][8]['text'] = ohlc['l']
                self.dfPutt.loc[len(self.dfPutt)] = ohlc
                #print(dfPutt)
            except IndexError:  # 에러 종류
                print('{} - 에러.'.format(indx))  # 에러가 발생 했을 경우 처리할 코드

            if self.codeValPutt15 == '':
                if (ohlc['c'] >= 1.50) and (ohlc['c'] < 2.0):
                    self.codeValPutt15 = ohlc['code']
            if self.codeValPutt20 == '':
                if (ohlc['c'] >= 2.0) and (ohlc['c'] < 3.0):
                    self.codeValPutt20 = ohlc['code']
            if self.codeValPutt30 == '':
                if (ohlc['c'] >= 3.0) and (ohlc['c'] < 4.0):
                    self.codeValPutt30 = ohlc['code']
            #
            #
            xP = (self.dfPutt[self.dfPutt['code'] == self.codeValPutt20])['c'].to_numpy()
            # print(x)

            if (len(xP) > 2):
                maxP = argrelextrema(xP, np.greater)[0]
                yP = [xP[i] for i in maxP]
                plt.subplot(212)
                plt.plot(xP)
                plt.plot(maxP, yP, 'bs')

                for a, b in zip(maxP, yP):
                    plt.text(a, b, "{:3.2f}".format(b))

                # plt.show(block=False)
                plt.draw()
                plt.pause(0.0001)
                #plt.clf()



