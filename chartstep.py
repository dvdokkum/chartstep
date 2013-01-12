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

Stepper=InstrumentControl.StepperMotor('/dev/tty.usbmodem1411')

### PROGRAM LOOP ###

while 1:

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
		if domain == 'status.chartbeat.net':
			angle = ((current / max) * 120) + 30
		else:
			angle = ((current / (max - min)) * 120) + 30
		
		#print "30 day max is: " + str(max)
		#print "30 day min is: " + str(min)
		#print "currently: " + str(current)
		
		steps = (angle * 800) // 180

		print str(angle) + " degrees"
		return steps
	
### API LIVE LOOP ###
	
	try:
		Stepper.SetPosition(1,1,4800)
		while 1:
			Stepper.SetPosition(1,1,getSteps(domain))
			time.sleep(5)
	
	except: KeyboardInterrupt
	print("Quiting...")
	print("")
	


