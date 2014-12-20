tasters-choice
==============
A python code to access Thomson Reuters' Web of Knowledge API.
Dependencies: multiprocessing, xlrd, xlwt, csv, suds, ElementTree package as well as standard available python 2.7 packages such as urllib2, sqlite3, os, time.
Prerequisites: You must purchase the Web of Knowledge subscription from Thomson Reuters and obtain username/password.
SID numbers must be passed in from auth.py
Template filename must be in the following format. "companyname".xlsx
Main directory with patent numbers is folder_dir = '/Users/James/Documents/'.
The code opens the excel files in the main directory that contain source patent numbers and examines the backward citing 
patents for each source patent.
The backward citing patents' derwent technological classification numbers and their respective
counts will be recorded in the database.
