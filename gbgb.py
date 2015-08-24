#!/usr/bin/python

import os
import re
import sys
import urllib
from movingaverage import *
from multiprocessing import Process

def main():
    for name in "./ratings.out.csv","./calctime-mvavg.out.csv","./splits-mvavg.out.csv","winnerstime-mvavg.out.csv":
        if os.path.exists(name):
            os.remove(name)
    getdognames()

def getdognames():
    """ this function reads a list of dognames from file """
    dognames="./dognames.txt"
    dogname=open(dognames,"r").readlines()
    count=0
    for n in dogname:
        count+=1
        #print n
        readdogs(n)

def readdogs(dogname):
    """  this function reads the primary web page for eachdog """
    dogname=dogname.replace(" ","%20")
    f=urllib.urlopen("http://www.gbgb.org.uk/raceCard.aspx?dogName="+dogname)
    ddogname=dogname.rstrip()+".txt"
    webout=open(ddogname,"w")
    s=f.read()
    webout.write(s)
    f.close()
    webout.close()
    extractdata(ddogname,dogname)

def extractdata(filedogname,dogname):
    """  what this function does is to format the downloaded history - basically get rid of the extraneous html """
    from HTMLParser import HTMLParser
    dogname=dogname.rstrip()
    dogname=dogname.replace("%20","+")
    flag = 1
    fd=open(filedogname,"r")
    filedogname2=dogname + "-rh.txt"
    fd2=open(filedogname2,"w")
    data=fd.readlines()
    for line in data:
        if 'nbsp' in line:
            line = "" 
        if '<td align="center"' in line:
            fd2.write(line)
            flag = 0
        if re.search('\s+\<\/tbody\>',line):
            flag = 1
        if re.search('\s+\<\/tr\>\<tr class="Grid',line):
            flag = 1
        if not flag and not '<td align="center"' in line:
            fd2.write(line)
    fd.close()
    os.remove(filedogname)
    fd2.close()
    analyse_data(dogname)

def analyse_data(dogname):
    """  this function extracts the dog data we want from its history """
    count=0
    dogname=dogname.replace("%20","+")
    fd=open(dogname +"-data.csv","w")
    fd3=open(dogname + "-rh.txt","r+")
    data=fd3.readlines()
    fd3.close()
    for i,lline in enumerate(data):
        newline = (re.sub('<[^<]+?>', ',', lline))
        newline = (re.sub('Race', ' ', newline))
        newline = (re.sub('Meeting', ' ', newline))
        newline = (re.sub(',,',',',newline))
        newline = (re.sub('^[		]*,','',newline))
        newline = (re.sub(',, ,, ,','',newline))
	laststring = [None] * 15
	txt = newline
        if newline.strip():
            for i in range(1,8):
	        laststring[i] = txt.split(',')[i]
                fd.write(laststring[i])
                fd.write(",") 
	    for j in range(5,0,-1):
	        laststring[j] = txt.split(',')[-j]
                fd.write(laststring[j])
	        if j != 1:
                    fd.write(",")

    fd.close()
    calc_moving_average(dogname)
    os.remove(dogname + "-rh.txt")

