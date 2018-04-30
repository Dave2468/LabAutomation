import tkinter as tk
from multiprocessing import Process, Value, Manager
import time
import visa
from time import localtime, strftime
import csv
import ctypes
from ctypes import c_char_p
from random import *
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.axes
import matplotlib as mpl
import sys
import serial
import binascii
import os
import numpy as np
plt.ion()

#Graphical Interface for viewing power
def viewer1(R1,pwmv,dv,pt,it,dt):
	def counter_label():
		def count():
			var2.set(str(R1.value))
			root.update_idletasks()
			root.after(500,count)
		count()
		def count1():
			var1.set(str(pwmv.value))
			root.update_idletasks()
			root.after(10,count1)
		count1()
		def count2():
			var.set(str(dv.value))
			root.update_idletasks()
			root.after(10,count2)
		count2()
		def count3():
			error= (((dv.value-R1.value)/dv.value)*100)
			var3.set(str(error)+"%")
			root.update_idletasks()
			root.after(10,count3)
		count3()
		def count4():
			var4.set(str(pt.value))
			root.update_idletasks()
			root.after(10,count4)
		count4()
		def count5():
			var5.set(str(it.value))
			root.update_idletasks()
			root.after(10,count5)
		count5()
		def count6():
			var6.set(str(dt.value))
			root.update_idletasks()
			root.after(10,count6)
		count6()
	try:
		i=0
		width=700
		height=600
		root = tk.Tk()
		var=tk.StringVar()
		var1=tk.StringVar()
		var2=tk.StringVar()
		var3=tk.StringVar()
		var4=tk.StringVar()
		var5=tk.StringVar()
		var6=tk.StringVar()
		screen_width = root.winfo_screenwidth()
		screen_height = root.winfo_screenheight()
		y = 0
		x = (screen_width - width)
		root.geometry('%dx%d+%d+%d' % (width, height, x, y))
		root.title("Power Meter Readings")
		labelhead = tk.Label(root, text="POWER READING",width=25,
							borderwidth=2, relief="ridge",font=("", 16) )
		labelhead.pack()
		label1 = tk.Label(root, textvariable = var2 ,fg="red", height=2,width=25,
								 anchor="n",font=("", 16))
		label1.pack()
		label4 = tk.Label(root, text="DESIRED READING",width=25,
							borderwidth=2, relief="ridge",font=("", 16) )
		label4.pack()
		label5 = tk.Label(root,  textvariable = var ,fg="red", height=2,width=25,
								 anchor="n",font=("", 16))
		label5.pack()
		label3 = tk.Label(root, text="Current PWM",width=25,
							borderwidth=2, relief="ridge",font=("", 16) )
		label3.pack()
		label2 = tk.Label(root,  textvariable = var1,fg="red", height=2,width=25,
								 anchor="n",font=("", 16))
		label2.pack()
		label7 = tk.Label(root, text="Error Percentage",width=25,
							borderwidth=2, relief="ridge",font=("", 16) )
		label7.pack()
		label6 = tk.Label(root,  textvariable = var3,fg="red", height=2,width=25,
								 anchor="n",font=("", 16))
		label6.pack()
		label8 = tk.Label(root, text="Pterm",width=25,
							borderwidth=2, relief="ridge",font=("", 16) )
		label8.pack()
		label9 = tk.Label(root,  textvariable = var4,fg="red", height=2,width=25,
								 anchor="n",font=("", 16))
		label9.pack()
		label10 = tk.Label(root, text="Iterm",width=25,
							borderwidth=2, relief="ridge",font=("", 16) )
		label10.pack()
		label11 = tk.Label(root,  textvariable = var5,fg="red", height=2,width=25,
								 anchor="n",font=("", 16))
		label11.pack()
		label12 = tk.Label(root, text="Dterm",width=25,
							borderwidth=2, relief="ridge",font=("", 16) )
		label12.pack()
		label13 = tk.Label(root,  textvariable = var6,fg="red", height=2,width=25,
								 anchor="n",font=("", 16))
		label13.pack()
		counter_label()
		root.mainloop()
	except KeyboardInterrupt:
		root.quit()
		root.destroy()
		return
	except:
		root.quit()
		root.destroy()
		print("Something wrong with GUI")
		return
