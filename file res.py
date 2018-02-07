#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


class CAN_FRAME() :

    l=[]

    def  lines_res(self, lines):
        for line in range(len(lines)):
            self.line_res(lines[line].strip('\n'))
        canframe = pd.DataFrame(np.array(self.l), columns=['time', 'id', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'count'])
        #16 进制转换为10进制
        canframe=canframe[['d0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7']].applymap(self.hex_to_dec)
        print(canframe)

    def  line_res(self, line):
        if len(line)>45:
            #分割为List
            buf = line.split(' ')
            #remove blank space
            while '' in buf:
                buf.remove('')
            while len(buf) < 11:
                buf.insert(len(buf)-1,'0')
            self.l.append(buf)
           # self.canframe.append(pd.DataFrame(np.array(buf).reshape(1, 11),columns=['time', 'id', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'count']),ignore_index=True)
            #print(line[0:8])
            #self.canframe['time']=line[0:8]
            #print(self.canframe)

    def hex_to_dec(self, x):
        return int(x, 16)

f = open('2017.txt', 'r', encoding='utf-8')
CAN_FRAME().lines_res(f.readlines())