# http://www.codingwithruss.com/pygame/how-to-use-joysticks-in-pygame/
import pygame
import pymavlink.dialects.v20.standard as mav
import struct
import typing
import struct
import typing
from pymavlink import mavutil
import time
from paho.mqtt import client as mqtt_client

target_system = 1
target_component = 1

def generateCommandLong(command, param1, param2):
  mavlink = mav.MAVLink(None,target_system,target_component)
  #target_system: int, target_component: int, command: int, confirmation: int, param1: float, param2: float, param3: float, param4: float, param5: float, param6: float, param7: float
  mav_msg = mavlink.command_long_encode(target_system, target_component, command, 0, param1, param2,0,0,0,0,0)
  return mav_msg.pack(mavlink)

def generateRCChannelsOverride(chan1_raw, chan3_raw, chan4_raw):
  mavlink = mav.MAVLink(None,target_system,target_component)
  #target_system: int, target_component: int, chan1_raw: int, chan2_raw: int, chan3_raw: int, chan4_raw: int, chan5_raw: int, chan6_raw: int, chan7_raw: int, chan8_raw: int, chan9_raw: int = 0, chan10_raw: int = 0, chan11_raw: int = 0, chan12_raw: int = 0, chan13_raw: int = 0, chan14_raw: int = 0, chan15_raw: int = 0, chan16_raw: int = 0, chan17_raw: int = 0, chan18_raw: int = 0
  mav_msg = mavlink.rc_channels_override_encode(target_system, target_component, chan1_raw, 0, chan3_raw, chan4_raw,0,0,0,0)
  return mav_msg.pack(mavlink)

def main():
  broker = '192.168.0.2'
  port = 1883
  topic = '/Mobius/KETI_GCS/GCS_Data/2001/orig'

  client = mqtt_client.Client()
  client.connect(broker, port)
  client.loop_start()

  pygame.init()

  #initialise the joystick module
  pygame.joystick.init()

  #create empty list to store joysticks
  joysticks = []

  #game loop
  run = True
  while run:

    #event handler
    for event in pygame.event.get():
      if event.type == pygame.JOYDEVICEADDED:
        joy = pygame.joystick.Joystick(event.device_index)
        joysticks.append(joy)
      #quit program
      elif event.type == pygame.QUIT:
        run = False
      elif event.type == pygame.JOYBUTTONDOWN:
        button = event.button
        command = 0
        param1 = 0
        param2 = 0
        if button == 2:
          command = mav.MAV_CMD_DO_SET_MODE
          param2 = 0
        elif button == 3:
          command = mav.MAV_CMD_DO_SET_MODE
          param2 = 1
        elif button == 1:
          command = mav.MAV_CMD_DO_SET_MODE
          param2 = 2
        elif button == 5:
          command = mav.MAV_CMD_USER_1
          param1 = 170
        else:
          continue
        mavmsg = generateCommandLong(command, param1, param2)
        print(client.publish(topic, mavmsg))
        print(mavmsg)
        
    for joystick in joysticks:
      threshold = 0.05
      forward = joystick.get_axis(3)
      side = joystick.get_axis(2)
      yaw = joystick.get_axis(0)
      #print(yaw, forward, side)
      if abs(forward) < threshold:
        forward = 0
      if abs(side) < threshold:
        side = 0
      if abs(yaw) < threshold:
        yaw = 0
      #print(yaw, forward, side)
      chan1_raw = int(yaw * 500 + 1500)
      chan3_raw = int(-forward * 500 + 1495)
      chan4_raw = int(side * 500 + 1500)      
      mavmsg = generateRCChannelsOverride(chan1_raw, chan3_raw, chan4_raw)
      #print(chan1_raw, chan3_raw, chan4_raw)
      client.publish(topic, mavmsg)
      #print(mavmsg)

    time.sleep(1/10)

if __name__ == "__main__":
  main()
  pygame.quit()