#Calculating units for plotting
def unitcal(yvalue):
	y=float(yvalue)
	if y<0:
		y=abs(y)
	f1='%e'%y
	f=str(f1)
	test=int(y)
	if test==0 and float(f1)<1 and y!=0:
		a=f.split("-")
		exp=int(a[1])
		unit1=1/(10**exp)
	else:
		a=f.split("+")
		exp=int(a[1])
		unit1=10**exp
		if unit1>=1:
			unit1=1
	return unit1
#Function for plotting onto the GUI
def plots1(R1,runtime,dv):
	try:
		mpl.rcParams['toolbar'] = 'None'
		width=700
		height=200
		m=0
		xdata = []
		ydata = []
		figure, ax = plt.subplots(figsize=(width/100,height/100))
		lines, = ax.plot([],[], 'b-')
		user32 = ctypes.windll.user32
		screen_width = user32.GetSystemMetrics(0)
		screen_height= user32.GetSystemMetrics(1)
		x = (screen_width - width)
		y = 610
		xmin=runtime.value
		xmax=(runtime.value)+10
		ax.set_xlim(xmin, xmax)
		j=R1.value
		unitv=unitcal(j)
		ax.set_ylim(j-((unitv)*1), j+((unitv)*1))
		figure.canvas.set_window_title('Plot')
		figure.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
		while True:
			x=runtime.value
			y=R1.value
			unitv=unitcal(y)
			ymin, ymax = ax.get_ylim()
			xmin,xmax=ax.get_xlim()
			if (xmin>x or xmax<x):
				xmin=x
				xmax=x+10
			if (ymin>y or ymax<y):
				ymin=y-((unitv)*1)
				ymax=y+((unitv)*1)
			ax.set_ylim(ymin,ymax)
			ax.set_xlim(xmin, xmax)
			xdata.append(x)
			ydata.append(y)
			lines.set_xdata(xdata)
			lines.set_ydata(ydata)
			ax.axhline(y=dv.value, xmin=0, xmax=1,linewidth=0.5)
			figure.canvas.show()
			figure.canvas.flush_events()
			time.sleep(0.03)
	except KeyboardInterrupt:
		plt.close('all')
		return
	except:
		plt.close('all')
		print("Something Wrong with plot")
		return

