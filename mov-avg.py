#!/usr/bin/python

''' basically movingaverage(data,period) , where data is a list/tuple? '''

import matplotlib.pyplot as plt
from movingaverage import *

plt.plot([1,2,3,4])
plt.ylabel('some numbers')
plt.show()


# basically need to read the data from our history file, put into a list and then use the movingaverage

period=10 # arbitrary here - maybe ask what moving average you want at the start?
fd=open("./data.txt","r")

dat=fd.readlines()
data=[]
for line in dat:
	splitline=line.split()
	num=float(splitline[-1])
	if int(num) != 0:
	  data.append(num)


for num in list(movingaverage(data,period)):
  print "moving average = %0.2f "  % num

