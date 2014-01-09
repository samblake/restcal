# requires python 3 & icalendar

from bottle import route, run, response, hook
from icalendar import Calendar, vDDDTypes
from datetime import date, datetime
import urllib.request

# TODO configurable
URL = 'http://localhost/calendar.ics'
FORMAT = '%d-%m-%Y'

@hook('after_request')
def cors():
	# Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
	response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@route('/date/<date>')
def byDate(date):
	d = parseDate(date)
	return filterEvents(lambda e: datePredicate(e, d), today())

@route('/type/<type>')
def byType(type):
	return filterEvents(lambda e: typePredicate(e, type) and futurePredicate(e), today())

@route('/current')
def current():
	todayStr = today().strftime(FORMAT)
	return byDate(todayStr)

@route('/current/<type>')
def currentType(type):
	d = today()
	return filterEvents(lambda e: typePredicate(e, type) and datePredicate(e, d), d)

def getCal():
	calStr = fetch(URL)
	return Calendar.from_ical(calStr)

def fetch(url):
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)
	return response.read().decode('utf-8')

def parseDate(date):
	return datetime.strptime(date, FORMAT).date()

def filterEvents(predicate, d):
        events = {}
        for event in getCal().walk('VEVENT'):
                if predicate(event):
                        events[event['SUMMARY']] = toDict(event, d)
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
	d = today()
	end = vDDDTypes.from_ical(event['DTEND'], d)
	return d <= end

def today():
	return date.today()

run(host='10.30.9.10', port=81)
