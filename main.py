# ////////////////////////////////////////////////////////////////
# //                     IMPORT STATEMENTS                      //
# ////////////////////////////////////////////////////////////////
import math
import sys
import time
import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.animation import Animation
from functools import partial
from kivy.config import Config
from kivy.core.window import Window
from pidev.kivy import DPEAButton
from pidev.kivy import PauseScreen
from time import sleep
from dpeaDPi.DPiComputer import *
from dpeaDPi.DPiStepper import *
from kivy.config import Config
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')
setStaircaseSpeed = 0
setRampSpeed = 0
# ////////////////////////////////////////////////////////////////
# //                     HARDWARE SETUP                         //
# ////////////////////////////////////////////////////////////////
"""Stepper Motor goes into MOTOR 0 )
    Limit Switch associated with Stepper Motor goes into HOME 0
    One Sensor goes into IN 0
    Another Sensor goes into IN 1
    Servo Motor associated with the Gate goes into SERVO 1
    Motor Controller for DC Motor associated with the Stairs goes into SERVO 0"""


# ////////////////////////////////////////////////////////////////
# //                      GLOBAL VARIABLES                      //
# //                         CONSTANTS                          //
# ////////////////////////////////////////////////////////////////
ON = False
OFF = True
HOME = True
TOP = False
OPEN = False
CLOSE = True
YELLOW = .180, 0.188, 0.980, 1
BLUE = 0.917, 0.796, 0.380, 1
DEBOUNCE = 0.1
INIT_RAMP_SPEED = 2
RAMP_LENGTH = 725
dpiStepper = DPiStepper()
stepper_num = 0
steps = 1600
microstepping = 8
wait_to_finish_moving_flg = True
stepperStatus = dpiStepper.getStepperStatus(0)
gear_ratio = 1
motorStepPerRevolution = 1600 * gear_ratio
dpiStepper.setStepsPerRevolution(stepper_num, motorStepPerRevolution)
speed_in_revolutions_per_sec = 10.0
accel_in_revolutions_per_sec_per_sec = 2.0
dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)
dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(stepper_num, accel_in_revolutions_per_sec_per_sec)

dpiComputer = DPiComputer()
dpiComputer.initialize()

dpiStepper.setMicrostepping(microstepping)
speed_steps_per_second = 200 * microstepping * 70
accel_steps_per_second_per_second = speed_steps_per_second
dpiStepper.setSpeedInStepsPerSecond(0, speed_steps_per_second)

dpiStepper.setAccelerationInStepsPerSecondPerSecond(0, accel_steps_per_second_per_second)

dpiStepper.setBoardNumber(0)
directionToMoveTowardHome = 1  # 1 Positive Direction -1 Negative Direction
homeSpeedInStepsPerSecond = speed_steps_per_second / 2
homeMaxDistanceToMoveInSteps = 9000


# ////////////////////////////////////////////////////////////////
# //            DECLARE APP CLASS AND SCREENMANAGER             //
# //                     LOAD KIVY FILE                         //
# ////////////////////////////////////////////////////////////////
class MyApp(App):
    def build(self):
        self.title = "Perpetual Motion"
        return sm

Builder.load_file('main.kv')
Window.clearcolor = (.1, .1,.1, 1) # (WHITE)



# ////////////////////////////////////////////////////////////////
# //                    SLUSH/HARDWARE SETUP                    //
# ////////////////////////////////////////////////////////////////
sm = ScreenManager()

# ////////////////////////////////////////////////////////////////
# //                       MAIN FUNCTIONS                       //
# //             SHOULD INTERACT DIRECTLY WITH HARDWARE         //
# ////////////////////////////////////////////////////////////////
	
# ////////////////////////////////////////////////////////////////
# //        DEFINE MAINSCREEN CLASS THAT KIVY RECOGNIZES        //
# //                                                            //
# //   KIVY UI CAN INTERACT DIRECTLY W/ THE FUNCTIONS DEFINED   //
# //     CORRESPONDS TO BUTTON/SLIDER/WIDGET "on_release"       //
# //                                                            //
# //   SHOULD REFERENCE MAIN FUNCTIONS WITHIN THESE FUNCTIONS   //
# //      SHOULD NOT INTERACT DIRECTLY WITH THE HARDWARE        //
# ////////////////////////////////////////////////////////////////

