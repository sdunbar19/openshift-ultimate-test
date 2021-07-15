#################################################################################################
# Script name          	: index.py
# Script author		: Sarah Dunbar														#
# Script creation date 	: 06/14/21
# Last modified: 	: 07/14/21																#
# Script description   	: Runs the website containing the desired information	#
#################################################################################################

## Imports
import sys
import json
import numpy
import datetime
import time

from python.maxDateWrapper import tabTupsToDict
from python.colorDictHelper import makeColorDict
from fileLoader import getAllInfoDict, refresh, refreshSpecific

from flask import Flask, session, render_template, request, send_file, redirect
from flask_session import Session

## Sessions
# Note we are using sessions instead of globals
# This makes our code thread and process safe 
# (every thread and process will use the same variables and won't interfere)
application = Flask(__name__)
SESSION_TYPE = 'filesystem'
application.config.from_object(__name__)
Session(application)

## Webpage functions
# Code for the landing page of the website, containing choice of database
@application.route('/')
def landing():
	session['infoDict'] = json.dumps(getAllInfoDict())
	session['database'] = 'Unknown'
	session['serverID'] = 'Unknown'
	session['server'] = 'Unknown'
	session['table'] = 'Unknown'
	session['columns'] = 'Unknown'
	session['colorDict'] = 'Unknown'
	session['refreshTab'] = 'False'
	session['refreshAll'] = 'False'

	return render_template('landing.html', infoDict=json.loads(session['infoDict']))


# Code for help pdf link
@application.route('/show/help-pdf/')
def showHelpPdf():
	return send_file('static/help.pdf', attachment_filename='help.pdf')

# Code for the loading page when 'Refresh all' clicked
@application.route('/refreshAll/')
def refreshAll():
	infoDict = json.loads(session['infoDict'])
	return render_template('refreshLoadingPage.html', infoDict=infoDict)

# Code for the results page when 'Refresh all' clicked
@application.route('/refreshResults/')
def refreshAllResults():

	global accInstr
	global columnsDict

	refresh()
	session['infoDict'] = json.dumps(getAllInfoDict())

	return render_template('refreshLanding.html', infoDict=json.loads(session['infoDict']))

# Code for the table production
@application.route('/loading/<database>/<server>/<refresh>', methods=['GET'])
def selectedServer(database, server, refresh):

	infoDict = json.loads(session['infoDict'])
	possibleLink = infoDict[database][server]

	# If it's a link, don't set anything
	if type(possibleLink) == str:
		return render_template('externalRedirect.html', link=possibleLink)

	session['server'] = server
	session['database'] = database
	session['refreshTab'] = refresh

	# Directs you to the loading screen until everything is loaded in loadPage()
	return render_template('loadingPage.html', infoDict=infoDict)


# Code for the loading resolution (tables and searchbar)
@application.route('/results', methods=['GET']) 
def loadPage():

	if session['refreshTab'] == 'True':

		refreshSpecific(session['database'], session['server'])
		session['infoDict'] = json.dumps(getAllInfoDict())
		session['refreshTab'] = 'False'


	# Find tuple of (date, table) for all valid tables
	columns, ptList, finalTuples, schema, sysDate, irregTimesDict = json.loads(session['infoDict'])[session['database']][session['server']]	

	colorDict = makeColorDict(columns, finalTuples, irregTimesDict)
	session['colorDict'] = json.dumps(colorDict)

	# Serialize
	session['columns'] = json.dumps(columns)

	return render_template('serverChosen.html', server=session['server'], database=session['database'], infoDict=json.loads(session['infoDict']), 
			   schema=schema, ptList=ptList, tabTups=finalTuples, columns=columns, tupLength=len(columns), colorDict=colorDict, sysDate=sysDate)


# Code for the portion of the website dealing with the chosen table
# If the table is valid, it prints the last date the table was modified
# Otherwise, it prints an error message 'Invalid table'
@application.route('/tableChosen', methods = ['POST', 'GET'])
def tableChosen():
	if request.method == 'POST':

		# Get tuples of tables, dates, list of possibleTables
		infoDict = json.loads(session['infoDict'])
		columns, ptList, tabTups, schema, sysDate, irregTimesDict = infoDict[session['database']][session['server']]

		colorDict = json.loads(session['colorDict'])

		# Get dictionary of table names to dates
		tabDict = tabTupsToDict(tabTups)

		# Retrieve entered table
		session['table'] = request.form['table']

		# If it is invalid
		if session['table'] not in ptList:
			result = "Invalid table"

		# If it is valid
		else:
			result = tabDict[session['table']]
		
		if session['table'] != '':
		
			return render_template('tableChosen.html', server=session['server'], database=session['database'], table=session['table'], infoDict=infoDict, 
				schema=schema, result=result, ptList=ptList, tabTups=tabTups, columns=columns, tupLength=len(columns), colorDict=colorDict, sysDate=sysDate)

		return render_template('serverChosen.html', server=session['server'], database=session['database'], infoDict=infoDict, 
				schema=schema, ptList=ptList, tabTups=tabTups, columns=columns, tupLength=len(columns), colorDict=colorDict, sysDate=sysDate)


# Note that we run on '0.0.0.0' to bypass restrictions
if __name__ == '__main__':
	application.run(host='0.0.0.0', debug=True, threaded=True)