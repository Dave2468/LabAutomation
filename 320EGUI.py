import tkinter as Tkinter
from tkinter import*
from tkinter import messagebox 
import visa
import os
import time
import csv
import sys
sys.setrecursionlimit(10000)
import random
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
#Starts the whole shebang, without initializing nothing else starts because of StartedProgram bit
def Initialize():
	global StartedProgram
	global my_instrument
	try:
		if(v.get()==0):
			my_instrument = rm.open_resource('USB0::0x1313::0x8022::M00263679::0::INSTR')
		elif(v.get()==1):
			my_instrument = rm.open_resource('USB0::0x1313::0x8022::M00408735::0::INSTR')
	except:
		print("Device Does Not Match or Is Not Connected")
	else:
		my_instrument.write(':PRANGE1 AUTO')
		my_instrument.write(':PRANGE2 AUTO')
		StartedProgram=1
		UpdateLiveValues()
#Updates wavelength for channel 1 read
def UpdateWave1():
	global my_instrument
	global StartedProgram
	if (StartedProgram==1):
		Wave1=':WAVEL1:VAL ' + txtTimeWave1.get()
		my_instrument.write(Wave1)
#Updates wavelength for channel 2 read
def UpdateWave2():
	global my_instrument
	global StartedProgram
	if (StartedProgram==1):
		Wave2=':WAVEL2:VAL ' + txtTimeWave2.get()
		my_instrument.write(Wave2)
#Refresh scale if values are zero or huge
def RefreshScale():
	global my_instrument
	global StartedProgram
	if (StartedProgram==1):
		my_instrument.write(':PRANGE1 AUTO')
		my_instrument.write(':PRANGE2 AUTO')
#Device List at the top
def RefreshDevice():
	Devices=rm.list_resources()
	lbl2.configure(text=Devices)

def CallRecord():
	#Just pass the filename
	global StartedProgram
	if (StartedProgram==1 and lbl11["text"]=="STP"):
		lbl11.configure(text="WRT")
		p=threading.Thread(target=RecordData).start()
def RecordData():
	global my_instrument
	global StartedProgram
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
	while (time.time() < StopTime):
		power1=float(my_instrument.query(':POW1:VAL?'))
		power2=float(my_instrument.query(':POW2:VAL?'))
		lbl6.configure(text=str(power1)+" W")
		lbl7.configure(text=str(power2)+" W")
		#Writing Values out to CSV file
		writer.writerow({ 'CLOCK':str(time.time()), 'CHANNEL1':power1, 'CHANNEL2':power2})
	csvfile.close()	
	lbl11.configure(text="STP")

#Animation function for creating live graphs
def animate(i):
	global my_instrument
	global x
	Pow1=0
	Pow2=0
	global Y1array
	global Y2array
	global Xx
	global StartedProgram
	if (StartedProgram==1 and lbl11["text"]=="STP"):
		Pow1=float(my_instrument.query(':POW1:VAL?'))
		Pow2=float(my_instrument.query(':POW2:VAL?'))
		x=time.clock()
		Xx.append(x)
		Y1array.append(Pow1)
		Y2array.append(Pow2)
		#Plot new array
		ax1.plot(Xx,Y1array)
		ax2.plot(Xx,Y2array)
		#Move graph along with time
		ax2.set_xlim((x-2),(x+1))
		ax1.set_xlim((x-2),(x+1))
		ax2.autoscale(True,'y',True)
		ax1.autoscale(True,'y',True)


#Updates the current power reading
def UpdateLiveValues():
	global my_instrument
	global StartedProgram
	if (StartedProgram==1 and lbl11["text"]=="STP"):
		power1=float(my_instrument.query(':POW1:VAL?'))
		power2=float(my_instrument.query(':POW2:VAL?'))
		lbl6.configure(text=str(power1)+" W")
		lbl7.configure(text=str(power2)+" W")
	window.after(30,UpdateLiveValues)


def ChangeText():
	lbl11.configure(text="STP")

def StartStopRecord(Variable):
	global StartedProgram
	if (StartedProgram==1 and lbl11["text"]=="STP"):
		WritingThread=threading.Thread(target=WriteStartStop)
		i = 0 
		if (Variable==0 and lbl11["text"]=="STP"):
			lbl11.configure(text="WRT")
			WritingThread.start()

