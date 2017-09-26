#Program to detect the presence of brainwave signals and predict the mental state of the person

import serial
import pymysql
from scipy import signal
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from numpy import interp
from sklearn import preprocessing, cross_validation, neighbors,svm
from sklearn.linear_model import LinearRegression


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
#make connections to your database
#database rooted in localhost....
connection = pymysql.connect(host = 'localhost',user = 'root',passwd ='',db='first_db')
cursor = connection.cursor()

#data set to be read and training and testing of classifier is to be done...
df = pd.read_csv('./DATASETS/fft_data.csv')
#df = df.drop(['id'],axis=1)
df = df[['mean','alpha','beta','delta','gamma','class']]

x= np.array(df.drop(['class'],1))
y = np.array(df['class'])
for i in range(0,6):
        #x= preprocessing.scale(x)
        X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(x,y,test_size=0.3)

        #clf = neighbors.KNeighborsClassifier()
        clf = svm.SVC()

        clf.fit(X_train,Y_train)
        confidence= clf.score(X_test,Y_test)

cont = 0
while cont==0:
        input('starting analysis..... ')
        #data acquisition via the serial port
        prediction = np.zeros(5)
        for factor in range(0,5):
                ser = serial.Serial()
                ser.baudrate = 57600
                ser.port = 'COM3'
                ser.open()

                #read 200 sets of data in one go for 5 times 

                m = np.zeros(200)
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
                x_plot = range(0,L,1)
                y_plot = m#interp(m,-1000,1000)
                plt.figure(1)
                plt.subplot(211)
                plt.plot(x_plot,y_plot)
                

                print(L)
                NFFT = next_power2(L) # Next power of 2 from length of y
                Y = np.fft.fft(m,NFFT)/L
                obj=slice(0,int(NFFT/2+1))
                Y = 2*abs(Y[obj])
                lfft = len(Y)
                x1_plot = range(0,lfft,1)
                y1_plot = Y
                plt.subplot(212)
                plt.plot(x1_plot,y1_plot)

                mn = np.mean(Y)         #formulate the mean value of the FFT signal
                data_test = np.zeros(5)
                count =0
                data_test[count] = mn
                count+= 1
                
                total = 0
                for i in range(0,129):
                        total+=Y[i]
                sumup = 0
                for i in range(8,14):
                        sumup+=Y[i]
                data_test[count]= sumup/total
                count+=1

                alpha = data_test[1]*100  #percentage of alpha waves

                sumup = 0
                for i in range(14,30):
                        sumup+=Y[i]
                data_test[count]= sumup/total
                count+=1

                beta = data_test[2]*100  #percentage of beta waves

                sumup = 0
                for i in range(0,4):
                        sumup+=Y[i]
                data_test[count]= sumup/total
                count+=1

                delta = data_test[3]*100  #percentage of delta waves

                sumup = 0
                for i in range(40,100):
                        sumup+=Y[i]
                data_test[count]= sumup/total
                count+=1

                gamma = data_test[4]*100  #percentage of gamma waves


                #prediction of the output classification
                example_measures = data_test
                example_measures = example_measures.reshape(1, -1)
                prediction[factor] = (clf.predict(example_measures))

        count1=count2=count3=count4=count5=0
        for i in range(0,len(prediction)):
                if prediction[i] == 1:
                        count1+=1
                elif prediction[i] == 2:
                        count2+=1
                elif prediction[i] == 3:
                        count3+=1
                elif prediction[i] == 4:
                        count4+=1
                else:
                        count5+=1
        if count1>3:
                result = 'Consult the doctor u may be epileptic'
        elif count1>=2 and count4>=2:
                result ='You may be stressed or epileptic'
        elif count4>=3:
                result = 'You are highly Stressed'
        elif count4>=2:
                result = 'You are thinking'
        elif count3>=3:
                result = 'You are concentrating'
        elif count3>=2 and count2>=2:
                result = 'You are distracted'
        elif count2>=2:
                result = 'You are calm'
        else:
                result = 'You are sleepy'
                              
        print(result)
        sql = ("INSERT INTO data(alpha,beta,delta,gamma,prediction) VALUES ('%d', '%d', '%d', '%d', '%s')" %(alpha,beta,delta,gamma,result))
        cursor.execute(sql)
        connection.commit()
        plt.show()
        cont = int(input('Continue ? '))
print('complete')
connection.close()
