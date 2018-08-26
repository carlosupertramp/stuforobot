#!C:\Users\uga04332\AppData\Local\Programs\Python\Python37\python.exe

#
#	Author			: Carlo B. <ktx@oblab.com>
#	Last Modify		: 2018.August.25 - DA: -304357.8196347032
#
#	Interprete		: 
#
#   Requiiti		: Installare  mail-parser e ehp tramite pip o da file
#					>> pip install mail-parser
#					>> pip install ehp
#

# Load Library
import io, os
import getopt, sys
import base64, email, re
import mailparser
from HTMLParser import HTMLParser
from ehp import *
from cgitb import html

# -------------------------------------
global _debug
_debug = 0
# -------------------------------------

def helpMe():
	print("--- Need Help ? ---")
	print("--> example ./soc_parser.py c:\\temp\\myfilehtml.txt")

def dBug(T):
	if _debug == 1:
		print(">>" + str(T))

def openEr(path, flags='rb'):
	fileObj = io.open(path, flags, buffering=0, encoding=None, errors=None, newline=None)
	streamTxt = fileObj.read()
	fileObj.close()
	return streamTxt

def parseThis(fullfilename):
	myStream = openEr(fullfilename)
	email_message = mailparser.parse_from_string(myStream)
	_mdate = email_message.date
	_body = email_message.body
	_id = email_message.message_id
	return _body

def getSocData(bodymessage):
	#dBug("parse this body" + str(bodymessage))
	socParse = Html()
	_socData = socParse.feed(bodymessage)
	dataBlock = ['AL2-KPI']
#	for j in _socData.find('td', ('style', 'font-weight: bold; padding-left: 4px; padding-bottom: 5px;')):
#	for b1 in _socData.find('td', ('style', 'padding-right: 5px; ')):
#		dBug("blocco 1>> " + b1.text())
#	for b2 in _socData.find('td', ('style', 'font-weight: bold; padding-left: 4px; padding-bottom: 5px;')):
#		dBug("blocco 2>> " + b2.text())
#	for b3 in _socData.find('span', ('class', 'HomePageText')): #Titoli
#		dBug("blocco 3>> " + b3.text())
	try:
		for _logs in _socData.find('span', ('id', 'ctl00_cph_lLogsReceivedNum')): #Logs
			dBug("Logs: >>" + _logs.text())
			dataBlock.append(int(_logs.text()))
		for _analyzed in _socData.find('span', ('id', 'ctl00_cph_lIncidentsAnalyzedNum')): #Analyzed
			dBug("Analyzed: >>" + _analyzed.text())
			dataBlock.append(int(_analyzed.text()))
		for _validated in _socData.find('span', ('id', 'ctl00_cph_lIncidentsValidatedNum')): #Validated
			dBug("Validated: >>" + _validated.text())
			dataBlock.append(int(_validated.text()))
		for _severe in _socData.find('span', ('id', 'ctl00_cph_lSevereIncidentsNum')): #Sever
			dBug("Severe: >>" + _severe.text())
		
		dataBlock.append(0) # Emergency

		for _params in _socData.find('div', ('style', 'font-weight: bold; padding-bottom: 4px; margin-top: 10px;')): #Warning
			_params = _params.text()
			_params = _params[-1]
			dataBlock.append(int(_params))
		if len(dataBlock) < 8:
			print "Exception: Numero dati non completo < 8"
			return False
		if dataBlock[1] < 100000:
			print "Warning: potenziale problema nella raccolta dati il numero LOGS troppo basso < 100.000"
			return False
	except:
		print "Exception: Alcuni elementi non sono numeri interi."
		return False

	socParse.close()
	return dataBlock

# +-------------------------------------------------------+
# |                                              MAIN <<<<|
# +-------------------------------------------------------+

def main(opts):
	if len(opts) <= 1:
			helpMe()
			sys.exit(2)
	else:
		fullfilename = opts[1]
		print getSocData(parseThis(fullfilename))
	
main(sys.argv)
