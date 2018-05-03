from Tkinter import* 
import visa
import os
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
#Starts the whole shebang, without initializing nothing else starts because of StartedProgram bit

class MyClass(object):
    def __init__(self):
        self.p = Process(target=PrintCrap)
    def fun1(self):
        self.p.start()

    def fun2(self):
        self.p.terminate()


def Initialize():
	global StartedProgram
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
	global StartedProgram
	if (StartedProgram==1):
		Wave1=':WAVEL1:VAL ' + txtTimeWave1.get()
		my_instrument.write(Wave1)
#Updates wavelength for channel 2 read
def UpdateWave2():
	global StartedProgram
	if (StartedProgram==1):
		Wave1=':WAVEL2:VAL ' + txtTimeWave2.get()
		my_instrument.write(Wave2)
#Refresh scale if values are zero or huge
def RefreshScale():
	global StartedProgram
	if (StartedProgram==1):
		my_instrument.write(':PRANGE1 AUTO')
		my_instrument.write(':PRANGE2 AUTO')
#Device List at the top
def RefreshDevice():
	Devices=rm.list_resources()
	lbl2.configure(text=Devices)
'''
def CallRecord():
	#Just pass the filename
	p=Process(target=RecordData).start()
'''
def RecordData():
	global StartedProgram
	if (StartedProgram==1):
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
		#All of this needs to be put into a seperate Process
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
			writer.writerow({ 'CLOCK':str(Clk[i]), 'CHANNEL1':str(Pow1[i]), 'CHANNEL2':str(Pow2[i])})
			i = i + 1 
		csvfile.close()	

#Animation function for creating live graphs
def animate(i):
	global x
	Pow1=0
	Pow2=0
	global Y1array
	global Y2array
	global Xx
	global StartedProgram
	if (StartedProgram==1):
		Pow1=my_instrument.query(':POW1:VAL?')
		Pow2=my_instrument.query(':POW2:VAL?')
		x=time.clock()
		#Append to array
	  	xX.append(x)
		Y1array.append(Pow1) 
		Y2array.append(Pow2)
		#Plot new array
		ax1.plot(xX,Y1array)
		ax2.plot(xX,Y2array)
		#Move graph along with time
		ax2.set_xlim((x-2),(x+1))
		ax1.set_xlim((x-2),(x+1))

#Updates the current power reading
def UpdateLiveValues():
	global StartedProgram
	if (StartedProgram==1):
		Val1= str(time.clock()) + " W"
		yPrint1=round(y,3)
		yPrint2=round(y2,3)
		lbl6.configure(text=yPrint1)
		lbl7.configure(text=yPrint2)
		window.after(30,UpdateLiveValues)
#Trying to add, start ands stop, problem is program hang while in loop, need process ?
#Start CSV writing process inside of here?
def StartStopRecord(Variable):
	global StartedProgram
	WritingThread=threading.Thread(target=PrintCrap)
	i = 0 
	if (Variable==0):
		print("starting thread")
		lbl11.configure(text="WRT")
		WritingThread.start()

def ChangeText():
	lbl11.configure(text="STP")

def PrintCrap():
	i=0
	timeStart=time.time()
	while(i == 0):
		#Printing the number of active threads
		print(threading.active_count())
		timeElapsed=time.time()-timeStart
		timeElapsed=round(timeElapsed,3)
		lbl10.configure(text=timeElapsed)
		time.sleep(.5)
		if (lbl11["text"]=="STP"):
			print("EXITED THREAD")
			i = 1
			lbl10.configure(text="0")

'''
def PrintCrap():
	global ConditionLoop
	while(True):
		if (ConditionLoop==0):
			print("hello world")
			time.sleep(.5)
		elif(ConditionLoop==1):
			print("TRIED TO STOP THE MADNESS")
			time.sleep(.5)
			'''
def Exit():
	#Locking user from exiting if there are threads running
	if(lbl11["text"]=="STP"):
			#Should be one active thread
			print(threading.active_count())
			print("Closing")
			sys.exit(0)

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




rm = visa.ResourceManager()
window=Tk()
width=window.winfo_screenwidth()
height=window.winfo_screenheight()
width=width
height=height
tot=str(width)+"x"+str(height)
WidgFrame=Tkinter.Frame(window,bg='grey',relief="ridge",bd='4')
WidgFrame.grid(column=0,row=0,sticky='w')
window.geometry("900x500")
window.title("PM320E")
lbl1= Label(WidgFrame,font =("Arial Bold",15), text='Connected Devices',bg='grey')
lbl1.grid(column=0,row =0,sticky='w',columnspan=15)
Devices=rm.list_resources()
lbl2= Label(WidgFrame,font =("Arial Bold",10),bg='grey')
lbl2.grid(column=0,row =1,columnspan=15,sticky='w')
lbl2.configure(text=Devices)

lbl3= Label(WidgFrame,font =("Arial Bold",15),bg='grey')
lbl3.grid(column=0,row =2,columnspan=1,sticky='w')
lbl3.configure(text="Select Device")
#Radio Button For Selecting Device
v = Tkinter.IntVar()
Radio1=Tkinter.Radiobutton(WidgFrame,text='USB0::0x1313::0x8022::M00263679::0::INSTR',padx=20,variable=v,value=0,bg='grey')
Radio1.grid(column=0,row=3,columnspan=15,sticky='w')
Radio2=Tkinter.Radiobutton(WidgFrame,text='USB0::0x1313::0x8022::M00408735::0::INSTR',padx=20,variable=v,value=1,bg='grey')
Radio2.grid(column=0,row=4,columnspan=15,sticky='w')

