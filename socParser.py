#!C:\Users\uga04332\AppData\Local\Programs\Python\Python37\python.exe

#
#	Author			: C. Balbo <carlo.balbo@unipolsai.it>
#	Last Modify		: 2018.August.23 - DA: -304357.8196347032
#
#	Interprete		: C:\Users\uga04332\AppData\Local\Programs\Python\Python37\python.exe
#
#   Requirements	: Installare  mail-parser tramite pip e ehp
#					>> pip install mail-parser
#					>> pip install ehp


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
_debug = 1
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
	dataBlock = ['record']
#	for j in _socData.find('td', ('style', 'font-weight: bold; padding-left: 4px; padding-bottom: 5px;')):
	for b1 in _socData.find('td', ('style', 'padding-right: 5px; ')):
		print("blocco 1>> " + b1.text())
	for b2 in _socData.find('td', ('style', 'font-weight: bold; padding-left: 4px; padding-bottom: 5px;')):
		print("blocco 2>> " + b2.text())
	for b3 in _socData.find('span', ('class', 'HomePageText')): #Titoli
		print("blocco 3>> " + b3.text())
	for _logs in _socData.find('span', ('id', 'ctl00_cph_lLogsReceivedNum')): #Logs
		print("Logs: >>" + _logs.text())
		dataBlock.append(_logs.text())
	for _analyzed in _socData.find('span', ('id', 'ctl00_cph_lIncidentsAnalyzedNum')): #Analyzed
		print("Analyzed: >>" + _analyzed.text())
	for _validated in _socData.find('span', ('id', 'ctl00_cph_lIncidentsValidatedNum')): #Validated
		print("Validated: >>" + _validated.text())
	for _severe in _socData.find('span', ('id', 'ctl00_cph_lSevereIncidentsNum')): #Sever
		print("Severe: >>" + _severe.text())
	dataBlock.append('0')
	for _params in _socData.find('div', ('style', 'font-weight: bold; padding-bottom: 4px; margin-top: 10px;')): #Warning
		_params = _params.text()
		_params = _params[-1]
		print("dataIn: >>" + _params)
		dataBlock.append(_params)

	print(dataBlock)
	socParse.close()

# +-------------------------------------------------------+
# |                                              MAIN <<<<|
# +-------------------------------------------------------+

def main(opts):
	if len(opts) <= 1:
			helpMe()
			sys.exit(2)
	else:
		fullfilename = opts[1]
		getSocData(parseThis(fullfilename))
	
main(sys.argv)