def WriteStartStop():
	global my_instrument
	i=0
	timeStart=time.time()
	fn=txtFile.get()
	#Creating a csv file to be written to
	filename=fn+".csv"
	csvfile= open(filename, 'w')
	wr=csv.writer(csvfile)
	wr.writerow(['ELAPSED','CHANNEL1','CHANNEL2'])
	fieldnames =['ELAPSED','CHANNEL1','CHANNEL2']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	#Initializing variables I will be using
	while(i == 0):
		#Printing the number of active threads
		timeElapsed=time.time()-timeStart
		timeElapsed=round(timeElapsed,3)
		lbl10.configure(text=str(timeElapsed)+" s")
		power1=float(my_instrument.query(':POW1:VAL?'))
		power2=float(my_instrument.query(':POW2:VAL?'))
		lbl6.configure(text=str(power1)+" W")
		lbl7.configure(text=str(power2)+" W")
		writer.writerow({'ELAPSED':str(timeElapsed), 'CHANNEL1':power1, 'CHANNEL2':power2 })
		time.sleep(.5)
		if (lbl11["text"]=="STP"):
			i = 1
			lbl10.configure(text="0")
			csvfile.close()	


def Exit():
	#Locking user from exiting if there are threads running
	if(lbl11["text"]=="STP"):
			#Should be one active thread
			print("Closing")
			sys.exit(0)
	elif(lbl11["text"]=="WRT"):
		messagebox.showwarning("Warning","Cannot Quit While Writing to Files")

#Globals for animation 
global ani
global x
x = 0 
global Y1array
Y1array=[]
global Y2array
Y2array=[]
global StartedProgram
StartedProgram=0
global Xx
Xx=[]


rm = visa.ResourceManager()
window=Tk()
width=window.winfo_screenwidth()
height=window.winfo_screenheight()
width=width
height=height
tot=str(width)+"x"+str(height)
WidgFrame=Tkinter.Frame(window,bg="gray18",relief="ridge",bd='4')
WidgFrame.grid(column=0,row=0,sticky='w',rowspan="50")
window.geometry("1100x700")
window.title("PM320E")
lbl1= Label(WidgFrame,font =("Arial Bold",15), text='Connected Devices',bg="gray18",fg="azure")
lbl1.grid(column=0,row =0,sticky='w',columnspan=15)
Devices=rm.list_resources()
lbl2= Label(WidgFrame,font =("Arial Bold",10),bg="gray18",fg="azure")
lbl2.grid(column=0,row =1,columnspan=15,sticky='w')
lbl2.configure(text=Devices)

lbl3= Label(WidgFrame,font =("Arial Bold",15),bg="gray18",fg="azure")
lbl3.grid(column=0,row =2,columnspan=1,sticky='w')
lbl3.configure(text="Select Device")
#Radio Button For Selecting Device
v = Tkinter.IntVar()
Radio1=Tkinter.Radiobutton(WidgFrame,text='USB0::0x1313::0x8022::M00263679::0::INSTR',padx=20,variable=v,value=0,bg="gray18",fg="azure",selectcolor="blue")
Radio1.grid(column=0,row=3,columnspan=15,sticky='w')
Radio2=Tkinter.Radiobutton(WidgFrame,text='USB0::0x1313::0x8022::M00408735::0::INSTR',padx=20,variable=v,value=1,bg="gray18",fg="azure",selectcolor="blue")
Radio2.grid(column=0,row=4,columnspan=15,sticky='w')

btn4 = Tkinter.Button(master=WidgFrame, text='Initialize', command=Initialize,bg='skyblue',width=15)
btn4.grid(column=0,row=5,sticky='w')
btn5 = Tkinter.Button(master=WidgFrame, text='Refresh Device List', command=RefreshDevice,bg='lightgoldenrod',width=15)
btn5.grid(column=1,row=5,sticky='w')

#This is for aligning elements so that they stay spaced apart equally, can just change this to move them together
i=0
j=4

