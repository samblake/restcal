RESTcal
=======

A web service to filter and display iCal events.

Requires Python 3. 

Paths are:

  * /date/<date> - Shows events on the given date
  * /type/<type> - Shows events of the given type 
  * /current - Shows events on the current date
  * /current/<type> - Shows events on the current date of the given type
  
The date format is %d-%m-%Y, for example 23-02-2014.
