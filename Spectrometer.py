
import tkinter as Tkinter
from tkinter import *
import visa
import time
import csv
import os
import sys
sys.setrecursionlimit(10000)
#import Tkinter, Tkconstants, tkFileDialog
import seabreeze.spectrometers as sb
import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
import matplotlib.animation as ani
import matplotlib.pyplot as plt

global StartedProgram
global spec
StartedProgram=0
def FindSpec():
	global spec
	global StartedProgram
	try:
		if(Sel.get()==0):
			spec=sb.Spectrometer.from_serial_number("USB2G3525")
		elif(Sel.get()==1):
			spec=sb.Spectrometer.from_serial_number("S05418")
	except:
		print('No Device Connected')
	else:
		StartedProgram=1

def CSVWRITEREF():
	global spec
	if (StartedProgram==1):
		global REFw
		global REFi
		wavelength=[]
		intensity=[]
		j = 0
		filename =  txt.get()+".csv"
		csvfile= open(filename, 'w')
		wr=csv.writer(csvfile)
		wr.writerow(['WaveLength', 'Intensity'])
		fieldnames =['WaveLength', 'Intensity']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		#We capture the data here
		wavelength, intensity= GETDATA()
		intenSUB=[]
		if (v.get()==0):
			while (j < len(wavelength)):
				#Global variable is used here
				intenSUB=REFi[j]-intensity[j]
				writer.writerow({'WaveLength':wavelength[j], 'Intensity':intenSUB})
				j = j + 1
		elif(v.get()==1):
			while (j < len(wavelength)):
				#Global variable is used here
				intenSUB=intensity[j]-REFi[j]
				writer.writerow({'WaveLength':wavelength[j], 'Intensity':intenSUB})
				j = j + 1
		elif(v.get()==2):
			while (j < len(wavelength)):
			#Global variable is used here
				intenSUB=REFi[j]/intensity[j] 
				writer.writerow({'WaveLength':wavelength[j], 'Intensity':intenSUB})
				j = j + 1
		elif(v.get()==3):
			while (j < len(wavelength)):
				#Global variable is used here
				intenSUB=intensity[j]/REFi[j]
				writer.writerow({'WaveLength':wavelength[j], 'Intensity':intenSUB})
				j = j + 1
		elif(v.get()==4):
			while (j < len(wavelength)):
				#Global variable is used here
				intenSUB=intensity[j]
				writer.writerow({'WaveLength':wavelength[j], 'Intensity':intenSUB})
				j = j + 1
		elif(v.get()==5):
			while (j < len(wavelength)):
				#Global variable is used here
				intenSUB=REFi[j]
				writer.writerow({'WaveLength':wavelength[j], 'Intensity':intenSUB})
				j = j + 1
		csvfile.close()


def UPDATEDEVICELIST():
	device=str(sb.list_devices())
	lbl1.configure(text=str(device),bg="lightgrey")

def animate(i):
	global spec
	if (StartedProgram==1):
		global REFw
		global REFi
		if(y.get()==0):
			ax1.clear()
			ax1.plot(spec.wavelengths(),spec.intensities())		
		elif(y.get()==1 and SetREF==1):
			ax1.clear()
			ax1.plot(REFw,REFi)
		elif(y.get()==2 and SetREF==1):
			ax1.clear()
			dataI,dataW=Subs()
			ax1.plot(dataW,dataI)
	plt.title('Irradiance W/m^2 vs. Wavelength nm')

def Subs():
	global spec
	if (StartedProgram==1):
		global REFw
		global REFi
		j=0
		intenUSB= []
		wavelength, intensity= GETDATA()
		while (j < len(intensity)):
			#Global variable is used here
			intenUSB.append(intensity[j]-REFi[j])
			j = j + 1
		return intenUSB,wavelength	

def INTEGRATIONTIME():
	global spec
	if (StartedProgram==1):
		try:
			Times=int(Timing.get())
			spec.integration_time_micros(Times)
			#TimesCurrent=str(spec.pixels)
			lbl5.configure(text=Times)
		except:
			lbl5.configure(text="Error with Value")

def GETDATA():
	global spec
	if (StartedProgram==1):
		wave=[]
		intens=[] 
		wave=spec.wavelengths()
		intens=spec.intensities()
		return wave,intens



def ReferenceStore():
	global spec
	global SetREF
	if (StartedProgram==1):
		global REFw
		global REFi
		REFw=[]
		REFi=[] 
		REFw=spec.wavelengths()
		REFi=spec.intensities()
		SetREF=1

global SetREF
SetREF=0
global REFw
global REFi
REFw=[]
REFi=[] 



window=Tk()
#window.update()
#filename=tkFileDialog.askopenfilename()
window.geometry('970x500')
window.title("SEA BREEZE")
window.configure(background='gray18')
MasterFrame=Tkinter.Frame(window,bg="lightgrey",relief="sunken",bd='4')
MasterFrame.grid(column=13,row=13,sticky='w')
StartDevice=Tkinter.Frame(MasterFrame,bg="lightgrey",width=30)
StartDevice.grid(column=13,row=13,sticky='n')
#Device List
lbl1= Label(StartDevice,font =("Arial Bold",15)   )
lbl1.grid(column=0,row =2)
#btn1= Button(window, text="Update Device List",command=UPDATEDEVICELIST)
#btn1.grid(column=0,row=1)
i=10
j=10
#Entering the filename
WidgFrame=Tkinter.Frame(MasterFrame,bg="lightgrey",relief="raised",bd='4')
WidgFrame.grid(column=13,row=14,sticky='w')
lbl2= Label(WidgFrame,text="Enter FileName",font =("Arial Bold",15),bg="lightgrey"   )
lbl2.grid(column=i+3, row=j+1)
txt=Entry(WidgFrame,width=10)
txt.grid(column=i+4,row=j+1)
txt.focus()
btn2= Button(WidgFrame, text="Record Spectrum",command=CSVWRITEREF,width="20",bg='orchid1')
btn2.grid(column=i+5,row=j+1)


