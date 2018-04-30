from ctypes import c_long, c_buffer, c_float, windll, pointer
import os
from multiprocessing import Process, Value
from threading import Thread
import math

dllname='APT.dll'
aptdll = windll.LoadLibrary(dllname)
aptdll.EnableEventDlg(False)
aptdll.APTInit()


def dllinit(dllname='APT.dll'):
	aptdll = windll.LoadLibrary(dllname)
	aptdll.EnableEventDlg(False)
	aptdll.APTInit()
	return aptdll


def Stageinit(SerialNum):
	SerialNum = c_long(SerialNum)
	result=aptdll.InitHWDevice(SerialNum)
	if result == 0:
		pass
	else:
		raise Exception('Connection Failed. Check Serial Number!')


def cleanUpAPT():
	aptdll.APTCleanUp()
	return

def getPos(SerialNum):
	SerialNum = c_long(SerialNum)
	position = c_float()
	aptdll.MOT_GetPosition(SerialNum, pointer(position))
	return position.value


def mAbs(SerialNum,absPosition):
	SerialNum = c_long(SerialNum)
	absolutePosition = c_float(absPosition)
	aptdll.MOT_MoveAbsoluteEx(SerialNum, absolutePosition, True)
	return 

def getVelocityParameters(SerialNum):
	SerialNum = c_long(SerialNum)
	minimumVelocity = c_float()
	acceleration = c_float()
	maximumVelocity = c_float()
	aptdll.MOT_GetVelParams(SerialNum, pointer(maximumAcceleration), pointer(maximumVelocity))
	velocityParameters = [minimumVelocity.value, acceleration.value, maximumVelocity.value]
	return velocityParameterLimits

def setVelocityParameters(SerialNum, minVel, acc, maxVel):
	SerialNum = c_long(SerialNum)
	minimumVelocity = c_float(minVel)
	acceleration = c_float(acc)
	maximumVelocity = c_float(maxVel)
	aptdll.MOT_SetVelParams(SerialNum, minimumVelocity, acceleration, maximumVelocity)
	return

def go_home(SerialNum):
	SerialNum = c_long(SerialNum)
	aptdll.MOT_MoveHome(SerialNum)
	return 

def MoveLine(x1,y1,x2,y2,Velocity):
	Y=y2-y1
	X=x2-x1
	ThetaAngle=math.degrees(math.atan(Y/X))
	VelocityX=Velocity*math.cos(ThetaAngle)
	VelocityY=Velocity*math.sin(ThetaAngle)
	VelocityMatrix = [ VelocityX ,VelocityY]
	return VelocityMatrix

