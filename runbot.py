# runbot.py
# Main program for basic directional controls on LEGObot Mk1

import sys
import time
import RPi.GPIO as GPIO

#Variables
ROBOTMOVING = False

#Setup GPIO pins
GPIO.setmode(GPIO.BOARD)  #use board pin numbering
GPIO.setup(11, GPIO.OUT)  #set pin as output, for motor1 - LEFT
GPIO.output(11, GPIO.LOW)        #make sure the pin is preset LOW
GPIO.setup(12, GPIO.OUT)  #set pin as output, for motor1 - LEFT
GPIO.output(12, GPIO.LOW)        #make sure the pin is preset LOW
GPIO.setup(15, GPIO.OUT)  #set pin as output, for motor2 - RIGHT
GPIO.output(15, GPIO.LOW)        #make sure the pin is preset LOW
GPIO.setup(16, GPIO.OUT)  #set pin as output, for motor2 - RIGHT
GPIO.output(16, GPIO.LOW)        #make sure the pin is preset LOW

# Function to turn OFF LED when robot in standby mode
def robot_standby():
    #GPIO.output(13, GPIO.LOW)  #set pin LOW for LED OFF
    ROBOTMOVING = False

# Function to turn ON LED any time the robot is moving
def robot_moving():
    #GPIO.output(13, GPIO.HIGH)  #set pin HIGH for LED ON
    ROBOTMOVING = True

# Function for moving robot forward
def move_forward():
    try:
        #start forward motion until command to stop or turn
        #set GPIO values for two wheel synchronized forward motion
        #LEFT MOTOR FORWARD
        GPIO.output(11, GPIO.HIGH)  #set motor1 pin 11 HIGH
        GPIO.output(12, GPIO.LOW)  #set motor1 pin 12 LOW
        #RIGHT MOTOR FORWARD
        GPIO.output(15, GPIO.HIGH)  #set motor2 pin 15 HIGH
        GPIO.output(16, GPIO.LOW)  #set motor2 pin 16 LOW
        robot_moving()
        print("moving forward")
        return 1;  #return success
    except:
        return 0;  #return fail

# Function for moving in reverse
def move_backward():
    try:
        #set GPIO values to move both motors in reverse
        #LEFT MOTOR BACKWARD
        GPIO.output(11, GPIO.LOW)  #set motor1 pin 11 LOW
        GPIO.output(12, GPIO.HIGH)  #set motor1 pin 12 HIGH
        #RIGHT MOTOR BACKWARD
        GPIO.output(15, GPIO.LOW)  #set motor2 pin 15 LOW
        GPIO.output(16, GPIO.HIGH)  #set motor2 pin 16 HIGH
        robot_moving()
        print("moving backward")
        time.sleep(3)  #backup for predefined timeframe of 3 secs, then stop
        #LEFT MOTOR OFF
        GPIO.output(11, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        #RIGHT MOTOR OFF
        GPIO.output(15, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
        print("reverse stopped")
        return 1;  #return success
    except:
        return 0;  #return fail

# Function for turning right
def pivot_right():
    try:
        #pivot right using left wheel fwd, right wheel back
        #LEFT MOTOR FORWARD
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(12, GPIO.LOW)
        #RIGHT MOTOR REVERSE
        GPIO.output(15, GPIO.LOW)
        GPIO.output(16, GPIO.HIGH)
        robot_moving()
        print("turning right")
        return 1;  #return success
    except:
        return 0;  #return fail

# Function for turning left
def pivot_left():
    try:
        #pivot left using right wheel motion fwd, left wheel back
        #LEFT MOTOR REVERSE
        GPIO.output(11, GPIO.LOW)
        GPIO.output(12, GPIO.HIGH)
        #RIGHT MOTOR FORWARD
        GPIO.output(15, GPIO.HIGH)
        GPIO.output(16, GPIO.LOW)
        robot_moving()
        print("turning left")
        return 1;  #return success
    except:
        return 0;  #return fail

# Function for stopping the robot
def stop_movement():
    try:
        #set GPIO values for both motors off
        #LEFT MOTOR OFF
        GPIO.output(11, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        #RIGHT MOTOR OFF
        GPIO.output(15, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
        robot_standby()
        print("stopping!")
        return 1;  #return success
    except:
        return 0;  #return fail

# Function for cleanly exiting the program
def exit_command():
    try:
        #set GPIO to stop all motor movement
        stop_movement()

        GPIO.cleanup()      #run GPIO cleanup
        print("exiting")
        return 1;  #return success
    except:
        return 0;  #return fail

# MORE MOVEMENT FUNCTIONS HERE [FUTURE]
# add movement functions for greater precision, ie. turn_left_fast and turn_left_slow

# Start the main program
print("Welcome to the LEGObot Mk1 prototype command program.")
print("Valid Commands: 1=start, 2=stop, 3=backup, 7=left, 8=right, 0=quit")
print("Please enter a command to begin...")

try:
    while True:
        cmd = int(input("> "))
        if cmd == 1:
            move_forward()
        elif cmd == 2:
            stop_movement()
        elif cmd == 3:
            move_backward()
        elif cmd == 7:
            pivot_left()
        elif cmd == 8:
            pivot_right()
        elif cmd == 0:
            exit_command()  #stop motor movement
            exit(0)         #Exit program
        else:
            print("Invalid command input... ignored.")
        time.sleep(1)

except ValueError:
    print("Oops!  That was not a valid input.")
except:
    print("Unexpected error:", sys.exc_info()[0])
finally:
    print("Goodbye")

#EOF