#Function that sets up for PM100D for reading.
#Also this function houses the functions responsible for the feedback loops.
def readerandfeed(portno,R1,runtime,fixedPWM,varPWM,vn,fn,dv,pt,it,dt):
	if not os.path.exists("data"):
		os.makedirs("data")
	time1=strftime(" @%H %M %S.csv")
	filename="data/"+fn.value+time1
	csvfile= open(filename, 'w', newline='')
	wr=csv.writer(csvfile)
	wr.writerow(['S.NO','RUN TIME','READING','PWM','DESIRED READING','Pterm','Iterm','Dterm','ErrorP','ErrorI','ErrorD'])
	fieldnames =['S.NO','RUN TIME','READING','PWM','DESIRED READING','Pterm','Iterm','Dterm','ErrorP','ErrorI','ErrorD']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	rm = visa.ResourceManager()
	a=rm.list_resources()
	vname=a[(vn.value-1)]
	pm100d=rm.get_instrument(vname)
	pm100d.write("INITitate")
	pm100d.write("CONFigure")
	pm100d.write("MEASure")
	pm100d.write("SENSe:AVERage:COUNt 100")


	kP=2.5445
	kI=4.5
	kD=0


	#Setting up the PM100D
	ser = serial.Serial(
					port=portno,
					baudrate=9600,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					bytesize=serial.EIGHTBITS,
					timeout=1)

	ser.reset_input_buffer()
	ser.reset_output_buffer()
	k=1
	s_no=0
	remainingt=0
	PowerReadp=0
	try:
		initialPWM=fixedPWM.value
		while True:
			cmd1= '7F'
			cmd2 = str(initialPWM)
			initial = '5b'
			pwm=calpwm(cmd2)
			pwmchecksum1=pwmchecksum(cmd1,pwm)
			command=initial+' '+cmd1+' '+pwm+' '+pwmchecksum1
			hex_data1=bytearray.fromhex(command)
			ser.write(hex_data1)
			ser.flush()
			out = ser.read()
			x=binascii.hexlify(out)
			hex1=str(x,'ascii')
			if hex1=='aa':
				varPWM.value=initialPWM
				break
			elif hex1=='3f':
				pass
			else:
				print("Critical Error")
		while True:
			cmd1='75'
			initial='5B'
			checksum=complement(cmd1)
			command=initial+' '+cmd1+' '+checksum
			hex_data2=bytearray.fromhex(command)
			ser.write(hex_data2)
			ser.flush()
			out = ser.read()
			x=binascii.hexlify(out)
			hex1=str(x,'ascii')
			if hex1=='aa':
				starttime=time.clock()
				break
			elif hex1=='3f':
				pass
			else:
				print("Critical Error")
		time.sleep(3)
		#Initializing variables for the PID
		previouspwm=0
		Error=0
		Error2=0
		Error3=0
		pterm=0
		iterm=0
		dterm=0
		reading=0
		pwmnew=0
		iteration=0
		timenow=time.clock()
		while True:
			PowerRead=abs(float((pm100d.query("READ?"))))
			fixedPWMval=fixedPWM.value
			Setpoint=dv.value
			timeprevious=timenow
			timenow=time.clock()
			readingprevious=reading
			reading=PowerRead
			ErrorPrev=Error
			Error=Setpoint-reading
			pterm=kP*Error
			Error2=Error2+(Error*(timenow-timeprevious))
			iterm=kI*Error2
			Error3=(Error-ErrorPrev)/(timenow-timeprevious)
			dterm=kD*Error3

			pt.value=pterm
			it.value=iterm
			dt.value=dterm

			PIDterm=pterm+iterm+dterm

			PWMvalue=float(fixedPWMval)+float(PIDterm)
			#Constraints for the system to not increase PWM by more than 50%
			if(PWMvalue>50):
				PWMvalue=50
			elif(PWMvalue<0):
				PWMvalue=0
			#This code here calculates decimal points in the 10th place
			previouspwm=pwmnew
			temppwm=float("{0:.1f}".format(PWMvalue))
			tenthdigit=str(temppwm)[len(str(temppwm))-1]
			pwmnew=round((float(temppwm)*2))/2
			#These roundings are for rounding off what the new power is as we can only
			#set the power in increments of 0.5
			#Values 0.0->0.2 are rounded down to 0
			#Values 0.3 and 0.4 round to 0.5
			#Value 0.5 and 0.6 round to 0.5
			#Values 0.7,0.8,0.9 round to 1
			if (tenthdigit=='7' or tenthdigit=='3'):
				pwmnew=pwmnew+0.5	


			varPWM.value=pwmnew


			ser.reset_input_buffer()
			ser.reset_output_buffer()
			#If the previousPWM is the same as the new one no serial data is sent, this is because when the
			#power is stable, flooding the bus with the same value over and over again reduces performance.
			if previouspwm!=pwmnew:
				while True:
					cmd1= '7F'
					cmd2 = str(pwmnew)
					initial = '5b'
					pwm=calpwm(cmd2)
					pwmchecksum1=pwmchecksum(cmd1,pwm)
					command=initial+' '+cmd1+' '+pwm+' '+pwmchecksum1
					hex_data1=bytearray.fromhex(command)
					ser.write(hex_data1)
					ser.flush()
					out = ser.read()
					x=binascii.hexlify(out)
					hex1=str(x,'ascii')
					if hex1=='aa':
						break
					elif hex1=='3f':
						pass
					else:
						print("Critical Error")
			
			s_no=s_no+1
			rt=time.clock()-starttime
			runtime.value=rt
			writer.writerow({'S.NO':s_no, 'RUN TIME':rt,'READING':PowerRead,'PWM':pwmnew,'DESIRED READING':dv.value,'Pterm':pt.value,'Iterm':it.value,
				'Dterm':dt.value,'ErrorP':Error,'ErrorI': Error2,'ErrorD':Error3})
			R1.value=PowerRead

	except KeyboardInterrupt:
		csvfile.close()
		pm100d.write("ABORt")
		pm100d.close()
		while True:
			cmd1= '7F'
			cmd2 = str(1)
			initial = '5b'
			pwm=calpwm(cmd2)
			pwmchecksum1=pwmchecksum(cmd1,pwm)
			command=initial+' '+cmd1+' '+pwm+' '+pwmchecksum1
			hex_data1=bytearray.fromhex(command)
			ser.write(hex_data1)
			ser.flush()
			out = ser.read()
			x=binascii.hexlify(out)
			hex1=str(x,'ascii')
			if hex1=='aa':
				break
			elif hex1=='3f':
				pass
			else:
				print("Critical Error")
		while True:
			cmd1='76'
			initial='5B'
			checksum=complement(cmd1)
			command=initial+' '+cmd1+' '+checksum
			hex_data2=bytearray.fromhex(command)
			ser.write(hex_data2)
			ser.flush()
			out = ser.read()
			x=binascii.hexlify(out)
			hex1=str(x,'ascii')
			if hex1=='aa':
				break
			elif hex1=='3f':
				pass
			else:
				print("Critical Error")
		return
	except:
		csvfile.close()
		pm100d.write("ABORt")
		pm100d.close()
		while True:
			cmd1= '7F'
			cmd2 = str(1)
			initial = '5b'
			pwm=calpwm(cmd2)
			pwmchecksum1=pwmchecksum(cmd1,pwm)
			command=initial+' '+cmd1+' '+pwm+' '+pwmchecksum1
			hex_data1=bytearray.fromhex(command)
			ser.write(hex_data1)
			ser.flush()
			out = ser.read()
			x=binascii.hexlify(out)
			hex1=str(x,'ascii')
			if hex1=='aa':
				break
			elif hex1=='3f':
				pass
			else:
				print("Critical Error")
		while True:
			cmd1='76'
			initial='5B'
			checksum=complement(cmd1)
			command=initial+' '+cmd1+' '+checksum
			hex_data2=bytearray.fromhex(command)
			ser.write(hex_data2)
			ser.flush()
			out = ser.read()
			x=binascii.hexlify(out)
			hex1=str(x,'ascii')
			if hex1=='aa':
				break
			elif hex1=='3f':
				pass
			else:
				print("Critical Error")
		print("Error in Feedback")
		return


