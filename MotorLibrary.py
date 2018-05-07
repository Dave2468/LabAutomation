from ctypes import c_long, c_buffer, c_float, windll, pointer
import os
from multiprocessing import Process, Value
from threading import Thread
import math
import time
import numpy as np  
import matplotlib.pyplot as plt

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

def setVelocityParameters(SerialNum, minVel, acc, maxVel):
	SerialNum = c_long(SerialNum)
	minimumVelocity = c_float(minVel)
	acceleration = c_float(acc)
	maximumVelocity = c_float(maxVel)
	aptdll.MOT_SetVelParams(SerialNum, minimumVelocity, acceleration, maximumVelocity)
	return
def getVelocityParameters(SerialNum):
	SerialNum = c_long(SerialNum)
	minimumVelocity = c_float()
	acceleration = c_float()
	maximumVelocity = c_float()
	aptdll.MOT_GetVelParams(SerialNum, pointer(minimumVelocity), pointer(acceleration), pointer(maximumVelocity))
	velocityParameters = [minimumVelocity.value, acceleration.value, maximumVelocity.value]
	return velocityParameters

def go_home(SerialNum):
	SerialNum = c_long(SerialNum)
	channel=c_long(0)
	aptdll.MOT_MoveHome(SerialNum,channel)
	return 

def setVel(SerialNum, maxVel):
	minVel, acc, oldVel = getVelocityParameters(SerialNum)
	setVelocityParameters(SerialNum, minVel, acc, maxVel)
	return 

def MoveLine(x1,y1,x2,y2,Velocity):
	Y=y2-y1
	X=x2-x1
	ThetaAngle=math.atan(Y/X)
	VelocityX=Velocity*math.cos(ThetaAngle)
	VelocityY=Velocity*math.sin(ThetaAngle)
	return VelocityX, VelocityY

def MoveClock(x1,y1,x2,y2,radius,Velocity,Direction):

	x3=float( (x1+x2)/2)
	y3=float ( (y1+y2)/2)
	q= float(math.sqrt( ((x2-x1)**2 ) + ((y2-y1)**2)  ))
	r=radius

	Centerx1= float(x3 + math.sqrt((r**2)- ((q/2)**2))*( (y1-y2) /q) )
	Centery1= float(y3 + math.sqrt((r**2)- ((q/2)**2))*( (x2-x1) /q) )

	ThetaIncrement =0
	PositionX=[]
	PositionY=[]
	VelocityX=[]
	VelocityY=[]
	Xincr=0
	Yincr=0

	ThetaBetweenCenterAndPointOne= math.degrees( math.atan(((y1-Centery1)/(x1-Centerx1))))
	ThetaBetweenCenterAndPointTwo= math.degrees( math.atan(((y2-Centery1)/(x2-Centerx1))))
	if (ThetaBetweenCenterAndPointOne< 0):
		ThetaBetweenCenterAndPointOne = 360 + ThetaBetweenCenterAndPointOne
	if (ThetaBetweenCenterAndPointTwo <0):
		ThetaBetweenCenterAndPointTwo= 360 + ThetaBetweenCenterAndPointTwo
	if (ThetaBetweenCenterAndPointOne > 360):
		ThetaBetweenCenterAndPointOne =  ThetaBetweenCenterAndPointOne -360
	if (ThetaBetweenCenterAndPointTwo >360):
		ThetaBetweenCenterAndPointTwo= ThetaBetweenCenterAndPointTwo -360

	#print("Theta 1")
	#print(ThetaBetweenCenterAndPointOne)
	#print("Theta 2")
	#print(ThetaBetweenCenterAndPointTwo)
	PointA=float(ThetaBetweenCenterAndPointOne)
	PointB=float(ThetaBetweenCenterAndPointTwo)
	ThetaAngle=abs(PointB - PointA)
	#print("Theta Angle")
	#print(ThetaAngle)
	
	
	DistanceTravelDegrees=0.0
	if (ThetaAngle<0):
		ThetaAngle= 360 + ThetaAngle
	elif(ThetaAngle> 360):
		ThetaAngle = ThetaAngle- 360



	ThetaRad = 0.0
	DirectionAddition = 10
	DistanceCounter = 0.0
	ThetaIncrement = ThetaBetweenCenterAndPointOne 

	if (Direction == "clk"):
		DirectionAddition = -DirectionAddition
		if (ThetaBetweenCenterAndPointOne>ThetaBetweenCenterAndPointTwo):
			DistanceTravelDegrees =ThetaAngle
		elif(ThetaBetweenCenterAndPointOne<ThetaBetweenCenterAndPointTwo):
			DistanceTravelDegrees =360-ThetaAngle
	elif(Direction=="cnlk"):
		DirectionAddition = DirectionAddition
		if (ThetaBetweenCenterAndPointOne>ThetaBetweenCenterAndPointTwo):
			DistanceTravelDegrees =360- ThetaAngle
		elif(ThetaBetweenCenterAndPointOne<ThetaBetweenCenterAndPointTwo):
			DistanceTravelDegrees =ThetaAngle

	while ( float(DistanceCounter) <= float(DistanceTravelDegrees)):
		#Start theta at zero and increment along the arc
		#print(ThetaIncrement)
		ThetaRad= math.radians(ThetaIncrement)
		Xincr =((radius)*math.cos(ThetaRad))+ float(Centerx1)
		Yincr= ((radius)*math.sin(ThetaRad))+ float(Centery1)
		PositionX.append(Xincr)
		PositionY.append(Yincr)
		VelocityX.append(abs(Velocity*math.cos(ThetaRad)))
		VelocityY.append(abs(Velocity*math.sin(ThetaRad)))
		
		ThetaIncrement= ThetaIncrement + DirectionAddition
		DistanceCounter= float(DistanceCounter) + abs(DirectionAddition)

		if (ThetaIncrement>360 ):
			ThetaIncrement= 0.0
		if (ThetaIncrement < 0):
			ThetaIncrement = ThetaIncrement + 360


	return PositionX, PositionY, VelocityX, VelocityY

