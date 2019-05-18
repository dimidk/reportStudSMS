#!/usr/bin/python
#-*-coding: utf-8 -*-

import os
#from urllib import urlopen this for python2.7
from urllib import request
import json
import passwd
import smtplib
from email.mime.text import MIMEText
import email.header
from datetime import datetime
import time
import math
import xlrd
import init
import readIpeuthinoi
from readIpeuthinoi import IpeuthinoiStoixeia


#don't forget to use regular expressions
#what if there are brothers and sisters in school and send info to the same phone number
#test to send email the last week not the last ones

server_host='smtp.gmail.com'
port=465
org_email='@gmail.com'
username=passwd.username+org_email
password=passwd.password
targets=passwd.targets
sender=username



#create a dictionary from every class file
class StudentsStoixeia():
	
	studStoixeia=dict()
	
	def __init__(self,phoneNumber,Surname,Name,tup=''):
		
		self.phoneNumber=phoneNumber
		self.Surname=str(Surname)
		self.Name=str(Name)
		self.tup=tup
		
		key=(self.phoneNumber,self.Surname,self.Name)
		
		if key not in StudentsStoixeia.studStoixeia:
		
			StudentsStoixeia.studStoixeia[key]=[self.tup]
		
#		else: 
				#create a tuple with the name of the second child to father's phone number
#				StudentsStoixeia.studStoixeia[self.phoneNumber].append(self.tup)

	
	
#sent a history request and get a json response
def checkSentAndXml(url):
	
	print ("Get HTTP Request Balance")
	
	response=request.urlopen(url)
	html=response.read()
	print ("OK, request success:",response.getcode())
	response.close()

	return html


def get_datetime():
		
	
	now=datetime.now()
	secs=now.timestamp()
	
	return secs,now


def createFile(filename,smsList):
	
	fp=open(filename,"w")
	for n in smsList:
		fp.write(n['text']+"\n")
	fp.close()
	

#read the xls class file
def readStudStoixeia(filename):
	
	print("process file {}".format(filename))
	
	try:
	
		fp=xlrd.open_workbook(filename,encoding_override="cp1252")
	except:
		print("open file error")

	"""now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':Read Teachers'' file'+filename+' and add to dictionary\n')"""
	
	sheet=fp.sheet_by_index(0)

	for i in range(15,sheet.nrows,1):

		lineList=sheet.row_values(i)
		lineList=[x for x in lineList if x!='']	
		surname=lineList[2].strip()
		name=lineList[3].strip()
		fatherName=lineList[4].strip()
		
		if len(lineList)>6:
			
			phoneNum=lineList[6]
			
			tup=(surname,name)
			s=StudentsStoixeia(phoneNum,surname,name,tup)
		else:
			print("there is no phone for this student {},{}".format(surname,name))

	"""for key,val in TeachersStoxeia.teacherstoixeia.items():
		for k in key:
			print k,
		print "==>",
		for t in val:
			print t,
		print "\n"
	
	print "duplicate names:",TeachersStoixeia.findDupNames"""
	
	
	filename_prc=filename.split('xls')[0]+'prc'
	os.rename(filename,filename_prc)


def createDictionary():
	
	filenames,a=init.findFile(init.tmimataDir,'prc')
	
	for name in filenames:
		
		filename=os.path.join(init.tmimataDir,name)
		if 'xls' not in filename:
			continue
		
		readStudStoixeia(filename)
		sendEMailToClass(smsStudStoixeia_d,smsStudStoixeia_f,filename)
			
		StudentsStoixeia.studStoixeia.clear()
		

#create an sms dictonary with all the smss' delivered or not to students (info from json response)
def createSmsDict(smsStudStoixeia_d,deliveStud):
	
	
	for s in deliveStud:
		keyAdd=(s['to'].lstrip('30'),s['text'].split()[1],s['text'].split()[2])
		
		if keyAdd not in smsStudStoixeia_d:
			tup=(s['text'].split()[1],s['text'].split()[2])
			smsStudStoixeia_d.update({keyAdd:[tup,s['text'],s['timestamp']]})
		else:
			smsStudStoixeia_d[keyAdd].append(s['text']+' '+s['timestamp'])
	
	return smsStudStoixeia_d
	

#combine info from two dictionaries and send an email to teacher about smss'
#also check for brothers and sisters
def sendEMailToClass(smsStudStoixeia_d,smsStudStoixeia_f,filename):
	
	
	currentSecs,currentTime=get_datetime()
	currentSecs=math.modf(currentSecs)[1]
#	print('current seconds time is:{} and in datetime format:{}'.format(currentSecs,currentTime))
	print("reading dictionary file and sms dictionary {}".format(filename))
	
	class_keys=StudentsStoixeia.studStoixeia.keys()
	
	bodytext_deliv="Τα παρακάτω μηνύματα παραδόθηκαν για το τμήμα " + filename+" είναι:\n"
	for key in class_keys:

		if key in smsStudStoixeia_d:
			value=smsStudStoixeia_d[key]
						
#			get a datetime object
			datetimeSent=datetime.strptime(value[2],'%Y-%m-%d %H:%M:%S')
			
#			convert a datetime object to seconds
			secsSent=datetimeSent.timestamp()
			
#			print('sms timestamp in secs:{} and timestamp:{}'.format(secsSent,datetimeSent))
			if secsSent<currentSecs and secsSent>currentSecs - 604800:
		
