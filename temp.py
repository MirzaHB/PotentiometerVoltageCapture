# -*- coding: utf-8 -*-
"""
PYTHON DEMO -- PART 2
Created on Wed Nov  2 11:54:30 2022

CAPTURING 16 BIT INT AND FLOAT NUMBERS OVER A TIME INTERVAL
Time stamps received numbers separated by \n
Saves in Dataframe
Saves in csv
Plots received data versus time

@author: Rushi V
"""

import numpy as np
import math 
import csv
import serial  # pip install pyserial  or conda install pyserial
import time
import pandas as pd
import plotly.express as px


import plotly.io as pio  # needed to plot plotly graphs in spyder
pio.renderers.default = 'browser' # to plot plotly graphs in browser


## OPEN SERIAL PORT 
ser = serial.Serial(port= "/dev/cu.usbserial-0001", baudrate = 9600, bytesize = 8, timeout =2, stopbits = serial.STOPBITS_ONE)


## INITIALIZATIONS
rxNumsStr = ''      #string to store received uint16_t numbers 
rxValuesList = []      #List to store received uint16_t numbers in int form 
rxTimesList = []   #list to store time stamps of received uint16_t numbers
rxBuffersList = []   #List of ADC buffers
rxVoltageList = []   #list of ADC voltages

startTime = time.time()   #Start time

## CAPTURE UART DATA
while(time.time() - startTime < 10):  #record data for 1 sec
    line =ser.readline() # reads uint16_t nums as single bytes 
    if ((line != b' \n') and (line != b'\n')) : #removes any '\n' without num captures
        rxNumsStr = rxNumsStr + line.decode('Ascii')  # Converts string of received uint16_t num to ASCII and combines Rx nums into 1 string
        timeMeas = time.time() -startTime # Time stamp received number
        rxTimesList.append(timeMeas) #save time stamps in a list

## CLOSE SERIAL PORT    
ser.close()  # close any open serial ports



### Rx DATA CLEANUP AND STRING TO FLOAT CONVERSION
rxNumsStr = rxNumsStr.replace('\x00','')  #\x00 seems to be sent with Disp2String()
rxNumsStr = rxNumsStr.strip() # remove unwanted chars and spaces 
rxValuesList = rxNumsStr.split(' \n ')  # split string by \n n store in list
# print(rxNumsList)




# Revieve value for buffer twice and split
for elem in rxValuesList:
    if ":" in elem:
        temp = elem.split(':')
        rxBuffersList.append(temp[0])
        rxVoltageList.append(temp[1])


# Convert second value recieved to voltage
rxBuffersList = [float(elem) for elem in rxBuffersList]  
rxVoltageList = [(float(elem)*3/1023) for elem in rxVoltageList]  


# Fix length of value indexes
if len(rxTimesList) > len(rxBuffersList):
    size = len(rxTimesList)
    rxTimesList.remove(rxTimesList[size - 1])


rxTimesList.append(10)
rxBuffersList.append(rxBuffersList[len(rxBuffersList) - 1])
rxVoltageList.append(rxVoltageList[len(rxVoltageList) - 1])


### CONVERT Rx DATA INTO DATA FRAME
dFBuffers = pd.DataFrame()
dFBuffers['Rx Buffer Time (sec)'] = rxTimesList
dFBuffers['Rx ADC Buffer Values'] = rxBuffersList




### PLOT Rx DATA VS Rx TIME
fig = px.line(dFBuffers, x='Rx Buffer Time (sec)', y='Rx ADC Buffer Values', title = 'RS232 ADC Buffers vs Time')
fig.show()


### CONVERT Rx DATA INTO DATA FRAME
dFVoltage = pd.DataFrame()
dFVoltage['Rx Voltage Time (sec)'] = rxTimesList
dFVoltage['Rx ADC Voltage Values'] = rxVoltageList



### PLOT Rx DATA VS Rx TIME
fig = px.line(dFVoltage, x='Rx Voltage Time (sec)', y='Rx ADC Voltage Values', title = 'RS232 ADC Voltages vs Time')
fig.show()



### COPY RX DATA AND RX TIME IN CSV AND XLS FILES
dFBuffers.to_csv('RxBuffersDataFloat.csv', index = True)
dFBuffers.to_excel('RxBuffersDataFloat.xlsx', sheet_name='New Sheet')


### COPY RX DATA AND RX TIME IN CSV AND XLS FILES
dFVoltage.to_csv('RxVoltageDataFloat.csv', index = True)
dFVoltage.to_excel('RxVoltageDataFloat.xlsx', sheet_name='New Sheet')