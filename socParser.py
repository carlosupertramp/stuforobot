#!C:\Users\uga04332\AppData\Local\Programs\Python\Python7\python.exe

#
#	Author			: C. B. <ktx@oblab.com>
#	Last Modify		: 2018.August.25 - DS: 77240710
#
#	Interprete		: C:\Users\uga04332\AppData\Local\Programs\Python\Python37\python.exe
#
#   Requiiti		: Installare  mail-parser e ehp tramite pip o da file
#					>> pip install mail-parser
#					>> pip install ehp
#					>> pip install HTMLParser
#					>> pip install future

# Load Library
import io, os
import getopt, sys
import base64, email, re
import mailparser
from HTMLParser import HTMLParser
from html.parser import HTMLParser
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
	global _mdate
	_mdate = email_message.date
	_body = email_message.body
	_id = email_message.message_id
	return _body

def getSocData(bodymessage):
	#dBug("parse this body" + str(bodymessage))
	socParse = Html()
	_socData = socParse.feed(bodymessage)
	dataBlock = ['AL2-KPI']
	dataBlock.append(str(_mdate)) #DataMessaggio
	try:
		for _params in _socData.find('td', ('style', 'font-weight: bold; padding-left: 4px; padding-bottom: 5px;')): #Warning
			dBug("Params: >>" + _params.text())
			dataBlock.append(int(_params.text()))
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
			dataBlock.append(int(_severe.text()))
		if len(dataBlock) < 17:
			print("Exception: Numero dati non completo < 17")
			return False
		if dataBlock[13] < 100000:
			print("Warning: potenziale problema nella raccolta dati il numero LOGS troppo basso < 100.000")
			return False
	except:
		print("Exception: Alcuni elementi non sono numeri interi.")
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
		f = open("soccsv.csv", "w")
		datawrite = getSocData(parseThis(fullfilename))
		dBug(datawrite)
		try:
			f.write(str(datawrite[0]) + ";" + str(datawrite[1]) + ";" + str(datawrite[2]) + ";" + str(datawrite[3]) + ";" + str(datawrite[4]) + ";" + str(datawrite[5]) + ";" + \
		     		str(datawrite[6]) + ";" + str(datawrite[7]) + ";" + str(datawrite[8]) + ";" + str(datawrite[9]) + ";" + str(datawrite[10]) + ";" + str(datawrite[11]) + ";" + \
			    	str(datawrite[12]) + ";" + str(datawrite[13]) + ";" + str(datawrite[14]) + ";" + str(datawrite[15]) + ";" + str(datawrite[16]) )
		except:
			f.write("PROBLEMA NEL RECUPERARE I DATI DALLA EMAIL")
			f.close()

main(sys.argv)