#				print('timestamp for current time is {} and for time sms sent is {}'.format(datetime.fromtimestamp(currentSecs),datetime.fromtimestamp(secsSent)))
				bodytext_deliv=bodytext_deliv+value[1]+','+value[2]+'\n'
				
	
	bodytext_fail="Τα παρακάτω μηνύματα απέτυχαν για το τμήμα "+filename+" είναι:\n"
	for key,value in smsStudStoixeia_f.items():
		if class_keys.__contains__(key):
			
#			get a datetime object
			datetimeSent=datetime.strptime(value[2],'%Y-%m-%d %H:%M:%S')
			
#			convert a datetime object to seconds
			secsSent=datetimeSent.timestamp()
			
#			print('sms timestamp in secs:{} and timestamp:{}'.format(secsSent,datetimeSent))
			if secsSent<currentSecs and secsSent>currentSecs - 604800:
			
#			timeSent=value[2].split()[0]
				bodytext_fail=bodytext_fail+value[1] + ','+value[2]+'\n'
#			print('sms failed:{} and in datetime format:{}'.format(bodytext_fail,currentTime))
	
	ipeuthinos=filename.split('/')[2].split('.')[0]

	try:
		value=IpeuthinoiStoixeia.ipeuthinoistoixeia[ipeuthinos]
		target=value[1]
		ipeuthinos_name=value[0]
		
		bodytext="Αγαπητέ Συνάδελφε Υπεύθυνος Τμήματος "+ipeuthinos_name+'\n'+bodytext_deliv + bodytext_fail
#		sendEMail(bodytext,target)
		sendEMail(bodytext,"dekadimi@gmail.com")
		
	except:
		print("Cannot find Ipeuthinos Tmimatos for {}".format(filename))
		errormsg="Δεν βρέθηκε ο Υπεύθυνος Τμήματος για το τμήμα "+filename
		sendEMail(errormsg,"dekadimi@gmail.com")
		

def sendEMail(mailSubject,target):
	
	msg=MIMEText(mailSubject)
	msg['Subject']='Absences SMS Information'
	msg['From']=sender
	msg['To']=target
#	msg['To']=', '.join(targets)
	
	print ("prepare sending email")
	server=smtplib.SMTP_SSL(server_host,port)
	server.login(username,password)
	server.sendmail(sender,target,msg.as_string())
	print ("email sent ")
	server.quit()


type_xml='&type=json'

urlcheck_sender=passwd.urlcheckSent+type_xml

print ("Start process for checking balance")
		
html=checkSentAndXml(urlcheck_sender)
data=json.loads(html.decode())
sms=data['sms']
total=data['total']

failed=[subsms for subsms in sms if subsms['status']=='f']
delivered=[subsms for subsms in sms if subsms['status']=='d']
sent=[subsms for subsms in sms if subsms['status']=='s']

deliveStud_start=[subsms for subsms in sms if subsms in delivered and subsms['text'].find('ΑΠΟΥΣ')!=-1]
deliveStud_exception=[subsms for subsms in deliveStud_start if subsms['text'].find('ΕΝΗΜΕΡΩΣΗ ΑΠΟΥΣΙΩΝ')!=-1]
deliveStud=[subsms for subsms in deliveStud_start if subsms not in deliveStud_exception]

failedStud_start=[subsms for subsms in sms if subsms in failed and subsms['text'].find('ΑΠΟΥΣ')!=-1]
failedStud_exception=[subsms for subsms in failedStud_start if subsms['text'].find('ΕΝΗΜΕΡΩΣΗ ΑΠΟΥΣΙΩΝ')!=-1]
failedStud=[subsms for subsms in failedStud_start if subsms not in failedStud_exception]

deliveTeacher=[subsms for subsms in sms if subsms in delivered and subsms['text'].find('Αγαπητέ')!=-1]
deliveRest=[subsms for subsms in sms if subsms in delivered and subsms not in deliveStud]



if __name__=='__main__':
	

	Bodytext=""
	fp=open("deliveStud.txt","w")
	for n in deliveStud:
		#python2.7 need to convert to run fp.write(n['text'].encode('utf-8')+"\n")
		fp.write(n['text']+"\n")
		Bodytext=Bodytext+n['text']+"\n"
	fp.close()


	print (len(delivered)," delivered messages")
	print (len(deliveStud)," delivered to Students")
	print (len(deliveTeacher)," delivered to Teachers")


	#create dictionary for sms key=phoneNumber and value=Surname Name
	smsStudStoixeia_d=dict()
	smsStudStoixeia_d=createSmsDict(smsStudStoixeia_d,deliveStud)

	smsStudStoixeia_f=dict()
	smsStudStoixeia_f=createSmsDict(smsStudStoixeia_f,failedStud)

	readIpeuthinoi.read_files()
	
	print("printing sms dictionary",len(smsStudStoixeia_d))
	print("printing sms dictionary",len(smsStudStoixeia_f))

#sendEMail(Bodytext)

	createDictionary()
	
	print("waiting for 2 secs")
	time.sleep(2)
	print("renaming files")
	files,a=init.findFile(init.ipeuthinoiDir)
	for name in files:
		
		if 'prc' not in name:
			continue
			
		filename=os.path.join(init.ipeuthinoiDir,name)
		init.mvFileToFirstName(filename)
		
	files,a=init.findFile(init.tmimataDir)
	for name in files:
		
		if 'prc' not in name:
			continue
		filename=os.path.join(init.tmimataDir,name)
		init.mvFileToFirstName(filename)
		
	print ("exit process\n")	
	
	

			
		