class MainScreen(Screen):

    staircaseSpeedText = '0'
    rampSpeed = INIT_RAMP_SPEED
    staircaseSpeed = 40




    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.initialize()

    def toggleGate(self):
        print("Open and Close gate here")
        #controlled by open gate button
       #on a servo motor
        if self.ids.gate.text == 'Open Gate':
            self.ids.gate.text = 'Close Gate'
            self.ids.gate.color = 0, 1, 0, 1

            print("Servo example:")
            print("  Rotate Servo 0 CW")
            servo_number = 0
            for i in range(1):
                dpiComputer.writeServo(servo_number, 90)
                sleep(1)
                dpiComputer.writeServo(servo_number, 0)
                dpiStepper.enableMotors(False)

        else:
            sleep(2)
            self.ids.gate.text = 'Open Gate'
            self.ids.gate.color = 0, 0, 0, 0


    def toggleStaircase(self,*args):
        print("Turn on and off staircase here")
        #Controlled by Staircase on Button
        #on servo motor
        global setStaircaseSpeed
        # if self.ids.staircase.text = 'Staircase Off':
        # self.ids.staircase.text = 'Staircase On'
        # self.ids.staircase.color = 0, 1, 0, 1
        # print("staircase button change")





        #servo_number = 1

        #self.ids.staircase.text = 'Staircase Off'
        #self.ids.staircase.color = 0, 1, 0, 1
        #print("staircase button change")
        #sleep(2)

        #print(setStaircaseSpeed)
        #dpiComputer.writeServo(servo_number, setStaircaseSpeed)
        #sleep(7)
        #dpiComputer.writeServo(servo_number, 91)
        #dpiStepper.enableMotors(False)
        #print("motor ran at modulated speed for 30 seconds the stopped")


        #sleep(2)
        #self.ids.staircase.text = 'Staircase On'
        #self.ids.staircase.color = 0, 0, 0, 0
        #dpiComputer.writeServo(servo_number, 91)
        #print("button reset")







        if self.ids.staircase.text == 'Staircase Off':
            self.ids.staircase.text = 'Staircase On'
            self.ids.staircase.color = 0, 1, 0, 1
            print("staircase button change")


            servo_number = 1
            for i in range(1):
                print(setStaircaseSpeed)
                dpiComputer.writeServo(servo_number, setStaircaseSpeed)
                sleep(7)
                dpiComputer.writeServo(servo_number, 91)
                dpiStepper.enableMotors(False)
            print("motor ran at modulated speed for 30 seconds the stopped")
        else:
            sleep(2)
            servo_number = 1
            self.ids.staircase.text = 'Staircase On'
            self.ids.staircase.text = 'Staircase Off'
            self.ids.staircase.color = 0, 0, 0, 0
            dpiComputer.writeServo(servo_number, 91)
            print("button reset")



    def toggleRamp(self):
        print("Move ramp up and down here")
        #contorlled ny Ramp to Top button
        if self.ids.ramp.text == 'Ramp to Top':
            self.ids.ramp.text = 'Stop Ramp'
            self.ids.ramp.color = 0, 1, 0, 1
            dpiStepper.enableMotors(True)

            currentPosition = dpiStepper.getCurrentPositionInSteps(0)[1]
            print(f"Pos = {currentPosition}")

            speed_steps_per_second = 200 * microstepping * setRampSpeed
            accel_steps_per_second_per_second = speed_steps_per_second
            dpiStepper.setSpeedInStepsPerSecond(0, speed_steps_per_second)

            dpiStepper.setAccelerationInStepsPerSecondPerSecond(0, accel_steps_per_second_per_second)

            dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)
            waitToFinishFlg = True
            dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, -28.5, waitToFinishFlg)
            sleep(1)
            #dpiStepper.moveToHomeInSteps(stepper_num, self.directionToMoveTowardHome, self.homeSpeedInStepsPerSecond, self.homeMaxDistanceToMoveInSteps)
            dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)
            waitToFinishFlg = True
            dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 28.5, waitToFinishFlg)
            dpiStepper.enableMotors(False)


        else:
            sleep(2)
            self.ids.ramp.text = 'Ramp to Top'
            self.ids.ramp.color = 0, 0, 0, 0
            dpiStepper.enableMotors(False)

    def auto(self):
        print("Run through one cycle of the perpetual motion machine")
        # put all other functions in circuit here
        global setStaircaseSpeed
        if self.ids.auto.text == 'Start':
            self.ids.auto.text = 'Stop'
            self.ids.auto.color = 0, 1, 0, 1
            dpiStepper.enableMotors(True)




            currentPosition = dpiStepper.getCurrentPositionInSteps(0)[1]
            print(f"Pos = {currentPosition}")

            dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)
            waitToFinishFlg = True
            dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, -28.5, waitToFinishFlg)
            sleep(.4)

            servo_number = 1
            for i in range(1):
                dpiComputer.writeServo(servo_number, setStaircaseSpeed)
                sleep(8)
                dpiComputer.writeServo(servo_number, 90)
                
            dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)
            waitToFinishFlg = True
            dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 28.5, waitToFinishFlg)
            sleep(.25)
            dpiStepper.enableMotors(False)

            sleep(.03)

            servo_number = 0
            for i in range(1):
                dpiComputer.writeServo(servo_number, 90)
                sleep(1)
                dpiComputer.writeServo(servo_number, 0)
        else:
            sleep(2)
            self.ids.auto.text = 'Start'
            self.ids.auto.color = 0, 0, 0, 0
            dpiStepper.enableMotors(False)
    def setRampSpeed(self, *args):
        print("Set the ramp speed and update slider text")
        #Controlled by ramp speed slider

        global setRampSpeed
        print(args[0])
        sleep(2)
        for i in range(1):
            ramp_text = "Speed of ramp in RPS "
            ramp_text_number = str(args[0])
            rampSpeedLabel = ramp_text + ramp_text_number
            self.ids.rampSpeedLabel.text = rampSpeedLabel
            print("Slider Updated")
            print(rampSpeedLabel)


        speed_in_revolutions_per_sec_per_second = 200 * microstepping * self.ids.rampSpeed.value
        accel_steps_per_second_per_second = speed_in_revolutions_per_sec_per_second
        dpiStepper.setAccelerationInStepsPerSecondPerSecond(0, accel_steps_per_second_per_second)
        dpiStepper.setAccelerationInStepsPerSecondPerSecond(1, accel_steps_per_second_per_second)


    def setStaircaseSpeed(self, *args):
        global setStaircaseSpeed
        print(args[0])
        sleep(2)
        setStaircaseSpeed = args[0]
        for i in range(1):
            staircase_text = "Speed of staircase in RPS "
            staircase_text_number = str(args[0])
            staircaseSpeedLabel = staircase_text + staircase_text_number
            self.ids.staircaseSpeedLabel.text = staircaseSpeedLabel

            #setStaircaseSpeed = self.ids.staircaseSpeed.value
            #setStaircaseSpeed = args[0]
            print("Slider Updated")
            print(staircaseSpeedLabel)




    def initialize(self):
        print("Close gate, stop staircase and home ramp here")
        dpiStepper.moveToHomeInSteps(stepper_num, directionToMoveTowardHome, homeSpeedInStepsPerSecond,homeMaxDistanceToMoveInSteps)
        sleep(0.05)
        dpiStepper.enableMotors(False)


    def resetColors(self):
        self.ids.gate.color = YELLOW
        self.ids.staircase.color = YELLOW
        self.ids.ramp.color = YELLOW
        self.ids.auto.color = BLUE
    
    def quit(self):
        print("Exit")
        MyApp().stop()

sm.add_widget(MainScreen(name = 'main'))

# ////////////////////////////////////////////////////////////////
# //                          RUN APP                           //
# ////////////////////////////////////////////////////////////////

MyApp().run()
