import numpy as np
import cv2
import time
import math
import _thread
from simple_pid import PID
from funciones import *

field_path = 'DCC/base/field.jpg'

class irb_sim:
    robot1 = Robot(np.array([0,0,0]))  # --> [x, y, thetha]
    ball = Pelota(np.array([0,0,0]))
    game_field = cv2.imread(field_path)

    def draw_robot(self, rob, color_front, color_back):
        # pos circulo frontal del robot
        r1_fx = int(rob.pos[0] + 30*math.cos(rob.pos[2]))
        r1_fy = int(rob.pos[1] + 30*math.sin(rob.pos[2]))
		
        # pos circulo posterior del robot
        r1_bx = int(rob.pos[0] + 0*math.cos(rob.pos[2]))
        r1_by = int(rob.pos[1] + 0*math.sin(rob.pos[2]))

        # dibujar 
        cv2.circle(self.game_field,(r1_fx, r1_fy), 10, color_front, -1)
        cv2.circle(self.game_field,(r1_bx, r1_by), 10, color_back, -1)
    
    def draw(self):
        self.game_field = cv2.imread(field_path)
        cv2.circle(self.game_field,(self.ball.pos[0],self.ball.pos[1]), 10, (0, 255, 255), -1)
        
        self.draw_robot(self.robot1,(0,0,255), (255,0,0))
        

global frame
global nClick

global Robot1hsvFrontColor
global Robot1hsvBackColor
global BallhsvBallColor 

global Robot1goalx
global Robot1goaly
global Robot2goalx
global Robot2goaly

global xcr_Robot1ColorBack
global ycr_Robot1ColorBack	
global xcr_Robot1ColorFront
global ycr_Robot1ColorFront
global xcr_BallColor
global ycr_BallColor

global theta
global dist
global cmd
global r1Ar
global r1Al

Robot1hsvFrontColor = np.array([0,0,0])
Robot1hsvBackColor = np.array([0,0,0])
BallhsvBallColor = np.array([0,0,0]) 

Robot1goalx = 0
Robot1goaly = 0
Robot2goalx = 0
Robot2goaly = 0

xcr_Robot1ColorBack = 0
ycr_Robot1ColorBack = 0	
xcr_Robot1ColorFront = 0
ycr_Robot1ColorFront = 0
xcr_BallColor = 0
ycr_BallColor = 0	

theta = 0
dist = 0
cmd = "0,0"
r1Al = 0
r1Ar = 0

LowerColorError = np.array([-10,-35,-35])
UpperColorError = np.array([10,35,35])

# Evita divisiones por cero
epcilon = 0.00001

# Permite que solo un robot renga la pelota


global grupo1
grupo1 = irb_sim()

# Backend
def start(delay):
    global pelota
    global r1Ar
    global r1Al
    STATE = "PELOTA"
    #r1Ar: PWM rueda derecha
    #r1Al: PWM rueda izquierda
    #dist: distancia robot-pelota
    #theta: angulo robot-pelota

    pid_ang = PID(1, 0.1, 0.05, setpoint=0)
    pid_ang.output_limits = (-250, 250)
    pid_ang.sample_time = 0.2
    delta_ang = 10
    
    pid_lin = PID(2, 0.5, 0.1, setpoint=20)
    pid_lin.output_limits = (-250, 250)
    pid_lin.sample_time = 0.2

    # Juegue_1_rob(grupo1.robot1, dist, theta)
    while(True):
		#Ciclo de programacion
	    if STATE == "PELOTA":
		    if abs(dist) < 30:
			    r1Ar = 0
			    r1Al = 0
		    else:
			    control_R = -pid_ang(theta)
			    control_L = pid_ang(theta)

				# Correccion linearl solo si el agulo es pequeño
			    if abs(theta) < delta_ang:
				    control_R -= pid_lin(dist)
				    control_L -= pid_lin(dist)
					
					
			    r1Ar = control_R
			    r1Al = control_L

		    print("Angulo: " + str(theta))
		    print("Distancia: " + str(dist))
		    time.sleep(0.2)
	

