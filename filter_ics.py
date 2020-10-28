from icalendar import Calendar
fname = 'filter.ics'

with open(fname, 'rb') as ics_file:
    ical_obj = Calendar.from_ical(ics_file.read())


def accept_component(component):
    if component.name != 'VEVENT':
        return True

import pdb; pdb.set_trace()
for component in ical_obj.subcomponents:
    print(component)

out = ical_obj.to_ical()
with open(fname, 'wb') as f:
    f.write(out)