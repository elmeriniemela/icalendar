
import sys
import os
import re
from datetime import datetime
from icalendar import Calendar

def print_summaries(ical_object):
    print(
        '\n'.join([
            '%s: %s' % (count, summary)
            for count, summary in enumerate(distinct_summaries(ical_object), start=1)
        ]),
    )

def auto_refactor(ical_object):
    results = {}
    current_summarys = distinct_summaries(ical_object)
    for summary in current_summarys:
        parts = sorted(map(refactor, filter(useful, summary.split(','))), key=auditorium_last)
        results.update({summary: ",".join(parts).strip()})

    for key, value in results.items():
        for component in ical_object.walk():
            if component.name == 'VEVENT':
                if key == str(component['summary']):
                    component['summary'] = value
        print()
        print("Original:")
        print(key)
        print("Refactored:")
        print(value)
        print()
    
    filename = sys.argv[1].rstrip('.ics') + "_refactored.ics"
    with open(filename, 'wb') as f:
        f.write(ical_object.to_ical())
    print("Refactored .ics saved to: " + filename)


def distinct_summaries(ical_object):
    summaries = set()
    for component in ical_object.walk(name='VEVENT'):
        summaries.add(str(component['summary']))
    return summaries

def useful(part):
    current_year = datetime.now().year
    exclude = [
        str(current_year),
        str(current_year + 1),
        str(current_year - 1),
        "Luento/",
        "Lecture/",
        "Föreläsning/",
        "Harjoitukset/",
        "Exercises/",
        "Övningar/",
        "/Luento",
        "/Lecture",
        "/Föreläsning",
        "/Harjoitukset",
        "/Exercises",
        "/Övningar",
    ]
    for pattern in exclude:
        if re.findall(pattern, part):
            return False
    return True

def refactor(part):
    replacements = {
        # Targers cource code ' / 28C00500 - '
        r" / .*? - ": " ",
        r"Otakaari 1": "",
        r"Kurssitentti/Course examination/Kurssitentti": "TENTTI",
        r"  ": r" ",
    }
    for find, replace in replacements.items():
        part = re.sub(find, replace, part)
    return part

def auditorium_last(part):
    if re.findall(r' [UY][0-9]', part):
        return 1
    return -1


if __name__ == "__main__":
    with open(sys.argv[1], 'rb') as f:
        CAL = Calendar.from_ical(f.read())

    def help():
        print(
            "\nCommands:\n"
            "a = autorefactor\n"
            "p = print open calendar\n"
            "cls = clear screen\n"
            "q = quit\n"
            "? = help"
        )
    help()
    while True:
        print()
        command = input("> ")
        if command == 'q':
            break
        elif command == 'a':
            auto_refactor(CAL)
        elif command == 'p':
            print_summaries(CAL)
        elif command == '?':
            help()
        elif command == 'cls':
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print("Not valid command. Type ? for help")
    