cv2.namedWindow('realidad', cv2.WINDOW_AUTOSIZE)

# Frontend
def sim_run(delay):
	global grupo1
	global r1Ar
	global r1Al
	r1x = 100
	r1y = 100
	r1a = 0
	rbx = 350
	rby = 350
	
	
	grupo1.robot1.pos = np.array([r1x,r1y,r1a])
	grupo1.ball.pos = np.array([rbx,rby,0])
	grupo1.draw()
	t = 0
	t_step = 0.027
	m = 0.5
	
	r1Vl = 0
	r1Vr = 0
	r1Al = 0
	r1Ar = 0
	
	while(True):
		
		r1Vr = r1Vr + r1Ar*t_step*t_step/2 - r1Vr*0.02
		r1Vl = r1Vl + r1Al*t_step*t_step/2 - r1Vl*0.02
		
		r1x_p = 0.5*(r1Vr + r1Vl)*math.cos(r1a)
		r1y_p = 0.5*(r1Vr + r1Vl)*math.sin(r1a)
		r1a_p = 0.5*(r1Vr - r1Vl)/15
		
		r1x = r1x + r1x_p*t_step
		r1y = r1y + r1y_p*t_step
		r1a = r1a + r1a_p*t_step
		
		grupo1.robot1.pos = np.array([r1x,r1y,r1a])
		grupo1.draw()
			
		
		

cv2.namedWindow('res',  cv2.WINDOW_AUTOSIZE )	
cv2.moveWindow('res', 700, 100)

_thread.start_new_thread(sim_run, (1,))
_thread.start_new_thread(  start, (1,))

frame = grupo1.game_field
frame = grupo1.game_field
Ypx, Xpx, ch = frame.shape
Ypx = int(Ypx/2)
Xpx = int(Xpx/2)


