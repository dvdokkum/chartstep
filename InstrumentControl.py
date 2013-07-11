#!/usr/bin/python
# Filename: InstrumentControl.py
version = '1.3'

#serialArduino is a modified python serial module which disables the dtrState preventing
#resets when the serial session is closed.
#http://www.arduino.cc/cgi-bin/yabb2/YaBB.pl?num=1274205532

#Code adapted from Dan Thompson and build-in Arduino examples
#http://danthompsonsblog.blogspot.com/2009/04/python-arduino-motor-shield-stepper.html
#and
#http://danthompsonsblog.blogspot.com/2008/09/easydriver-v31-tutorial.html

import serialArduino
import time

print 'Loading InstrumentControl v'+ version

def help():
	print 'InstrumentControl.py currently supports:'
	print 'Stepper Motor Control'

class StepperMotor:
    def __init__(self, StepperMotorAddress):
        self.StepperMotorAddress = StepperMotorAddress
        self.StepperMotor = serialArduino.Serial(StepperMotorAddress, 115200, timeout=0.25)
        print "StepperMotor: Serial Communication Open" 
        time.sleep(1)
    def CloseSerial(self):
        #Close Serial Port
        self.StepperMotor.close()
        print "StepperMotor: Serial Communication Closed"  
        return
    def SetDelay(self,speed):
      if speed < 100 or speed > 65535:
        print "invalid speed"
        return

      binary = DecimalToBinary(speed)
      numBytes = BinaryCount(binary)
      self.StepperMotor.write(chr(14))
      #Note: The 2 in (0,2,1) allows for the transmission of two bytes.
      for i in range(0,2,1):
          sBinary = str(binary)
          firstByte = int(sBinary,2) & int('11111111',2)
          newBinary = int(sBinary,2) >> 8
          binary = DecimalToBinary(newBinary)
          self.StepperMotor.write(chr(firstByte))
      #time.sleep(1)
      return speed

    def SetPosition(self,num,degsPerStepFloat,stepsFloat):
       steps = int(stepsFloat / degsPerStepFloat)
       if(steps < 65535 and steps > -1):
               binary = DecimalToBinary(steps)
               numBytes = BinaryCount(binary)
               self.StepperMotor.write(chr(255))
               #Note: The 2 in (0,2,1) allows for the transmission of two bytes.
               for i in range(0,2,1):
                       sBinary = str(binary)
                       firstByte = int(sBinary,2) & int('11111111',2)
                       newBinary = int(sBinary,2) >> 8
                       binary = DecimalToBinary(newBinary)
                       self.StepperMotor.write(chr(firstByte))
       if(steps > -65535 and steps < 0):
               stepsNeg = steps * -1
               binary = DecimalToBinary(stepsNeg)
               numBytes = BinaryCount(binary)
               self.StepperMotor.write(chr(220))
               #Note: The 2 in (0,2,1) allows for the transmission of two bytes.
               for i in range(0,2,1):
                       sBinary = str(binary)
                       firstByte = int(sBinary,2) & int('11111111',2)
                       newBinary = int(sBinary,2) >> 8
                       binary = DecimalToBinary(newBinary)
                       self.StepperMotor.write(chr(firstByte))
       #time.sleep(1)
       return stepsFloat
    def GetPosition(self):
        self.StepperMotor.write(chr(5)+chr(0)+chr(0))
        time.sleep(1)
        StepperPosition=self.StepperMotor.readline()
        return StepperPosition
    def GetVersion(self):
        self.StepperMotor.write(chr(118)+chr(0)+chr(0))
        time.sleep(1)
        FirmwareVersion=self.StepperMotor.readline()
        return FirmwareVersion

#Convert integer n (base 10) to a binary string (base 2)
def DecimalToBinary(n):
   if n < 0: raise ValueError, "must be a positive integer"
   BinaryString=bin(n)[2:]
   return BinaryString

#Returns the number of bit bytes (eighths) in binary string. Rounds up.
def BinaryCount(number):
    sNumber = str(number)
    length = len(sNumber)
    numBytes = length / 8.0
    numBytesInt = length / 8
    if numBytes > numBytesInt:
        return numBytesInt + 1
    else:
        return numBytesInt

# End of InstrumentControl.py