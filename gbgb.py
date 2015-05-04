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
    dognames="./dognames.txt"
    """ this function reads a list of dognames from file """
    dogname=open(dognames,"r").readlines()
    count=0
    for n in dogname:
        count+=1
        print n
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
    # need to look closer at this as getting 14-15 fields - should be consistent!
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
    'A1':{1:138,2:120,3:112,4:94,5:86,6:78},
    'A2':{1:130,2:112,3:104,4:86,5:78,6:70},
    'A3':{1:122,2:104,3:96,4:78,5:70,6:62},
    'A4':{1:114,2:96,3:88,4:70,5:62,6:54},
    'A5':{1:106,2:88,3:80,4:62,5:54,6:46},
    'A6':{1:98,2:80,3:72,4:54,5:46,6:38},
    'A7':{1:90,2:72,3:64,4:46,5:38,6:30},
    'A8':{1:82,2:64,3:56,4:38,5:30,6:22},
    'A9':{1:74,2:56,3:48,4:30,5:22,6:14},
    'A10':{1:66,2:48,3:40,4:22,5:14,6:8},
    'A11':{1:58,2:40,3:32,4:14,5:6,6:6},
    'B1':{1:58,2:40,3:32,4:14,5:6,6:6},
    'B2':{1:58,2:40,3:32,4:14,5:6,6:6},
    'S1':{1:122,2:104,3:96,4:78,5:70,6:62},
    'S2':{1:114,2:96,3:88,4:70,5:62,6:54},
    'S3':{1:106,2:88,3:80,4:62,5:54,6:46},
    'S4':{1:98,2:80,3:72,4:54,5:46,6:38},
    'S5':{1:90,2:72,3:64,4:46,5:38,6:30},
    'S6':{1:82,2:64,3:56,4:38,5:30,6:22},
    'S7':{1:74,2:56,3:48,4:30,5:22,6:14},
    'S8':{1:66,2:48,3:40,4:22,5:14,6:8},
    'S9':{1:58,2:40,3:32,4:14,5:6,6:6},
    'HP':{1:90,2:72,3:64,4:46,5:38,6:30},
    'H1':{1:82,2:64,3:56,4:38,5:30,6:22},
    'H2':{1:74,2:56,3:48,4:30,5:22,6:14},
    'H3':{1:66,2:48,3:40,4:22,5:14,6:8},
    'H4':{1:58,2:40,3:32,4:14,5:6,6:6},
    'OR':{1:138,2:120,3:112,4:94,5:86,6:78},
    'KS':{1:138,2:120,3:112,4:94,5:86,6:78},
    'P1':{1:90,2:72,3:64,4:46,5:38,6:30},
    'P2':{1:82,2:64,3:56,4:38,5:30,6:22},
    'P3':{1:74,2:56,3:48,4:30,5:22,6:14},
    'P4':{1:66,2:48,3:40,4:22,5:14,6:8},
    'P5':{1:58,2:40,3:32,4:14,5:6,6:6},
    'P6':{1:58,2:40,3:32,4:14,5:6,6:6},
    'P7':{1:58,2:40,3:32,4:14,5:6,6:6},
    'D1':{1:122,2:104,3:96,4:78,5:70,6:62},
    'D2':{1:114,2:96,3:88,4:70,5:62,6:54},
    'D3':{1:106,2:88,3:80,4:62,5:54,6:46},
    'D4':{1:98,2:80,3:72,4:54,5:46,6:38},
    'D5':{1:90,2:72,3:64,4:46,5:38,6:30},
    'IT':{1:138,2:120,3:112,4:94,5:86,6:78},
    'IV':{1:138,2:120,3:112,4:94,5:86,6:78}
    }
    # we now want to add the moving average of the actual, not calculated time and also for the split time.
    period=4 # arbitrary here - maybe ask what moving average you want at the start?
    try:
        fd=open(dogname +"-data.csv","r")
        fd2=open("ratings.out.csv","a")
        fd3=open("calctime-mvavg.out.csv","a")
        fd3s=open("splits-mvavg.out.csv","a")
        fd3wt=open("winnerstime-mvavg.out.csv","a")
    except:
        pass
    dat=fd.readlines()
    data=[]
    data_calctime=[]
    data_brkn=[]
    data_wint=[]
    cnt=1
    # format of line is
    # 12 columns - from left to right remember 1st is pos 0 last is pos 11
    # 
    error = 0
    for line in dat:
        splitline=line.split(",")
        if len(splitline) == 12:
            pos=splitline[1]
            brk=splitline[2]
            if brk == '&nbsp;':
                brk = 0
            brkn=float(brk)
            data_brkn.append(brkn)
            grade=splitline[10]
            #pos=pos[:-2]
            pos=int(pos)
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
    klist=list(movingaverage(data,period))
    klist=[int(elem) for elem in klist ]
    klist2=list(movingaverage(data_calctime,period))
    klist2=[round(elem,2) for elem in klist2]
    klist3=list(movingaverage(data_brkn,period))
    klist3=[round(elem,2) for elem in klist3]
    klist4=list(movingaverage(data_wint,period))
    klist4=[round(elem,2) for elem in klist4]
    dogname=dogname.replace('%20','+')
    v=(dogname,klist)
    v2=(dogname,klist2)
    v3=(dogname,klist3)
    v4=(dogname,klist4)
    value=str(v)
    value2=str(v2)
    value3=str(v3)
    value4=str(v4)
    fd2.write(value)
    fd3.write(value2)
    fd3s.write(value3)
    fd3wt.write(value4)
    fd2.write("\n")
    fd3.write("\n")
    fd3s.write("\n")
    fd3wt.write("\n")
    fd2.close()
    fd3.close()
    fd3s.close()
    fd3wt.close()

if __name__ == '__main__':
    main()