while(True):
	frame = grupo1.game_field	
	# Convert BGR to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
	Robot1LowerColorBack = np.array([120,255,255]) + LowerColorError
	Robot1UpperColorBack = np.array([120,255,255]) + UpperColorError	
	Robot1LowerColorFront = np.array([0,255,255]) + LowerColorError
	Robot1UpperColorFront = np.array([0,255,255]) + UpperColorError	

	BallLowerColor = np.array([30,255,255]) + LowerColorError
	BallUpperColor = np.array([30,255,255]) + UpperColorError	
	
    # Threshold for HSV image
	Robot1ColorBackMask = cv2.inRange(hsv, Robot1LowerColorBack, Robot1UpperColorBack)
	Robot1ColorBackBlur = cv2.GaussianBlur(Robot1ColorBackMask,(31,31),0)
	Robot1ColorBackRet, Robot1ColorBackOTSUMask = cv2.threshold(Robot1ColorBackBlur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	Robot1ColorFrontMask = cv2.inRange(hsv, Robot1LowerColorFront, Robot1UpperColorFront)
	Robot1ColorFrontBlur = cv2.GaussianBlur(Robot1ColorFrontMask,(31,31),0)
	Robot1ColorFrontRet, Robot1ColorFrontOTSUMask = cv2.threshold(Robot1ColorFrontBlur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	
	BallColorMask = cv2.inRange(hsv, BallLowerColor, BallUpperColor)
	BallColorBlur = cv2.GaussianBlur(BallColorMask,(31,31),0)
	BallColorRet, BallColorOTSUMask = cv2.threshold(BallColorBlur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)	
 
	# Bitwise-AND mask and original image
	Robot1ColorBackRes = cv2.bitwise_and(frame,frame, mask= Robot1ColorBackOTSUMask)
	Robot1ColorFrontRes = cv2.bitwise_and(frame,frame, mask= Robot1ColorFrontOTSUMask)	
	BallColorRes = cv2.bitwise_and(frame,frame, mask= BallColorOTSUMask)	
		
	res = Robot1ColorBackRes + Robot1ColorFrontRes + BallColorRes

	Robot1ColorBackMoments = cv2.moments(Robot1ColorBackOTSUMask, 1)
	m00_Robot1ColorBack = int(Robot1ColorBackMoments['m00'])
	m01_Robot1ColorBack = int(Robot1ColorBackMoments['m01'])
	m10_Robot1ColorBack = int(Robot1ColorBackMoments['m10'])	
	Robot1ColorFrontMoments = cv2.moments(Robot1ColorFrontOTSUMask, 1)
	m00_Robot1ColorFront = int(Robot1ColorFrontMoments['m00'])
	m01_Robot1ColorFront = int(Robot1ColorFrontMoments['m01'])
	m10_Robot1ColorFront = int(Robot1ColorFrontMoments['m10'])
	
	BallColorMoments = cv2.moments(BallColorOTSUMask, 1)
	m00_BallColor = int(BallColorMoments['m00'])
	m01_BallColor = int(BallColorMoments['m01'])
	m10_BallColor = int(BallColorMoments['m10'])	
	

	if(m00_BallColor*m00_Robot1ColorBack*m00_Robot1ColorFront> 0):
		
		xc_Robot1ColorBack = int(m10_Robot1ColorBack/m00_Robot1ColorBack)
		yc_Robot1ColorBack = int(m01_Robot1ColorBack/m00_Robot1ColorBack)	
		xc_Robot1ColorFront = int(m10_Robot1ColorFront/m00_Robot1ColorFront)
		yc_Robot1ColorFront = int(m01_Robot1ColorFront/m00_Robot1ColorFront) 
		
		xc_BallColor = int(m10_BallColor/m00_BallColor)
		yc_BallColor = int(m01_BallColor/m00_BallColor)	

		xcr_Robot1ColorBack = xc_Robot1ColorBack - Xpx
		ycr_Robot1ColorBack = yc_Robot1ColorBack - Ypx	
		xcr_Robot1ColorFront = xc_Robot1ColorFront - Xpx
		ycr_Robot1ColorFront = yc_Robot1ColorFront - Ypx
		
		xcr_BallColor = xc_BallColor - Xpx
		ycr_BallColor = yc_BallColor - Ypx			
		
		ax = xcr_Robot1ColorFront - xcr_Robot1ColorBack
		ay = ycr_Robot1ColorFront - ycr_Robot1ColorBack
		bx = xcr_BallColor - xcr_Robot1ColorBack
		by = ycr_BallColor - ycr_Robot1ColorBack
		
		r1mx = int((xcr_Robot1ColorFront + xcr_Robot1ColorBack)/2)
		r1my = int((ycr_Robot1ColorFront + ycr_Robot1ColorBack)/2)
		if(ay != 0):
			m = -ax/ay
			n = r1my - m*r1mx
			if(ycr_Robot1ColorFront < ycr_Robot1ColorBack):
				p1x = int(r1mx + 10) + Xpx
				p1y = int(m*(p1x-Xpx)+ n) + Ypx
				p2x = int(r1mx - 10) + Xpx
				p2y = int(m*(p2x-Xpx)+ n) + Ypx
			else:
				p1x = int(r1mx - 10) + Xpx
				p1y = int(m*(p1x-Xpx)+ n) + Ypx
				p2x = int(r1mx + 10) + Xpx
				p2y = int(m*(p2x-Xpx)+ n) + Ypx
		else:
			m = 0
			p1x = r1mx + Xpx
			p1y = r1my + 10 + Ypx
			p2x = r1mx + Xpx
			p2y = r1my - 10 + Ypx
		
		am = math.sqrt(math.pow(ax, 2) + math.pow(ay, 2))
		bm = math.sqrt(math.pow(bx, 2) + math.pow(by, 2)) 
		ab = ax*bx + ay*by
		
		d1 = int(math.sqrt(math.pow(xcr_BallColor - p1x + Xpx, 2) + math.pow(ycr_BallColor - p1y + Ypx, 2)))
		d2 = int(math.sqrt(math.pow(xcr_BallColor - p2x + Xpx, 2) + math.pow(ycr_BallColor - p2y + Ypx, 2)))
		dist = int(math.sqrt(math.pow(xcr_BallColor - xcr_Robot1ColorFront, 2) + math.pow(ycr_BallColor - ycr_Robot1ColorFront, 2)))
		
		theta = 0
		if(am*bm > 0):
			if(d1 < d2):
				theta = int(math.acos(ab/(am*bm + epcilon))*180/math.pi)
			else:
				theta = -int(math.acos(ab/(am*bm + epcilon))*180/math.pi)
		else:
			theta = 0

			
		cv2.line(res, (xc_Robot1ColorBack, yc_Robot1ColorBack), (xc_Robot1ColorFront, yc_Robot1ColorFront), (255,0,0),3)
		cv2.line(res, (xc_Robot1ColorBack, yc_Robot1ColorBack), (xc_BallColor, yc_BallColor), (255,0,0),3)
		
		cv2.line(res, (Xpx-int(Xpx*3/2), Ypx), (Xpx+int(Xpx*3/2), Ypx), (0,255,0),1)
		cv2.line(res, (Xpx, Ypx-int(Ypx*3/2)), (Xpx, Ypx+int(Ypx*3/2)), (0,255,0),1)
		
		# cv2.line(res, (p1x, p1y), (p2x, p2y), (0,0,255),3)
		
		cv2.circle(res,(xc_Robot1ColorBack,yc_Robot1ColorBack), 3, (0,0,255), -1)
		cv2.circle(res,(xc_Robot1ColorFront,yc_Robot1ColorFront), 3, (0,0,255), -1)
		cv2.circle(res,(xc_BallColor,yc_BallColor), 3, (0,0,255), -1)
		cv2.circle(res,(r1mx + Xpx,r1my + Ypx), 3, (0,0,255), -1)
		
		cv2.circle(res,(Robot1goalx,Robot1goaly), 10, (0,0,255), -1)
		cv2.circle(res,(Robot2goalx,Robot2goaly), 10, (0,0,255), -1)
		cv2.circle(res,(p1x,p1y), 2, (0,0,255), -1)
		cv2.circle(res,(p2x,p2y), 2, (0,0,255), -1)
				
		# cv2.putText(res, "(" + str(xcr_Robot1ColorBack) + "," + str(ycr_Robot1ColorBack) + ")",(xc_Robot1ColorBack,yc_Robot1ColorBack), 5, 1, (255,255,255),1,8,False)
		# cv2.putText(res, "(" + str(xcr_Robot1ColorFront) + "," + str(ycr_Robot1ColorFront) + ")",(xc_Robot1ColorFront,yc_Robot1ColorFront), 5, 1, (255,255,255),1,8,False)
		# cv2.putText(res, "(" + str(xcr_BallColor) + "," + str(ycr_BallColor) + ")",(xc_BallColor,yc_BallColor), 5, 1, (255,255,255),1,8,False)
		
		# cv2.putText(res, "<" + str(theta) + " |" + str(dist),(xc_BallColor+30,yc_BallColor+30), 5, 1, (255,255,255),1,8,False)
		# cv2.putText(res, "P1(" + str(d1) + ")",(p1x,p1y), 5, 1, (0,255,0),1,8,False)
		# cv2.putText(res, "P2(" + str(d2) + ")",(p2x,p2y), 5, 1, (0,255,0),1,8,False)		
		
		
	# cv2.imshow('frame',frame)	
	cv2.imshow('res',res)
	cv2.imshow('realidad', grupo1.game_field)


	if cv2.waitKey(1) & 0xFF == 27:
		break


cv2.destroyAllWindows()