#Function for listing the available serial ports
def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
#Function for finding the complement of an input for sending values to UC2000
def complement(input1):
	my_hexdata = input1
	scale = 16
	num_of_bits = 8
	cbin=[]
	binary=bin(int(my_hexdata, scale))[2:].zfill(num_of_bits)
	cbin = ""
	for bit in binary:
		if bit == "1":
			cbin+="0"
		else:
			cbin+="1"
	intbin=(int(cbin, 2))
	checksum=hex(intbin).rstrip("L").lstrip("0x") or "0"
	return checksum
#Function to find code to send certain PWM to UC2000.
def calpwm(input11):
	input1=float(input11)
	my_hexdata1 = int(input1*2)
	value=hex(my_hexdata1).rstrip("L").lstrip("0x") or "0"
	if len(value)==1:
		value1='0'+value
		return value1
	elif len(value)==2:
		return value
#Function for finding last byte 'checksum' for sending to UC2000
def pwmchecksum(input1,input2):
	my_hexdata1 = input1
	my_hexdata2 = input2
	mhh1=int(my_hexdata1,16)
	mhh2=int(my_hexdata2,16)
	mhh=mhh1+mhh2
	my_hexdata=hex(mhh).rstrip("L").lstrip("0x") or "0"
	scale = 16
	num_of_bits = 8
	cbin=[]
	binary=bin(int(my_hexdata, scale))[2:].zfill(num_of_bits)
	cbin = ""
	for bit in binary:
		if bit == "1":
			cbin += "0"
		else:
			cbin += "1"
	intbin=(int(cbin, 2))
	checksum=hex(intbin).rstrip("L").lstrip("0x") or "0"
	if len(checksum)==1:
		checksum1='0'+checksum
		return checksum1
	elif len(checksum)==2:
		return checksum



