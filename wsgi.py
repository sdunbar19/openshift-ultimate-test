#################################################################################################
# Script name          	: index.py
# Script author		: Sarah Dunbar														#
# Script creation date 	: 06/14/21
# Last modified: 	: 06/27/21																#
# Script description   	: Runs the website containing the desired information	#
#################################################################################################

## TODOS
# TODO: Change query back (need currentdate - 1 not -2)

## Imports
import sys
import json
import numpy
import datetime
import time

from dataWrapper import createDictionaries
from python.maxDateWrapper import findTablesWrapper, tabTupsToDict

from flask import Flask, session, render_template, request, send_file
from flask_session import Session

## Sessions
# Note we are using sessions instead of globals
# This makes our code thread and process safe 
# (every thread and process will use the same variables and won't interfere)
application = Flask(__name__)
SESSION_TYPE = 'filesystem'
application.config.from_object(__name__)
Session(application)


## Globals
# These can be globals because they are constant
dbTbls, accInstr, columnsDict = createDictionaries()


## Webpage functions
# Code for the landing page of the website, containing choice of database
@app.route('/')
def landing():
	session['database'] = 'Unknown'
	session['server'] = 'Unknown'
	session['table'] = 'Unknown'
	session['tableTuples'] = 'Unknown'
	session['ptList'] = 'Unknown'
	session['columns'] = 'Unknown'
	session['colorDict'] = 'Unknown'
	return render_template('landing.html', accInstr=accInstr, dbTbls=dbTbls)

# Code for help pdf link
@app.route('/show/help-pdf/')
def show_help_pdf():
    return send_file('static/help.pdf', attachment_filename='help.pdf')

# Code for the table production
@app.route('/loading/<table>', methods=['GET'])
def selectedServer(table):
	
	global accInstr
	global dbTbls
	
	session['server'] = table
	session['database'] = accInstr[table][0]

	# Directs you to the loading screen until everything is loaded in loadPage()
	return render_template('loadingPage.html', accInstr=accInstr, dbTbls=dbTbls)

# Code for the loading resolution (tables and searchbar)
@app.route('/results', methods=['GET']) 
def loadPage():

	# Find tuple of (date, table) for all valid tables
    ptList, finalTuples, columns, colorDict = findTablesWrapper(accInstr, dbTbls, session['server'], session['database'], columnsDict)
    columns = ["Name"] + columns	

	# Serialize
    session['tableTuples'] = json.dumps(finalTuples)
    session['ptList'] = json.dumps(ptList)
    session['columns'] = json.dumps(columns)
    session['colorDict'] = json.dumps(colorDict)

    return render_template('serverChosen.html', server=session['server'], database=session['database'], accInstr=accInstr, 
				dbTbls=dbTbls, ptList=ptList, tabTups=finalTuples, columns=columns, tupLength=len(columns), colorDict=colorDict)

# Code for the portion of the website dealing with the chosen table
# If the table is valid, it prints the last date the table was modified
# Otherwise, it prints an error message 'Invalid table'
@app.route('/tableChosen', methods = ['POST', 'GET'])
def tableChosen():
	if request.method == 'POST':

		# Get tuples of tables, dates, list of possibleTables
		tabTups = json.loads(session['tableTuples'])
		ptList = json.loads(session['ptList'])
		columns = json.loads(session['columns'])
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
		
			return render_template('tableChosen.html', server=session['server'], database=session['database'], table=session['table'], accInstr=accInstr, 
			dbTbls=dbTbls, result=result, ptList=ptList, tabTups=tabTups, columns=columns, tupLength=len(columns), colorDict=colorDict)

		return render_template('serverChosen.html', server=session['server'], database=session['database'], accInstr=accInstr, 
				dbTbls=dbTbls, ptList=ptList, tabTups=tabTups, columns=columns, tupLength=len(columns), colorDict=colorDict)

# Note that we run on '0.0.0.0' to bypass restrictions
if __name__ == '__main__':
	application.run(debug=True, threaded=True)