def calc_moving_average(dogname):
    """ basically movingaverage(data,period) , where data is a list/tuple? """
    # thinking I should move these ratings into  a separate file?
    ratings={
    'A1':{1:110,2:108,3:106,4:104,5:102,6:100},
    'A2':{1:100,2:98,3:96,4:94,5:92,6:90},
    'A3':{1:90,2:88,3:86,4:84,5:82,6:80},
    'A4':{1:80,2:78,3:76,4:74,5:72,6:70},
    'A5':{1:70,2:68,3:66,4:64,5:62,6:60},
    'A6':{1:60,2:58,3:56,4:54,5:52,6:50},
    'A7':{1:50,2:48,3:46,4:44,5:42,6:40},
    'A8':{1:40,2:38,3:36,4:34,5:32,6:30},
    'A9':{1:30,2:28,3:26,4:24,5:22,6:20},
    'A10':{1:20,2:18,3:16,4:14,5:12,6:10},
    'A11':{1:10,2:9,3:8,4:7,5:6,6:5},
    'A15':{1:6,2:5,3:4,4:3,5:2,6:1},
    'S1':{1:110,2:108,3:106,4:104,5:102,6:100},
    'S2':{1:100,2:98,3:96,4:94,5:92,6:90},
    'S3':{1:90,2:88,3:86,4:84,5:82,6:80},
    'S4':{1:80,2:78,3:76,4:74,5:72,6:70},
    'S5':{1:70,2:68,3:66,4:64,5:62,6:60},
    'S6':{1:60,2:58,3:56,4:54,5:52,6:50},
    'S7':{1:50,2:48,3:46,4:44,5:42,6:40},
    'S8':{1:40,2:38,3:36,4:34,5:32,6:30},
    'S9':{1:30,2:28,3:26,4:24,5:22,6:20},
    'B1':{1:110,2:108,3:106,4:104,5:102,6:100},
    'B2':{1:100,2:98,3:96,4:94,5:92,6:90},
    'B3':{1:90,2:88,3:86,4:84,5:82,6:80},
    'B4':{1:80,2:78,3:76,4:74,5:72,6:70},
    'B5':{1:70,2:68,3:66,4:64,5:62,6:60},
    'B6':{1:60,2:58,3:56,4:54,5:52,6:50},
    'B7':{1:50,2:48,3:46,4:44,5:42,6:40},
    'B8':{1:40,2:38,3:36,4:34,5:32,6:30},
    'B9':{1:30,2:28,3:26,4:24,5:22,6:20},
    'B10':{1:20,2:18,3:16,4:14,5:12,6:10},
    'B11':{1:10,2:9,3:8,4:7,5:6,6:5},
    'E1':{1:110,2:108,3:106,4:104,5:102,6:100},
    'E2':{1:100,2:98,3:96,4:94,5:92,6:90},
    'E3':{1:90,2:88,3:86,4:84,5:82,6:80},
    'E4':{1:80,2:78,3:76,4:74,5:72,6:70},
    'E5':{1:70,2:68,3:66,4:64,5:62,6:60},
    'E6':{1:60,2:58,3:56,4:54,5:52,6:50},
    'E7':{1:50,2:48,3:46,4:44,5:42,6:40},
    'E8':{1:40,2:38,3:36,4:34,5:32,6:30},
    'E9':{1:30,2:28,3:26,4:24,5:22,6:20},
    'E10':{1:20,2:18,3:16,4:14,5:12,6:10},
    'E11':{1:10,2:9,3:8,4:7,5:6,6:5},
    'M1':{1:110,2:108,3:106,4:104,5:102,6:100},
    'M2':{1:100,2:98,3:96,4:94,5:92,6:90},
    'M3':{1:90,2:88,3:86,4:84,5:82,6:80},
    'M4':{1:80,2:78,3:76,4:74,5:72,6:70},
    'M5':{1:70,2:68,3:66,4:64,5:62,6:60},
    'M6':{1:60,2:58,3:56,4:54,5:52,6:50},
    'M7':{1:50,2:48,3:46,4:44,5:42,6:40},
    'M8':{1:40,2:38,3:36,4:34,5:32,6:30},
    'M9':{1:30,2:28,3:26,4:24,5:22,6:20},
    'M10':{1:20,2:18,3:16,4:14,5:12,6:10},
    'TC':{1:110,2:110,3:110,4:110,5:110,6:110},
    'HP':{1:110,2:110,3:110,4:110,5:110,6:110},
    'H1':{1:110,2:108,3:106,4:104,5:102,6:100},
    'H2':{1:100,2:98,3:96,4:94,5:92,6:90},
    'H3':{1:90,2:88,3:86,4:84,5:82,6:80},
    'H4':{1:80,2:78,3:76,4:74,5:72,6:70},
    'H5':{1:70,2:68,3:66,4:64,5:62,6:60},
    'H6':{1:60,2:58,3:56,4:54,5:52,6:50},
    'H7':{1:50,2:48,3:46,4:44,5:42,6:40},
    'H8':{1:40,2:38,3:36,4:34,5:32,6:30},
    'H9':{1:30,2:28,3:26,4:24,5:22,6:20},
    'H10':{1:20,2:18,3:16,4:14,5:12,6:10},
    'H11':{1:10,2:9,3:8,4:7,5:6,6:5},
    'HS2':{1:10,2:9,3:8,4:7,5:6,6:5},
    'OR':{1:100,2:100,3:100,4:100,5:100,6:100},
    'KS':{1:10,2:9,3:8,4:7,5:6,6:5},
    'P1':{1:110,2:108,3:106,4:104,5:102,6:100},
    'P2':{1:100,2:98,3:96,4:94,5:92,6:90},
    'P3':{1:90,2:88,3:86,4:84,5:82,6:80},
    'P4':{1:80,2:78,3:76,4:74,5:72,6:70},
    'P5':{1:70,2:68,3:66,4:64,5:62,6:60},
    'P6':{1:60,2:58,3:56,4:54,5:52,6:50},
    'P7':{1:50,2:48,3:46,4:44,5:42,6:40},
    'P8':{1:40,2:38,3:36,4:34,5:32,6:30},
    'P9':{1:30,2:28,3:26,4:24,5:22,6:20},
    'P10':{1:20,2:18,3:16,4:14,5:12,6:10},
    'P11':{1:10,2:10,3:10,4:10,5:10,6:10},
    'D1':{1:110,2:108,3:106,4:104,5:102,6:100},
    'D2':{1:100,2:98,3:96,4:94,5:92,6:90},
    'D3':{1:90,2:88,3:86,4:84,5:82,6:80},
    'D4':{1:80,2:78,3:76,4:74,5:72,6:70},
    'D5':{1:70,2:68,3:66,4:64,5:62,6:60},
    'D6':{1:60,2:58,3:56,4:54,5:52,6:50},
    'D7':{1:50,2:48,3:46,4:44,5:42,6:40},
    'D8':{1:40,2:38,3:36,4:34,5:32,6:30},
    'D9':{1:30,2:28,3:26,4:24,5:22,6:20},
    'D10':{1:20,2:18,3:16,4:14,5:12,6:10},
    'D11':{1:10,2:10,3:10,4:10,5:10,6:10},
    'IT':{1:10,2:9,3:8,4:7,5:6,6:5},
    'IV':{1:10,2:9,3:8,4:7,5:6,6:5},
    }

    # we now want to add the moving average of the actual, not calculated time and also for the split time.
    period=4 # arbitrary here - maybe ask what moving average you want at the start?
    try:
        fd=open(dogname +"-data.csv","r")
        fd2=open("ratings.out.csv","a")
        fd3=open("calctime-mvavg.out.csv","a")
        fd3s=open("splits-mvavg.out.csv","a")
        fd3wt=open("winnerstime-mvavg.out.csv","a")
        fd3po=open("position-mvavg.out.csv","a")
        fd4po=open("position.out.csv","a")
    except:
        pass
    dat=fd.readlines()
    data=[]
    data_calctime=[]
    data_brkn=[]
    data_wint=[]
    data_pos=[]
    cnt=1
    # format of line is
    # 12 columns - from left to right remember 1st is pos 0 last is pos 11
    # 
    error = 0
    for line in dat:
        splitline=line.split(",")
        if len(splitline) == 12:
            pos=splitline[3]
            brk=splitline[2]
            if brk == '&nbsp;':
                brk = 0
            brkn=float(brk)
            data_brkn.append(brkn)
            grade=splitline[10]
            pos=int(pos)
            # this is to ensure position is within range
            if 1 <= pos <=6:
                pass
            else:
                pos = 6
            going=splitline[4]
            wint=splitline[7]
            calt=splitline[11]
	    if "&nbsp;" in calt:
	        calt = wint
		error =1
            calctime = float(calt)
            winnerstime = float(wint)
            rat=ratings[grade][pos]
            datal=dogname+","+grade+"\n"
            data_pos.append(pos)
            if calctime != 0:
                data_calctime.append(calctime)
            if winnerstime != 0:
                data_wint.append(winnerstime)
            if int(rat) != 0:
                data.append(rat)
            cnt+=1
    if error == 1:
	print "dont trust " + dogname + " finish time appears wrong"
	error = 0
    if len(dat) <period:
        period=len(data)
        print period
    # from here to end of function needs a sort out.
    klist=list(movingaverage(data,period))
    klist=[int(elem) for elem in klist ]
    klist1=list(movingaverage(data_calctime,period))
    klist1=[round(elem,2) for elem in klist1]
    klist2=list(movingaverage(data_calctime,period))
    klist2=[round(elem,2) for elem in klist2]
    klist3=list(movingaverage(data_brkn,period))
    klist3=[round(elem,2) for elem in klist3]
    klist4=list(movingaverage(data_wint,period))
    klist4=[round(elem,2) for elem in klist4]
    klist5=list(movingaverage(data_pos,period))
    klist5=[round(elem,2) for elem in klist5]
    klist6=list(data_pos)
    dogname=dogname.replace('%20','+')
    v=(dogname,klist)
    v1=(dogname,klist1)
    v2=(dogname,klist2)
    v3=(dogname,klist3)
    v4=(dogname,klist4)
    v5=(dogname,klist5)
    v6=(dogname,klist6)
    value=str(v)
    value1=str(v1)
    value2=str(v2)
    value3=str(v3)
    value4=str(v4)
    value5=str(v5)
    value6=str(v6)
    fd2.write(value)
    fd3.write(value2)
    fd3s.write(value3)
    fd3wt.write(value4)
    fd3po.write(value5)
    fd4po.write(value6)
    fd2.write("\n")
    fd3.write("\n")
    fd3s.write("\n")
    fd3wt.write("\n")
    fd3po.write("\n")
    fd4po.write("\n")
    fd2.close()
    fd3.close()
    fd3s.close()
    fd3wt.close()
    fd3po.close()
    fd4po.close()

if __name__ == '__main__':
    # maybe just maybe put some error checking here
    main()
