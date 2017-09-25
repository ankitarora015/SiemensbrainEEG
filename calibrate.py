#program to calibrate the required information and store it in the datasets
import serial
from scipy import signal
import pandas as pd
import math
import numpy as np
import csv as file

#define the function to determine 2^next power
def next_power2(x):
	value=1
	while value<=x :
		value = value << 1;
	return value;

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#data acquisition via the serial port
count = 5
for i in range(0,count):
        classify = input('Enter class : ')
        ser = serial.Serial()
        ser.baudrate = 57600
        ser.port = 'COM3'
        ser.open()

        m = np.zeros(200)
        n = np.zeros(200)
        i = 0
        while i<200:
              a = ser.readline()
              if is_number(a)== True:
                    m[i] = int(a)
                    i = i+1

        ser.close()

        #analytics of received dataset
        fs = 200.0  # Sample frequency (Hz)
        f0 = 60.0  # Frequency to be removed from signal (Hz)
        Q = 30.0  # Quality factor
        w0 = f0/(fs/2)  # Normalized Frequency
        # Design notch filter
        b, a = signal.iirnotch(w0, Q)
        # Frequency response
        m = (signal.lfilter(b, a, m))

        mu = int(np.mean(m))
        m = (100*(m-mu))

        #finding out the FFT of the signal
        L=len(m)
        print(L)
        NFFT = next_power2(L) # Next power of 2 from length of y
        Y = np.fft.fft(m,NFFT)/L
        obj=slice(0,int(NFFT/2+1))
        Y = 2*abs(Y[obj])
        lfft = len(Y)

        mn = np.mean(Y)
        data_test = np.zeros(7)
        count =0
        
        total = 0
        for i in range(0,129):
                total+=Y[i]
        sumup = 0
        for i in range(0,4):
                sumup+=Y[i]
        data_test[count]= sumup/total
        count+=1

        sumup = 0
        for i in range(4,8):
                sumup+=Y[i]
        data_test[count]= sumup/total
        count+=1

        sumup = 0
        for i in range(8,13):
                sumup+=Y[i]
        data_test[count]= sumup/total
        count+=1

        sumup = 0
        for i in range(13,30):
                sumup+=Y[i]
        data_test[count]= sumup/total
        count+=1

        sumup = 0
        for i in range(30,40):
                sumup+=Y[i]
        data_test[count]= sumup/total
        count+=1

        sumup = 0
        for i in range(40,100):
                sumup+=Y[i]
        data_test[count]= sumup/total
        count+=1

        data_test[count] = mn
        count+=1

        
        filtercol = ''
        for i in range(0,L):
                filtercol = filtercol + str(m[i])+','

        fftcol = ''
        for i in range(0,lfft):
                fftcol = fftcol + str(Y[i])+','
        filtercol = filtercol + str(classify) + "\n"

        an =''
        for i in range(0,count):
                if i==(count-1):
                        an = an+str(data_test[i])
                else:
                        an = an+str(data_test[i])+','

        fftcol = fftcol + str(classify) +"," + an + "\n"

        #write filter data
        file = open('filter_data.csv',"a")
        file.write(filtercol)
        file.close()

        #write fft data
        file = open('fft_data.csv',"a")
        file.write(fftcol)
        file.close()
print('Writing complete !!')
