# Here are the assignment 1 of RT course
____
## Assignment 1: Python Robotics Simulation
____
Sensors can detect boxes around all directions (from -180.0 degrees to 180.0 degrees). Write a python script for achieving this robot’s behaviour:

* constrantly drive the robot around the circuit in the counter-clockwise direction
* avoid touching the golden boxes
* when the robot is close to a silver box, it should grab it, and move it behind itself

## The first task is in /assignment_1
____
# Installing and running
The simulator requires a Python 2.7 installation, the pygame library, PyPyBox2D, and PyYAML.

Pygame, unfortunately, can be tricky (though not impossible) to install in virtual environments. If you are using pip, you might try pip install hg+https://bitbucket.org/pygame/pygame, or you could use your operating system's package manager. Windows users could use Portable Python. PyPyBox2D and PyYAML are more forgiving, and should install just fine using pip or easy_install.
____
# Troubleshooting
When running python run.py <file>, you may be presented with an error: ImportError: No module named 'robot'. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
  * Find the location of srtools: pip show sr.tools
  * Get the location. In my case this was /usr/local/lib/python2.7/dist-packages
  * Create symlink: ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/
  ____
  # To run:
 Open a terminal, git clone the task and run the following commands:
```
$ python run.py Ex1.py
 ```
 ____
  # Solution:
 Flowchart: ex1.drawio.png

 ![Alt-текст](https://github.com/DariaShV/RT_Assignment1/blob/main/ex1.drawio.png "Flowchart")
 
 ## DRIVE function
 ____
 The simulated robot has two motors configured for skid steering, connected to a two-output Motor Board. The left motor is connected to output 0 and the right motor to output 1.

The Motor Board API is identical to that of the SR API, except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

Function for setting a linear velocity with provided speed and time.

Arguments: speed (int): the speed of the wheels seconds (int): the time interval
 ```
 def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
 ```
 ____
## TURN function
Function for setting an angular velocity

Arguments: speed (int): the speed of the wheels seconds (int): the time interval 
 ```
 def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
 ```
 ____
 ## find_token()
 ____
 Function to find the closest silver token

 Returns:
distance of the closest silver token (-1 if no silver token is detected at a distance more than 3) 
angle between the robot and the silver token (-1 if no silver token is detected at a distance more than 3)

 ```
 def find_token(): 
    dist=10
    for token in R.see():
        if token.dist < dist and token.rot_y>-20 and token.rot_y< 20 and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
	    rot_y=token.rot_y
    if dist>3:
	return -1, -1
    else:
   	return dist, rot_y   
 ```
 ____
 ##  find_golden_token()
 ____
  Orientation function by side golden token
    Returns:
       distance to the side nearest gold token (-1 if the gold token is found in the range 89<Grot_y<91 or -89>Grot_y>-91
       the angle between the robot and the gold token (-1 if the gold token is detected in the range 89<Grot_y<91 or -89>Grot_y>-91)
```  
def find_golden_token()   
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
 ```
____
 ##  forward_token():
 ____
 Function to find the nearest front gold token
    Returns:
distance of the closest golden token (-1 if no golden token is detected at a distance more than 3)
angle between the robot and the golden token (-1 if no golden token is detected at a distance more than 3)

  ____
 ##  rotate():
	 ____
 Rotation function
    Return:
    Correct, if the angle is negative, then the robot turns left
    False, if the angle is positive, the robot turns right.
```
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
 ```	
