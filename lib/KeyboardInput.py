#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import avango.daemon
import time

class KeyboardInput(avango.script.Script):

    ## input fields
    sf_button0 = avango.SFBool()
    sf_button1 = avango.SFBool()
    sf_button2 = avango.SFBool()
    sf_button3 = avango.SFBool()
    sf_button4 = avango.SFBool()
    sf_button5 = avango.SFBool()
    sf_button6 = avango.SFBool()

    ## output fields 
    sf_rot_input0 = avango.SFFloat()
    sf_rot_input1 = avango.SFFloat()
    sf_rot_input2 = avango.SFFloat()    

    sf_max_fps = avango.SFFloat()
    sf_max_fps.value = 60.0 # initial value
        
    ## constructor
    def __init__(self):
        self.super(KeyboardInput).__init__()
   
        ### parameters ###
        self.rot_velocity = 2.0 # in degrees/sec
        
        ### variables ###
        self.lf_time = time.time() # absolute time of last frame
        
        ## init sensor
        self.keyboard_sensor = avango.daemon.nodes.DeviceSensor(
            DeviceService = avango.daemon.DeviceService())
        self.keyboard_sensor.Station.value = "gua-device-keyboard"

        ## init field connections
        self.sf_button0.connect_from(self.keyboard_sensor.Button4) # left arrow key
        self.sf_button1.connect_from(self.keyboard_sensor.Button5) # right arrow key
        self.sf_button2.connect_from(self.keyboard_sensor.Button6) # up arrow key
        self.sf_button3.connect_from(self.keyboard_sensor.Button7) # down arrow key                
        self.sf_button4.connect_from(self.keyboard_sensor.Button10) # page up
        self.sf_button5.connect_from(self.keyboard_sensor.Button11) # page down        
        self.sf_button6.connect_from(self.keyboard_sensor.Button15) # left ctrl key        
   
   
        ## set global evaluate policy
        self.always_evaluate(True)

    @field_has_changed(sf_button6) # evaluated if this field has changed
    def sf_button6_changed(self):
    
        if self.sf_button6.value == True: # key pressed
            
            if self.sf_max_fps.value == 60.0:
                self.sf_max_fps.value = 20.0 # set slow application/render framerate
                print("slow:", self.sf_max_fps.value, "FPS")
            else:
                self.sf_max_fps.value = 60.0 # set fast application/render framerate
                print("fast:", self.sf_max_fps.value, "FPS")

    def evaluate(self): # evaluated every frame if any input field has changed  
        # frame independent animation
        now = time.time()
        diff = now - self.lf_time
        self.lf_time = now
        print(self.sf_button0.value)
        ## get rot_value0
        if self.sf_button0.value == True:
            self.sf_rot_input0.value = - diff * self.rot_velocity
        elif self.sf_button1.value == True:
            self.sf_rot_input0.value = diff * self.rot_velocity
        else:
            self.sf_rot_input0.value = 0
        ## get rot_value1
        if self.sf_button2.value == True:
            self.sf_rot_input1.value = - diff * self.rot_velocity
        elif self.sf_button3.value == True:
            self.sf_rot_input1.value = diff * self.rot_velocity
        else:
            self.sf_rot_input0.value = 0
        ## get rot_value2
        if self.sf_button4.value == True:
            self.sf_rot_input2.value = - diff * self.rot_velocity
        elif self.sf_button5.value == True:
            self.sf_rot_input2.value = diff * self.rot_velocity
        else:
            self.sf_rot_input0.value = 0