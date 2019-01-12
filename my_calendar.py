import sys, re, os
from icalendar import Calendar, Event

class MyCalendar:
    selection = []

    def __init__(self, file):
        with open(file, 'rb') as f:
            self.cal = Calendar.from_ical(f.read())
        self.query()

    def query(self, start_dt=None, end_dt=None, regex=None):
        self.selection = []
        for event in self.cal.walk(name='VEVENT'):
            if start_dt and not event.decoded('dtstart') > start_dt:
                continue
            elif end_dt and not event.decoded('dtend') < end_dt:
                continue
            elif regex and not re.findall(regex, str(event['summary'])):
                continue
            self.selection.append(event)
    def display(self):
        print('\n'.join(['%s: %s' % (str(x.decoded('dtstart')), str(x['summary'])) for x in self.selection]))
    
    def rename(self, name):
        for event in self.selection:
            event['summary'] = name
    
    
    

cal = MyCalendar('icalexport.ics')
cal.query()
cal.display()

while True:
    command = input('> ')
    try:
        eval('cal.{}'.format(command))
    except AttributeError as error:
        eval(command)
        