def main():
	#Values, functions, and multiprocessing is initialized here.
	rm = visa.ResourceManager()
	a=rm.list_resources()
	filename=input("Enter filename: ")
	manager = Manager()
	fn = manager.Value(c_char_p, str(filename))
	print("Available PowerMeters:")
	i=0
	while i<len(a):
		print((i+1),".",a[i])
		i=i+1
	visaname = input("\nEnter your choice:")
	vname=Value('i', int(visaname))
	reading1 = Value('d',0.0000000)
	rtv = Value('d',0.0000000) #runtime
	fixedPWM = Value('d',0.0) 
	varPWM = Value('d',0.0)
	pt=Value('d',0)
	it=Value('d',0)
	dt=Value('d',0)
	dv=Value('d',0.0000000)
	dv1=Value('d',0.0000000)
	pviewer=Process(target=viewer1, args=(reading1,varPWM,dv,pt,it,dt, ))
	pplot=Process(target=plots1, args=(reading1,rtv,dv1, ))
	print("Configuring ")
	print("Available Ports")
	print(serial_ports())
	pn = input("\nEnter Port number: ")
	portno='COM'+pn
	readerfeed=Process(target=readerandfeed, args=(portno,reading1,rtv,fixedPWM,varPWM ,vname,fn,dv,pt,it,dt, ))
	DesiredOutputPower= input("Enter your desired power reading: ")
	try:
		#The user enters a desired power and the expression below finds the equivalent PWM.
		#This expression was obtained through a regression model between output power and PWM.
		pwmtemp=3.539324+(2.882411*float(DesiredOutputPower))
		pwm1=round((float(pwmtemp)*2))/2
		dv1.value=float(DesiredOutputPower)
		dv.value=float(DesiredOutputPower)
		previousdesired=float(DesiredOutputPower)
		start = input("Would you liked to being lasing, Y or N: ")
		if((start=='y') or (start=='Y')):
			user32 = ctypes.WinDLL('user32', use_last_error=True)
			user32.LockSetForegroundWindow(1)
			fixedPWM.value=pwm1
			pviewer.start()
			readerfeed.start()
			pplot.start()
		while True:
			DesiredOutputPower= input("Enter your desired power reading: ")
			dv1.value=float(DesiredOutputPower)
			diffinoutput=(float(DesiredOutputPower)-previousdesired)
			control=0
			newpower=previousdesired
			while (control<abs(diffinoutput)):
				if diffinoutput<0:
					newpower=newpower-0.1
				else:
					newpower=newpower+0.1
				pwmtemp=3.539324+(2.882411*float(newpower))
				pwm1=round((float(pwmtemp)*2))/2
				time.sleep(0.5)
				fixedPWM.value=pwm1
				dv.value=float(newpower)
				control=control+0.1
			previousdesired=float(DesiredOutputPower)

	except KeyboardInterrupt:
		while True:
			if (not(pviewer.is_alive() and pplot.is_alive())):
				pviewer.terminate()
				pplot.terminate()
				pviewer.join()
				pplot.join()
				break
		while True:
			if(readerfeed.is_alive()):
				pass
			elif not(readerfeed.is_alive()):
				readerfeed.terminate()
				readerfeed.join()
				break
			else:
				pass
		print("\nEverything closed successfully")
		return


	except :
		while True:
			if (not(pviewer.is_alive() and pplot.is_alive())):
				pviewer.terminate()
				pplot.terminate()
				pviewer.join()
				pplot.join()
				break
		while True:
			if(readerfeed.is_alive()):
				pass
			elif not(readerfeed.is_alive()):
				readerfeed.terminate()
				readerfeed.join()
				break
			else:
				pass
		print("\nSome Problem")
		return

if __name__ == "__main__":
	os.system('cls')
	main()