def MoveClockWise(x1,y1,x2,y2,radius,Velocity):

	x3=float( (x1+x2)/2)
	y3=float ( (y1+y2)/2)
	q= float(math.sqrt( ((x2-x1)**2 ) + ((y2-y1)**2)  ))
	r=radius

	Centerx1= float(x3 + math.sqrt((r**2)- ((q/2)**2))*( (y1-y2) /q) )
	Centery1= float(y3 + math.sqrt((r**2)- ((q/2)**2))*( (x2-x1) /q) )
	#print("Centerx1")
	#print(Centerx1)
	#print("Centery1")
	#print(Centery1)

	#Want to increase theta by 0.1 every increment over the arc length
	#starting position is going to be at x1,y1
	ThetaIncrement =0
	PositionX=[]
	PositionY=[]
	VelocityX=[]
	VelocityY=[]
	Xincr=0
	Yincr=0
	#Making all of the angles positive
	#ThetaBetweenCenterAndPointOne = math.degrees( math.acos(((x1-Centerx1)/r)))
	#ThetaBetweenCenterAndPointTwo = math.degrees(math.acos(((x2-Centerx1)/r)))
	ThetaBetweenCenterAndPointOne= math.degrees( math.atan(((y1-Centery1)/(x1-Centerx1))))
	ThetaBetweenCenterAndPointTwo= math.degrees( math.atan(((y2-Centery1)/(x2-Centerx1))))
	if (ThetaBetweenCenterAndPointOne< 0):
		ThetaBetweenCenterAndPointOne = 360- abs(ThetaBetweenCenterAndPointOne)
	if (ThetaBetweenCenterAndPointTwo <0):
		ThetaBetweenCenterAndPointTwo= 360-abs(ThetaBetweenCenterAndPointTwo)	
	#ThetaBetweenCenterAndPointOne = float(math.degrees(math.atan((y1- Centery1  ) / (x1 - Centerx1 ))))
	#ThetaBetweenCenterAndPointTwo = float(math.degrees(math.atan((y2- Centery1  ) / (x2 - Centerx1 ))))

	#print("ThetaBetweenCenterAndPointOne")
	print(ThetaBetweenCenterAndPointOne)
	#print("ThetaBetweenCenterAndPointTwo")
	#print(ThetaBetweenCenterAndPointTwo)
	#For some reason needed to assign variables or it wouldnt work
	PointA=float(ThetaBetweenCenterAndPointOne)
	PointB=float(ThetaBetweenCenterAndPointTwo)
	ThetaAngle=abs(PointB - PointA)
	#print("ThetaAngle")
	print(ThetaAngle)


	#These test values should be the values of X and Y of the starting points
	#print("Starting X Value")
	ThetaRad= math.radians(ThetaBetweenCenterAndPointOne)
	Testing = (radius*(math.cos(ThetaRad)))  +  Centerx1
	print(Testing)

	#print("Starting Y Value")
	ThetaRad= math.radians(ThetaBetweenCenterAndPointOne)
	Testing = (radius*(math.sin(ThetaRad)))  +   Centery1

	print(Testing)

	DistanceTravelDegrees =ThetaBetweenCenterAndPointTwo - ThetaBetweenCenterAndPointOne
	#Condition Checking
	if (DistanceTravelDegrees<0):
		DistanceTravelDegrees = 360 - abs(DistanceTravelDegrees) 
	DistanceCounter = 0.0
	#print("DistanceTravelDegrees")
	ThetaIncrement = ThetaBetweenCenterAndPointOne 
	#print(DistanceTravelDegrees)
	while (float(DistanceCounter) < float(DistanceTravelDegrees)):
		#Start theta at zero and increment along the arc
		#print(ThetaIncrement)

		ThetaRad= math.radians(ThetaIncrement)
		Xincr = ((radius)*math.cos(ThetaRad))+ float(Centerx1)
		Yincr= ((radius)*math.sin(ThetaRad))  + float(Centery1)
		PositionX.append(Xincr)
		PositionY.append(Yincr)
		VelocityX.append((Velocity*math.cos(ThetaIncrement)))
		VelocityY.append((Velocity*math.sin(ThetaIncrement)))
		ThetaIncrement= ThetaIncrement + 0.1
		DistanceCounter= float(DistanceCounter) + 0.1
		#print(DistanceCounter)
		#print(ThetaIncrement)
		if (ThetaIncrement>=360 or (ThetaIncrement<= -360)):
			ThetaIncrement= 0.0
	return PositionX, PositionY, VelocityX, VelocityY

def main():
	try:
		motorx=27250758
		motory=45867342
		motorz=83842570
		Stageinit(motorx)
		Stageinit(motory)
		Stageinit(motorz)
		print(getPos(motorx))
		print(getPos(motory))
		print(getPos(motorz))
		x=1
		y=1
		z=1
		i=0
		processx=Thread(target=mAbs,args=(motorx,x,))
		processy=Thread(target=mAbs,args=(motory,y,))
		processz=Thread(target=mAbs,args=(motorz,z,))
		processx.start()
		processy.start()
		processz.start()
		processx.join()
		processy.join()
		processz.join()
		while (i<3):
			processx=Thread(target=mAbs,args=(motorx,x,))
			processy=Thread(target=mAbs,args=(motory,y,))
			processz=Thread(target=mAbs,args=(motorz,z,))
			processx.start()
			processy.start()
			processz.start()
			processx.join()
			processy.join()
			processz.join()
			i=i+1
			if (i%2)!=0:
				x=10
				y=50
				z=10
			else:
				x=1
				y=1
				z=1
			print(i)
		
		processx=Thread(target=go_home,args=(motorx,))
		processy=Thread(target=go_home,args=(motory,))
		processz=Thread(target=go_home,args=(motorz,))
		processx.start()
		processy.start()
		processz.start()
		processx.join()
		processy.join()
		processz.join()


		cleanUpAPT()
	except:
		cleanUpAPT()

if __name__ == "__main__":
	main()
