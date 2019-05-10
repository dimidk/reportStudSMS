#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
import os
import datetime
import string
import init
import xlrd


class IpeuthinoiStoixeia():
	
	"""class which makes a dictionary for teachers
	if there are teachers with the same surname then the first letter of their first name is add to key"""

	ipeuthinoistoixeia=dict()
			
	def __init__(self,Tmima,Surname,Email):
		
		self.Tmima=str(Tmima)
		self.Surname=str(Surname)
		self.Email=str(Email)
		
		
		if (self.Tmima) not in IpeuthinoiStoixeia.ipeuthinoistoixeia:
	
			IpeuthinoiStoixeia.ipeuthinoistoixeia[self.Tmima]=[self.Surname,self.Email]
		else:	print("Error!! Cannot put the same class two times!")



def read_StoixeiaFile(filename):
	
	"""this function read excell file and call a class (TeacherStoixeia) to make a dictionary with this information"""
	

	fp=xlrd.open_workbook(filename,encoding_override="cp1252")
	
	sheet=fp.sheet_by_index(0)

	for i in range(3,sheet.nrows,1):
		
		tmima=sheet.row_values(i)[0]
		surname=sheet.row_values(i)[1].strip()
		email=sheet.row_values(i)[2].strip()
		
#		print(tmima,' ',surname,' ',email)
		
		s=IpeuthinoiStoixeia(tmima,surname,email)
	
	
	"""print ("ipeuthinoi information\n")
	for key,val in IpeuthinoiStoixeia.ipeuthinoistoixeia.items():
		print(key,"==>")
		for t in val:
			print(t)"""
	
	filename_prc=filename.split('xls')[0]+'prc'
	os.rename(filename,filename_prc)
	
	
def read_files():
	
	"""this function checks if there is a file for teachers information"""
	
	filenames,a=init.findFile(init.ipeuthinoiDir,'prc')
	
	for name in filenames:
		
#		print(name)
		filename=os.path.join(init.ipeuthinoiDir,name)
		
#		print(filename)
		if 'xls' not in filename:
			continue
		
		read_StoixeiaFile(filename)
	

	
"""testing purpose"""
#read_files()