txtTime=Entry(WidgFrame,width=5)
txtTime.grid(column=i+0,row=j+3,sticky='w')
lbl4= Label(WidgFrame,font =("Arial Bold",15),text='Enter Recording Time in sec',bg="gray18",fg="azure")
lbl4.grid(column=i+1,row=j+3,sticky='w')
#This is for Wavelength1
txtTimeWave1=Entry(WidgFrame,width=5)
txtTimeWave1.grid(column=i+0,row=j+4,sticky='w')
btn1 = Tkinter.Button(master=WidgFrame, text='Set Ch1 Wavelength', command=UpdateWave1,bg='lightgoldenrod',width=20)
btn1.grid(column=i+1,row=j+4,sticky='w')
#This is for Wavelength2
txtTimeWave2=Entry(WidgFrame,width=5)
txtTimeWave2.grid(column=i+0,row=j+5,sticky='w')
btn2 = Tkinter.Button(master=WidgFrame, text='Set Ch2 Wavelength', command=UpdateWave2,bg='lightgoldenrod',width=20)
btn2.grid(column=i+1,row=j+5,sticky='w')
#This is for FileName
txtFile=Entry(WidgFrame,width=15)
txtFile.grid(column=i+0,row=j+6,sticky='w')
lbl5= Label(WidgFrame,font =("Arial Bold",15),text='Enter a FileName',bg="gray18",fg="azure")
lbl5.grid(column=i+1,row =j+6,sticky='w')
#Start Recording Data
btn3 = Tkinter.Button(master=WidgFrame, text='Record Data', command=CallRecord,bg='skyblue',width=10)
btn3.grid(column=i+0,row=j+7,sticky='w')


#Live Plots

fig = plt.figure(figsize=(4.5, 7), dpi=100,facecolor="#2e2e2e")
fig.set_figwidth(5)
fig.subplots_adjust(hspace=.5)
ax1 = fig.add_subplot(2,1,1)
ax1.set_title("Channel 1",color="white")
ax2 = fig.add_subplot(2,1,2)
ax2.set_title("Channel 2",color="white")
canvas = FigureCanvasTkAgg(fig, master=WidgFrame)
canvas.get_tk_widget().grid(column=25,row=0,rowspan=40,columnspan=10,sticky="w")
canvas.draw()
#Need to find way of speeding up graphing, blit ?
ani = ani.FuncAnimation(fig, animate, interval=1000)
ax1.tick_params(axis='both', which='major', labelsize=5,colors='white')
ax2.tick_params(axis='both', which='major', labelsize=5,colors='white')





#Manual start stop portion
StartStopFrame=Tkinter.Frame(WidgFrame,bg="gray18",relief="ridge",bd='3')
StartStopFrame.grid(column=0,row=12,sticky='w',rowspan="100",columnspan="15",pady="5")
lbl8= Label(StartStopFrame,font =("Arial Bold",15),text='Manual Start/Stop',bg="gray18",fg="azure")
lbl8.grid(column=0,row=12,sticky='w')
btn3 = Tkinter.Button(master=StartStopFrame, text='Start', command=lambda:StartStopRecord(0),bg='skyblue',width=5)
btn3.grid(column=1,row=12,padx='30',sticky='e')
btn4 = Tkinter.Button(master=StartStopFrame, text='Stop', command=ChangeText,bg='lightgoldenrod',width=5)
btn4.grid(column=3,row=12,padx="30",sticky='w')
lbl9= Label(StartStopFrame,font =("Arial Bold",15),text='Elapsed Time',bg="gray18",fg="azure")
lbl9.grid(column=0,row=13,sticky='w')
lbl10= Label(StartStopFrame,font =("Arial Bold",15),bg="gray18",width="15",fg="azure")
lbl10.grid(column=1,row=13,sticky='w')

lbl11= Label(StartStopFrame,font =("Arial Bold",15),bg="gray18",width="5",fg="azure")
lbl11.grid(column=2,row=12,sticky='w')
ChangeText()
#Here is the quit button

ReadingFrame=Tkinter.Frame(StartStopFrame,bg="gray18",relief="ridge",bd='3')
ReadingFrame.grid(column=0,row=14,sticky='w',rowspan="100",columnspan="15")
lbl6Name= Label(ReadingFrame,font =("Arial Bold",15),text="Ch1:",bg="gray18",fg="azure")
lbl6Name.grid(column=0,row=36,sticky='w')
lbl6= Label(ReadingFrame,font =("Arial Bold",15),bg="gray18",width="28",height="2",fg="firebrick1")
lbl6.grid(column=1,row=36,sticky='w',padx="70")
lbl6.configure(text="0 W")
#Channel2
lbl7Name= Label(ReadingFrame,font =("Arial Bold",15),text="Ch2:",bg="gray18",fg="azure")
lbl7Name.grid(column=0,row=37,sticky='w')
lbl7= Label(ReadingFrame,font =("Arial Bold",15),bg="gray18",width="28",height="2",fg="firebrick1")
lbl7.grid(column=1,row=37,sticky='w',padx="70")
lbl7.configure(text="0 W")
btn10 = Tkinter.Button(master=ReadingFrame, text='Quit', command=Exit,bg='red')
btn10.grid(column=i+0,row=38,pady=30)



window.configure(background="gray18")
os.system('cls')
window.mainloop()




