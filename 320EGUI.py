from Tkinter import* 
import visa
import time
import csv
import random
import Tkinter, Tkconstants, tkFileDialog
import seabreeze.spectrometers as sb
import matplotlib
import threading
matplotlib.use('TkAgg')
from numpy import arange, sin, pi, linspace, cos
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
import matplotlib.animation as ani
import matplotlib.pyplot as plt
from multiprocessing import Process, Value, Array

def Initialize():
	if(v.get()==0):
		my_instrument = rm.open_resource('USB0::0x1313::0x8022::M00263679::0::INSTR')
	elif(v.get()==1):
		my_instrument = rm.open_resource('USB0::0x1313::0x8022::M00408735::0::INSTR')
	my_instrument.write(':PRANGE1 AUTO')
	my_instrument.write(':PRANGE2 AUTO')
def UpdateWave1():
	Wave1=':WAVEL1:VAL ' + txtTimeWave1.get()
	my_instrument.write(Wave1)

def UpdateWave2():
	Wave1=':WAVEL2:VAL ' + txtTimeWave2.get()
	my_instrument.write(Wave2)

def RefreshScale():
	my_instrument.write(':PRANGE1 AUTO')
	my_instrument.write(':PRANGE2 AUTO')

def RefreshDevice():
	Devices=rm.list_resources()
	lbl2.configure(text=Devices)

def RecordData():
	fn=txtFile.get()
	#Creating a csv file to be written to
	filename=fn+".csv"
	csvfile= open(filename, 'w')
	wr=csv.writer(csvfile)
	wr.writerow(['CLOCK','CHANNEL1','CHANNEL2'])
	fieldnames =['CLOCK','CHANNEL1','CHANNEL2']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	rt= int(txtTime.get())
	StopTime=time.time() + rt
	#Initializing variables I will be using
	Pow1=[]
	Pow2=[]
	Clk=[]
	i = 0
	#Loop where we iterate over the specified time period
	while (time.time() < StopTime):
		#Here we take in measurements and push them to an array
		power1=str(my_instrument.query(':POW1:VAL?'))
		power2=str(my_instrument.query(':POW2:VAL?'))
		Pow1.append(power1)
		Pow2.append(power2)
		Clk.append(time.clock())
		#Printing out values to see while we loop
		print("Time: %f Channel1: %s Channel2 %s"   % (time.clock(),power1, power2 ) )

	while (i < len(Pow1)):
		#Writing our array to a csv file
		writer.writerow({ 'CLOCK': Clk[i], 'CHANNEL1':Pow1[i], 'CHANNEL2':Pow2[i]})
		i = i + 1 
		
	#Closing CSV file	
	csvfile.close()	

def animate(i):
	global x
	global y 
	global xX
	global yY
	global yY2
	global y2
	x=x+.25
	y=sin(x)
	y2=cos(x)
  	#a=random.randint(1,10)
  	xX.append(x)
	yY.append(y) 
	yY2.append(y2)

	ax1.plot(xX,yY)
	ax2.plot(xX,yY2)
	ax2.set_xlim((x-25),(x+5))
	ax1.set_xlim((x-25),(x+5))
	#ax2.plot(b,a)
#For Adjusting GUI
def UpdateLiveValues():
	Val1= str(time.clock()) + " W"
	yPrint1=round(y,3)
	yPrint2=round(y2,3)
	lbl6.configure(text=yPrint1)
	lbl7.configure(text=yPrint2)
	window.after(30,UpdateLiveValues)

def StartStopRecord():
	TimeStart= time.clock()
	TimeElapsed= time.clock()-TimeStart
	lbl10.configure(text=TimeElapsed)
	window.after(30,StartStopRecord)

def Exit():
	sys.exit(0)


global x
x = 0 
global y
y = 5 
global xX
xX=[]
global yY
yY=[]
global yY2
yY2=[]
global y2 
y2 = 0 
rm = visa.ResourceManager()
window=Tk()
window.geometry('1250x1250')
window.title("PM320E")
lbl1= Label(window,font =("Arial Bold",15), text='Connected Devices')
lbl1.grid(column=0,row =0,sticky='w',columnspan=15)
Devices=rm.list_resources()
lbl2= Label(window,font =("Arial Bold",10))
lbl2.grid(column=0,row =1,columnspan=15,sticky='w')
lbl2.configure(text=Devices)

