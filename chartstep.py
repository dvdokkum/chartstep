#imports
from __future__ import division
import InstrumentControl
import urllib2
import json 
import time
import signal 
import sys

#ENTER API KEY HERE#
APIkey = ""

#initiate Arduino connection

Stepper=InstrumentControl.StepperMotor('/dev/tty.usbmodem1411') #change this to your Arduino address

#speed settings
fast = 200
slow = 9000

### PROGRAM LOOP ###

while 1:
	Stepper.SetDelay(fast)
	Stepper.SetPosition(1,1,0)
	print("")
	print("What domain?")
	print("(Input 'cbtotal' for Chartbeat stats)")
	print("")
	
	domain = raw_input()
	if domain == 'cbtotal':
		domain = 'status.chartbeat.net'
	
	print("")
	print("Got it.... " + domain)
	print("")
	print("Running....")
	print("Press Control-C to Stop")
	print("")
	
	#getSteps for domain, print Angle#
	
	def getSteps(domain):
		
		timestamp = int(time.time())
		
		if domain == 'status.chartbeat.net':
			
			#cbtotal API
			APIquickstat = "http://chartbeat.com/api/cbtotal"
			json1 = urllib2.urlopen(APIquickstat).read()
			quickstat = json.loads(json1)
			current = quickstat['total']
	
		else:
			
			# Chartbeat API URLs
			APIquickstat = "http://api.chartbeat.com/live/quickstats/v3/?apikey=" + APIkey + "&host=" + domain
			json1 = urllib2.urlopen(APIquickstat).read()
			quickstat = json.loads(json1)
			current = quickstat['people']
	
		APIhistorical = "http://api.chartbeat.com/historical/traffic/stats/?apikey=" + APIkey + "&host=" + domain + "&end=" + 	str(timestamp) + "&properties=max,min"
	
			# Reading JSON data
	
		json2 = urllib2.urlopen(APIhistorical).read()
		
		historical = json.loads(json2)
		max = historical['data'][domain]['people']['max']
		min = historical['data'][domain]['people']['min']
	
		#angle formula
		angle = ((current / max) * 120)
		
		#print "30 day max is: " + str(max)
		#print "30 day min is: " + str(min)
		#print "currently: " + str(current)
		
		steps = (angle * 533.333333) // 120

		print str(angle) + " degrees"
		#print steps
		return steps
	
### API LIVE LOOP ###
	
	try:
		goSteps = getSteps(domain)+4800
		Stepper.SetDelay(fast)
		Stepper.SetPosition(1,1,4800)
		Stepper.SetDelay(slow)
		Stepper.SetPosition(1,1,goSteps)

		while 1:
			time.sleep(5)
			Stepper.SetPosition(1,1,getSteps(domain) + 4800)
	
	except: KeyboardInterrupt
	print("Quiting...")
	print("")
	