btn4 = Tkinter.Button(master=WidgFrame, text='Initialize', command=Initialize,bg='grey')
btn4.grid(column=0,row=5,sticky='w')
btn5 = Tkinter.Button(master=WidgFrame, text='Refresh Device List', command=RefreshDevice,bg='grey')
btn5.grid(column=1,row=5,sticky='w')

#This is for aligning elements so that they stay spaced apart equally, can just change this to move them together
i=0
j=4

txtTime=Entry(WidgFrame,width=5)
txtTime.grid(column=i+0,row=j+3,sticky='w')
lbl4= Label(WidgFrame,font =("Arial Bold",15),text='Enter Recording Time in sec',bg='grey')
lbl4.grid(column=i+1,row=j+3,sticky='w')
#This is for Wavelength1
txtTimeWave1=Entry(WidgFrame,width=5)
txtTimeWave1.grid(column=i+0,row=j+4,sticky='w')
btn1 = Tkinter.Button(master=WidgFrame, text='Set Ch1 Wavelength', command=UpdateWave1,bg='grey')
btn1.grid(column=i+1,row=j+4,sticky='w')
#This is for Wavelength2
txtTimeWave2=Entry(WidgFrame,width=5)
txtTimeWave2.grid(column=i+0,row=j+5,sticky='w')
btn2 = Tkinter.Button(master=WidgFrame, text='Set Ch2 Wavelength', command=UpdateWave2,bg='grey')
btn2.grid(column=i+1,row=j+5,sticky='w')
#This is for FileName
txtFile=Entry(WidgFrame,width=15)
txtFile.grid(column=i+0,row=j+6)
lbl5= Label(WidgFrame,font =("Arial Bold",15),text='Enter a FileName',bg='grey')
lbl5.grid(column=i+1,row =j+6,sticky='w')
#Start Recording Data
btn3 = Tkinter.Button(master=WidgFrame, text='Record Data', command=RecordData,bg='grey')
btn3.grid(column=i+0,row=j+7)


#Graph Portion
GraphFrame=Tkinter.Frame(window,bg='grey',relief="ridge",bd='3',height="25")
GraphFrame.grid(column=1,row=0,sticky='w',rowspan="100")
#Live Plots
fig = plt.figure(figsize=(4.5, 4.5), dpi=100,facecolor="lightgrey")
fig.subplots_adjust(hspace=.5)
ax1 = fig.add_subplot(2,1,1)
ax1.set_title("Channel 1")
ax2 = fig.add_subplot(2,1,2)
ax2.set_title("Channel 2")
canvas = FigureCanvasTkAgg(fig, master=GraphFrame)
canvas.get_tk_widget().grid(column=6,row=0,rowspan=40,columnspan=10,sticky="w")
canvas.draw()
#Need to find way of speeding up graphing, blit ?
ani = ani.FuncAnimation(fig, animate, interval=2000)


#These get updated with value of PM320E channel reading
ValueFrame=Tkinter.Frame(window,bg='grey',relief="ridge",bd='3')
ValueFrame.grid(column=0,row=10,sticky='w',rowspan="100",columnspan="15")
#Channel1
lbl6Name= Label(ValueFrame,font =("Arial Bold",28),text="Ch1:",bg="grey")
lbl6Name.grid(column=0,row=0,sticky='w')
lbl6= Label(ValueFrame,font =("Arial Bold",28),bg="grey")
lbl6.grid(column=1,row=0,sticky='w',padx="160")
#Channel2
lbl7Name= Label(ValueFrame,font =("Arial Bold",28),text="Ch2:",bg="grey")
lbl7Name.grid(column=0,row=1,sticky='w')
lbl7= Label(ValueFrame,font =("Arial Bold",28),bg="grey")
lbl7.grid(column=1,row=1,sticky='w')


#Manual start stop portion
StartStopFrame=Tkinter.Frame(WidgFrame,bg='grey',relief="ridge",bd='3')
StartStopFrame.grid(column=0,row=12,sticky='w',rowspan="100",columnspan="15")
lbl8= Label(StartStopFrame,font =("Arial Bold",15),text='Manual Start/Stop',bg='grey')
lbl8.grid(column=0,row=12,sticky='w')
btn3 = Tkinter.Button(master=StartStopFrame, text='Start', command=lambda:StartStopRecord(0),bg='grey')
btn3.grid(column=1,row=12,padx='30')
btn4 = Tkinter.Button(master=StartStopFrame, text='Stop', command=ChangeText,bg='grey')
btn4.grid(column=3,row=12,padx="30")
lbl9= Label(StartStopFrame,font =("Arial Bold",15),text='Elapsed Time',bg='grey')
lbl9.grid(column=0,row=13,sticky='w')
lbl10= Label(StartStopFrame,font =("Arial Bold",15),bg='grey',width="15")
lbl10.grid(column=1,row=13,sticky='w')

lbl11= Label(StartStopFrame,font =("Arial Bold",15),bg='grey',width="5")
lbl11.grid(column=2,row=12,sticky='w')

#Here is the quit button
btn10 = Tkinter.Button(master=StartStopFrame, text='Quit', command=Exit,bg='grey')
btn10.grid(column=i+0,row=14)
window.configure(background="grey")
window.mainloop()




