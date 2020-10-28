from icalendar import Calendar
fname = 'filter.ics'

with open(fname, 'rb') as ics_file:
    ical_obj = Calendar.from_ical(ics_file.read())

print(ical_obj.subcomponents)


out = ical_obj.to_ical()
with open(fname, 'wb') as f:
    f.write(out)