def MoveCircle(SerialNumX,SerialNumY,x1,y1,x2,y2,radius,Velocity,Direction):
	PosX,PosY,VelX,VelY=MoveClock(x1,y1,x2,y2,radius,Velocity,Direction)
	i = 1
	while (i<len(PosX)):
		aptdll.MOT_SetVelParams(c_long(SerialNumX), c_float(0), c_float(1.5), c_float(VelX[i-1]))
		aptdll.MOT_SetVelParams(c_long(SerialNumY), c_float(0), c_float(1.5), c_float(VelY[i-1]))
		#setVel(SerialNumX,VelX[i-1])
		#setVel(SerialNumY,VelY[i-1])
		print("Iteration %f" % i)
		print("X: %f Y:%f"%(PosX[i],PosY[i]))
		processX=Thread(target=mAbs,args=(SerialNumX,PosX[i],))
		processY=Thread(target=mAbs,args=(SerialNumY,PosY[i],))
		processX.start()
		processY.start()
		processX.join()
		processY.join()
		i = i + 1
	return PosX,PosY


def LinearProcess(SerialNumX,SerialNumY,x2,y2,Velocity):
	#This function is for moving from your current position to a new position
	x1=getPos(SerialNumX)
	y1=getPos(SerialNumY)
	VelX, VelY = MoveLine(x1,y1,x2,y2,Velocity)
	setVel(SerialNumX,VelX)
	setVel(SerialNumY,VelY)
	processX=Thread(target=mAbs,args=(SerialNumX,x2,))
	processY=Thread(target=mAbs,args=(SerialNumY,y2,))
	processX.start()
	processY.start()
	processX.join()
	processY.join()
	time.sleep(0.1)
	X = np.linspace(x1,x2,50,endpoint=True)
	Y=  np.linspace(y1,y2,50,endpoint=True)
	return X,Y
	

def main():
	try:
		#Initializing the motors
		#Y-motor stage range 0 - 50
		#X-motor stage range 0 - 150
		motorx=45867342
		motory=83842570
		motorz=27250758
		Stageinit(motorx)
		Stageinit(motory)
		go_home(motorx)
		go_home(motory)
		mAbs(motorx,0)
		mAbs(motory,0)
		print(getVelocityParameters(45867342))
		print(getVelocityParameters(83842570))

		X,Y= LinearProcess(motorx,motory,60,10,2)
		plt.plot(X,Y,color='red',alpha=1.00)
		X,Y=MoveCircle(motorx,motory,60,10,65,20,15,2,"clk")
		plt.plot(X,Y,color='blue',alpha=1.00)
		#X,Y= LinearProcess(motorx,motory,15,10,2)
		#plt.plot(X,Y,color='red',alpha=1.00)
		setVel(45867342,19)
		setVel(83842570,2)
		mAbs(motorx,0)
		mAbs(motory,0)
		plt.ylim(0,50)
		plt.xlim(0,150)
		plt.show()


		cleanUpAPT()
	except:
		cleanUpAPT()

if __name__ == "__main__":
	os.system('cls')
	main()
