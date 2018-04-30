from Tkinter import* 
import visa
import time
import csv
import Tkinter, Tkconstants, tkFileDialog
import seabreeze.spectrometers as sb
import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
import matplotlib.animation as ani
import matplotlib.pyplot as plt


#spec=sb.Spectrometer.from_serial_number("S05418")
def CSVWRITE():
	a = a + 1

def CSVWRITEREF():
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
			csvfile.close()
	elif(v.get()==4):
		while (j < len(wavelength)):
			#Global variable is used here
			intenSUB=intensity[j]
			writer.writerow({'WaveLength':wavelength[j], 'Intensity':intenSUB})
			j = j + 1
			csvfile.close()
	elif(v.get()==5):
		while (j < len(wavelength)):
			#Global variable is used here
			intenSUB=REFi[j]
			writer.writerow({'WaveLength':wavelength[j], 'Intensity':intenSUB})
			j = j + 1
			csvfile.close()


def UPDATEDEVICELIST():
	#devices=sb.list_devices()
	device=str(sb.list_devices())
	List.set(device) 
	lbl1.configure(text=device)

def animate(i):
	ax1.clear()
	ax1.plot(spec.wavelengths(),spec.intensities())

def INTEGRATIONTIME():
	Times=int(Timing.get())
	spec.integration_time_micros(Times)
	#TimesCurrent=str(spec.pixels)
	lbl5.configure(text=Times)

def GETDATA():
	wave=[]
	intens=[] 
	wave=spec.wavelengths()
	intens=spec.intensities()
	return wave,intens


def DataOutput():
	i =0
	while i<20:
		j = i - 1
		da1.set(i)
		da2.set(j)
		i = i + 1
		time.sleep(1)
		window.update()

def ReferenceStore():
	global REFw
	global REFi
	REFw=[]
	REFi=[] 
	REFw=spec.wavelengths()
	REFi=spec.intensities()



window=Tk()
List=StringVar()
#window.update()
#filename=tkFileDialog.askopenfilename()
window.geometry('1250x950')
window.title("SEA BREEZE")
window.configure(background='white')
#Device List
lbl1= Label(window,font =("Arial Bold",15)   )
lbl1.grid(column=0,row =2)
btn1= Button(window, text="Update Device List",command=UPDATEDEVICELIST,bg="red",fg="red")
btn1.grid(column=0,row=1)

#Entering the filename
lbl2= Label(window,text="Enter FileName",font =("Arial Bold",15)   )
lbl2.grid(column=5, row =1)
txt=Entry(window,width=10)
txt.grid(column=6,row=1)
txt.focus()
btn2= Button(window, text="Press Here to Record Spectrum",command=CSVWRITEREF,bg="orange",fg="red")
btn2.grid(column=7,row=1)


#Integration Time
btn4= Button(window, text="Click To Set Int Time",command=INTEGRATIONTIME,bg="orange",fg="red")
btn4.grid(column=5,row=2)
Timing=Entry(window,width=10)
Timing.grid(column=6,row=2)
lbl5= Label(window,font =("Arial Bold",15)   )
lbl5.grid(column=7, row =2)


#Reference Spectrum
btn5= Button(window,command=ReferenceStore, text="Press To Set Reference Spectrum",bg="orange",fg="red")
btn5.grid(column=5,row=3)

#MatPlotlib Live Image First Spectrometer
fig = plt.figure(figsize=(5, 5), dpi=100)
ax1 = fig.add_subplot(1, 1, 1)
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().grid(column=4,row=15)
canvas.show()
#ani = ani.FuncAnimation(fig, animate, interval=1000)

#MatPlotlib Live Image Flame NIR
fig = plt.figure(figsize=(5, 5), dpi=100)
ax1 = fig.add_subplot(1, 1, 1)
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().grid(column=5,row=15)
canvas.show()


#Radio button Selection for choosing operation
v = Tkinter.IntVar()
Radio0=Tkinter.Radiobutton(window,text="Ref-Curr",padx=0,variable=v,value=0)
Radio0.grid(column=5,row=4,sticky='nsew')
Radio1=Tkinter.Radiobutton(window,text="Curr-Ref",padx=0,variable=v,value=1)
Radio1.grid(column=5,row=5,sticky='nsew')
Radio2=Tkinter.Radiobutton(window,text="Ref/Curr",padx=0,variable=v,value=2)
Radio2.grid(column=6,row=4,sticky='nsew')
Radio3=Tkinter.Radiobutton(window,text="Curr/Ref",padx=0,variable=v,value=3)
Radio3.grid(column=6,row=5,sticky='nsew')
Radio4=Tkinter.Radiobutton(window,text="Curr",padx=0,variable=v,value=4)
Radio4.grid(column=5,row=6,sticky='nsew')
Radio5=Tkinter.Radiobutton(window,text="Ref",padx=0,variable=v,value=5)
Radio5.grid(column=6,row=6,sticky='nsew')

#Quit Button
btn3 = Tkinter.Button(master=window, text='Quit', command=sys.exit)
btn3.grid(column=7,row=6)


UPDATEDEVICELIST()
window.mainloop()