#Integration Time
btn4= Button(WidgFrame, text="Set Int Time in us",command=INTEGRATIONTIME,width="20",bg="aquamarine2")
btn4.grid(column=i+3,row=j+2)
Timing=Entry(WidgFrame,width=10)
Timing.grid(column=i+4,row=j+2)
lbl5= Label(WidgFrame,font =("Arial Bold",10) ,bg="lightgrey",width="25"  )
lbl5.grid(column=i+5, row =j+2)



#Reference Spectrum
btn5= Button(WidgFrame,command=ReferenceStore, text="Set Reference Spectrum",width="20",bg="orchid1")
btn5.grid(column=i+3,row=j+3)

#MatPlotlib Live Image First Spectrometer
fig = plt.figure(figsize=(5, 5), dpi=100,facecolor='#2e2e2e')
ax1 = fig.add_subplot(1, 1, 1)
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().grid(column=0,row=10,rowspan=10,columnspan=10,pady=0,sticky='s')
canvas.draw()
ani = ani.FuncAnimation(fig, animate, interval=1000)
plt.title('Irradiance W/m^2 vs. Wavelength nm')
ax1.tick_params(axis='both', which='major',colors='white')
ax1.set_title("Channel 1",color="white")
#MatPlotlib Live Image Flame NIR



#Radio button Selection for choosing operation
v = Tkinter.IntVar()
Radio0=Tkinter.Radiobutton(WidgFrame,text="Ref-Curr",padx=0,variable=v,value=0,bg="lightgrey")
Radio0.grid(column=i+3,row=j+4,sticky='nsw')
Radio1=Tkinter.Radiobutton(WidgFrame,text="Curr-Ref",padx=0,variable=v,value=1,bg="lightgrey")
Radio1.grid(column=i+3,row=j+5,sticky='nsw')
Radio2=Tkinter.Radiobutton(WidgFrame,text="Ref/Curr",padx=0,variable=v,value=2,bg="lightgrey")
Radio2.grid(column=i+4,row=j+4,sticky='nsw')
Radio3=Tkinter.Radiobutton(WidgFrame,text="Curr/Ref",padx=0,variable=v,value=3,bg="lightgrey")
Radio3.grid(column=i+4,row=j+5,sticky='nsw')
Radio4=Tkinter.Radiobutton(WidgFrame,text="Curr",padx=0,variable=v,value=4,bg="lightgrey")
Radio4.grid(column=i+3,row=j+6,sticky='nsw')
Radio5=Tkinter.Radiobutton(WidgFrame,text="Ref",padx=0,variable=v,value=5,bg="lightgrey")
Radio5.grid(column=i+4,row=j+6,sticky='nsw')

#Radio Button For Graph
lblgraph= Label(WidgFrame,font =("Arial Bold",15) ,bg="lightgrey",text="Choose Graph Display"  )
lblgraph.grid(column=i+3, row =j+7,columnspan="10")
y = Tkinter.IntVar()
Radio6=Tkinter.Radiobutton(WidgFrame,text="Current",padx=0,variable=y,value=0,bg="lightgrey")
Radio6.grid(column=i+3,row=j+8,sticky='nsw')
Radio7=Tkinter.Radiobutton(WidgFrame,text="Reference",padx=0,variable=y,value=1,bg="lightgrey")
Radio7.grid(column=i+4,row=j+8,sticky='nsw')
Radio8=Tkinter.Radiobutton(WidgFrame,text="Curr-Ref",padx=0,variable=y,value=2,bg="lightgrey")
Radio8.grid(column=i+5,row=j+8,sticky='e')

#Quit Button
btn3 = Tkinter.Button(master=StartDevice, text='Quit', command=sys.exit,width="20",bg="aquamarine2")
btn3.grid(column=0,row=6)
UPDATEDEVICELIST
btn7 = Tkinter.Button(master=StartDevice, command=UPDATEDEVICELIST,text="Refresh Device List",width="20",bg="aquamarine2")
btn7.grid(column=0,row=4)
btn6= Button(StartDevice,command=FindSpec, text="Press to Initialize device",width="20",bg="orchid1")
btn6.grid(column=0,row=5)

Select=Tkinter.Frame(StartDevice,bg="lightgrey",relief="groove",bd='4')
Select.grid(column=0,row=3,sticky='n')

Sel = Tkinter.IntVar()
RadioSel1=Tkinter.Radiobutton(Select,text="USB2000",padx=1,variable=Sel,value=0,bg="lightgrey")
RadioSel1.grid(column=0,row=0,sticky='n')
RadioSel2=Tkinter.Radiobutton(Select,text="STS-VIS",padx=2,variable=Sel,value=1,bg="lightgrey")
RadioSel2.grid(column=1,row=0,sticky='n')

UPDATEDEVICELIST()
os.system('cls')
window.mainloop()