lbl3= Label(window,font =("Arial Bold",15))
lbl3.grid(column=0,row =2,columnspan=1,sticky='w')
lbl3.configure(text="Select Device")
#Radio Button For Selecting Device
v = Tkinter.IntVar()
Radio1=Tkinter.Radiobutton(window,text='USB0::0x1313::0x8022::M00263679::0::INSTR',padx=20,variable=v,value=0)
Radio1.grid(column=0,row=3,columnspan=15,sticky='w')
Radio2=Tkinter.Radiobutton(window,text='USB0::0x1313::0x8022::M00408735::0::INSTR',padx=20,variable=v,value=1)
Radio2.grid(column=0,row=4,columnspan=15,sticky='w')

btn4 = Tkinter.Button(master=window, text='Initialize', command=Initialize)
btn4.grid(column=0,row=5,sticky='w')
btn5 = Tkinter.Button(master=window, text='Refresh Device List', command=RefreshDevice)
btn5.grid(column=1,row=5,sticky='w')

#This is for input time
i=0
j=4
txtTime=Entry(window,width=5)
txtTime.grid(column=i+0,row=j+3,sticky='w')
lbl4= Label(window,font =("Arial Bold",15),text='Enter Recording Time in sec')
lbl4.grid(column=i+1,row=j+3,sticky='w')
#This is for Wavelength1
txtTimeWave1=Entry(window,width=5)
txtTimeWave1.grid(column=i+0,row=j+4,sticky='w')
btn1 = Tkinter.Button(master=window, text='Set Ch1 Wavelength', command=UpdateWave1)
btn1.grid(column=i+1,row=j+4,sticky='w')
#This is for Wavelength2
txtTimeWave2=Entry(window,width=5)
txtTimeWave2.grid(column=i+0,row=j+5,sticky='w')
btn2 = Tkinter.Button(master=window, text='Set Ch2 Wavelength', command=UpdateWave2)
btn2.grid(column=i+1,row=j+5,sticky='w')
#This is for FileName
txtFile=Entry(window,width=15)
txtFile.grid(column=i+0,row=j+6)
lbl5= Label(window,font =("Arial Bold",15),text='Enter a FileName')
lbl5.grid(column=i+1,row =j+6,sticky='w')

btn3 = Tkinter.Button(master=window, text='Record Data', command=RecordData)
btn3.grid(column=i+0,row=j+7)



#Live Plots
fig = plt.figure(figsize=(9, 4.5), dpi=100)
fig.subplots_adjust(hspace=.5)
ax1 = fig.add_subplot(2, 2, 1)
ax1.set_title("Channel 1")
ax2 = fig.add_subplot(2, 2, 3)
ax2.set_title("Channel 2")
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().grid(column=6,row=0,rowspan=40,columnspan=40,sticky="w")
canvas.draw()
ani = ani.FuncAnimation(fig, animate, interval=5)



lbl6= Label(window,font =("Arial Bold",30))
lbl6.grid(column=31,row =1,sticky='w')
lbl7= Label(window,font =("Arial Bold",30))
lbl7.grid(column=31,row =9,sticky='w')



lbl8= Label(window,font =("Arial Bold",15),text='Manual Start/Stop')
lbl8.grid(column=0,row=12,sticky='w')
btn3 = Tkinter.Button(master=window, text='Start/Stop', command=StartStopRecord)
btn3.grid(column=1,row=12)
lbl9= Label(window,font =("Arial Bold",15),text='Elapsed Time')
lbl9.grid(column=0,row=13,sticky='w')
lbl10= Label(window,font =("Arial Bold",15))
lbl10.grid(column=1,row=13,sticky='w')


btn10 = Tkinter.Button(master=window, text='Quit', command=Exit)
btn10.grid(column=i+0,row=14)
UpdateLiveValues()



window.mainloop()



