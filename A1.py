from __future__ import print_function

import time
from sr.robot import *

a_th = 1.5
""" float: Threshold for the control of the linear distance"""
d_th = 0.4
""" float: Threshold for the control of the orientation"""
R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def find_token(): 
    """
    Function to find the closest silver token
    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected at a distance more than 3) 
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected at a distance more than 3)
    """
    dist=10
    for token in R.see():
    
        if token.dist < dist and token.rot_y>-20 and token.rot_y< 20 and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
	    rot_y=token.rot_y

    if dist>3:
	return -1, -1
    else:
   	return dist, rot_y   
    

def find_golden_token():
    """     
    Orientation function by side golden token
    Returns:
       Gdist(float): distance to the side nearest gold token (-1 if the gold token is found in the range 89<Grot_y<91 or -89>Grot_y>-91
       Grot_y (float): the angle between the robot and the gold token (-1 if the gold token is detected in the range 89<Grot_y<91 or -89>Grot_y>-91)
    """
    Gdist=1.5
    for token in R.see():
    
	if token.dist < Gdist and  token.rot_y<135 and token.rot_y>45 and token.info.marker_type is MARKER_TOKEN_GOLD:
            Gdist=token.dist
	    Grot_y=token.rot_y

	if token.dist < Gdist and token.rot_y>-135 and token.rot_y<-45 and token.info.marker_type is MARKER_TOKEN_GOLD:
            Gdist=token.dist
	    Grot_y=token.rot_y

    if Grot_y>89 and Grot_y<91 or Grot_y<-89 and Grot_y>-91:
	return -1, -1
    else:
   	return Gdist, Grot_y

	    
def distance_token():
    """
       Function to find the nearest front gold token
    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected at a distance more than 3)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected at a distance more than 3)
    """  

    distance=8
    for token in R.see():
        if token.dist < distance and token.rot_y>-10 and token.rot_y<10 and token.info.marker_type is MARKER_TOKEN_GOLD:
            distance=token.dist
	    rot=token.rot_y
	    
    if distance<2:
	return distance, rot
    else:
   	return -1, -1
 
dist_rot = 2  # a distance to detect the boxes in rotation 
"""                
Rotation function.
    Arguments:
distance (float):
    Return:
    Correct, if the angle is negative, then the robot turns left
    False, if the angle is positive, the robot turns right.
"""

def rotate():
    dist = dist_rot
    # Detecting any obstacles from the sides to avoid it by rotating 
    for token in R.see():
        if (-110<token.rot_y<-70 or 70<token.rot_y<110) and token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist = token.dist
            rotate = token.rot_y
    # Turning right with a speed of 25 in 0.1 sec
    if rotate < 0:
        turn(1400, 0.2)
        return False
    # Turning left with a speed of 25 in 0.1 sec
    else:
        turn(-1400, 0.2)
        return True

  	
#-----------------------------------------------------------------------------  
 
while 1:
   
   Gdist, Grot_y = find_golden_token()
   dist, rot_y = find_token()
   
   t=0.1
   """ 
    Access to the first token at the beginning
   """   
  
   if dist==-1:

       Gdist, Grot_y = find_golden_token()
       dist, rot_y = find_token()
       
       """  Alignment for moving straight """
       
       while Grot_y!=-1 and  dist==-1:
           Gdist, Grot_y = find_golden_token()
	   dist, rot_y = find_token()
	   print("  @@ Grot_y=", Grot_y )
	   
	   if Grot_y < -45 and Grot_y > -90:    
               turn(9, t)
	   elif Grot_y > 45 and Grot_y < 90 :
               turn(-9, t)
           elif Grot_y > -135 and Grot_y < -90:    
               turn(-9, t)
	   elif Grot_y > 90 and Grot_y < 135 :
               turn(9, t)
                             
       
       """ Front Wall Detection """
       if Grot_y==-1 and  dist==-1:        
           distance, rot = distance_token()
           dist, rot_y = find_token()
           
           """ Moving backwards when approaching the wall """
           if distance<0.5 and distance>0:
               print("           STOP        ")
               drive(-150, t)
               distance, rot = distance_token()
               print( "      distance =   ", distance )
                       
           if distance<0.75 and distance>0.5:
               print("            BACK ")
               drive(-50, t)
               distance, rot = distance_token()
               print( "      distance =   ", distance)
           
           
           """ Mid-distance turn """
           if distance>0.75 and distance<1.25:
               print("      !!  find_token ")
               dist, rot_y = find_token()
               time.sleep(2)
               rotate() 
               time.sleep(2) 
              
               drive(400, t)
               Gdist, Grot_y = find_golden_token()
               dist, rot_y = find_token()
               distance, rot = distance_token()
                       
           
           """ Moving forward a long distance to the wall """
           if distance<2 and distance>1.25:
               print("            FORWARD       ")
               drive(50, t)
               distance, rot = distance_token()
               dist, rot_y = find_token()
               print( "      distance=   ", distance,  )


           
           elif distance==-1:
               drive(900, t)
               distance, rot = distance_token()
               Gdist, Grot_y = find_golden_token()  
               print("      Go to wall!", distance  )

#-----------------------------------------------------------------------------    

   elif dist <d_th:  # if we are close to the token, we try grab it.
        print("            Found it!")
        if R.grab(): # if we grab the token, we move the robot on the right, we release the token, and we move the robot back and on the left
            print("            Gotcha!")
	    turn(35, 2)
	    R.release()
	    drive(-15,2)
	    turn(-35,2)
	else:
            print("  Aww, I'm not close enough.")
            drive(-15,2)
   elif -a_th<= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
	print("Ah, that'll do.")
        drive(10, 0.5)
   elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
       
        print(" dist=", dist )
        print("Left a bit...")
        turn(-2, 0.5)
   elif rot_y > a_th:
       
        print("  dist=", dist )
        print("Right a bit...")
        turn(+2, 0.5)

