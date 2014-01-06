# requires python 3 & icalendar

from bottle import route, run
from icalendar import Calendar, vDDDTypes
from datetime import date, datetime
import urllib.request


# TODO configurable
URL = 'http://localhost/calendar.ics'
FORMAT = '%d-%m-%Y'

@route('/date/<date>')
def byDate(date):
	d = parseDate(date)
	events = {}
	for event in filterEvents(lambda e: datePredicate(e, d)):
		events[event['SUMMARY']] = toDict(event, d)
	return events

@route('/type/<type>')
def byType(type):
	d = date.today();
	events = {}
	for event in filterEvents(lambda e: typePredicate(e, type) and futurePredicate(e)):
		events[event['SUMMARY']] = toDict(event, d)
	return events

@route('/current')
def current():
	today = date.today()
	todayStr = today.strftime(FORMAT)
	return byDate(todayStr)

@route('/current/<type>')
def currentType(type):
	d = date.today()
	events = {}
	for event in filterEvents(lambda e: typePredicate(e, type) and datePredicate(e, d)):
		events[event['SUMMARY']] = toDict(event, d)
	return events

def getCal():
	calStr = fetch(URL)
	return Calendar.from_ical(calStr)

def fetch(url):
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)
	return response.read().decode('utf-8')

def parseDate(date):
	return datetime.strptime(date, FORMAT).date()

def filterEvents(predicate):
        return [event for event in getEvents() if predicate(event)]

def getEvents():
	events = []
	for event in getCal().walk('VEVENT'):
		events.append(event)
	return events

def toDict(event, d):
	start = vDDDTypes.from_ical(event['DTSTART'], d)
	end = vDDDTypes.from_ical(event['DTEND'], d)
	return {
		'start' : start.strftime(FORMAT),
		'end' : end.strftime(FORMAT),
		'diff': (end - d).days
	}

def datePredicate(event, d):
	start = vDDDTypes.from_ical(event['DTSTART'], d)
	end = vDDDTypes.from_ical(event['DTEND'], d)
	return start <= d <= end

def typePredicate(event, t):
	summary = event['SUMMARY'].lower()
	return t.lower() in summary

def futurePredicate(event):
	d = date.today()
	end = vDDDTypes.from_ical(event['DTEND'], d)
	return d <= end

run(host='10.30.9.10', port=81)