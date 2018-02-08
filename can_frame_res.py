#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


class CAN_FRAME() :

    def  get_dataframe_original(self, lines):
        l=[]
        columns = ['time', 'id', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'count']
        for line in range(len(lines)):
            self.line_res(lines[line].strip('\n') ,l)
        return pd.DataFrame(np.array(l), columns=columns)

    def  line_res(self, line,list):
        if len(line)>45:
            #分割为List
            buf = line.split(' ')
            #remove blank space
            while '' in buf:
                buf.remove('')
            #add zeros to fit the size
            while len(buf) < 11:
                buf.insert(len(buf)-1, '0')
            if( len(buf) == 11):
                list.append(buf)

    def hex_to_dec(self, x):
        return int(x, 16)

    def dataframe_to_int(self,list,columns):
        dataframe= pd.DataFrame(np.array(list), columns=columns)
        dataframe_mapped=dataframe[[ 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7']].applymap(self.hex_to_dec)
        dataframe_mapped.insert(0,'time',dataframe['time'])
        dataframe_mapped.insert(1, 'id', dataframe['id'])
        dataframe_mapped.insert(2, 'd0', dataframe['d0'])
        dataframe_mapped.insert(dataframe_mapped.columns.__len__(), 'count', dataframe['count'])
        return  dataframe_mapped

    def get_data_frame(self,lines):
        l=[]
        columns = ['time', 'id', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'count']
        for line in range(len(lines)):
            self.line_res(lines[line].strip('\n'), l)
        return self.dataframe_to_int(l, columns)

#f = open('2017.txt', 'r', encoding='utf-8')
#print(CAN_FRAME().get_data_frame(f.readlines()))