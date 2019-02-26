from icalendar import Calendar, Event
import sys
import os

def calToString(cal):
    return '\n'.join(['%s: %s' % (k, v) for k, v in mapCal(cal).items()])

def mapCal(cal):
    count = 1
    mapping = {}
    for component in cal.walk(name='VEVENT'):
        old_name = str(component['summary'])
        if not old_name in mapping.values():
            mapping[count] = old_name
            count += 1
    return mapping

def auto_refactor(cal):
    import re
    from datetime import datetime
    current_year = datetime.now().year
    exclude = [
        str(current_year),
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

    replacements = {
        r" / .*? - ": " ",
        r"Otakaari 1": "",
        r"Kurssitentti/Course examination/Kurssitentti": "TENTTI",
        r"  ": r" ",
    }

    results = {}
    current_summarys = list(mapCal(cal).values())
    for summary in current_summarys:
        new_parts = []
        parts = summary.split(',')
        for part in parts:
            for find, replace in replacements.items():
                part = re.sub(find, replace, part)
            for pattern in exclude:
                if re.findall(pattern, part):
                    break
            else:
                new_parts.append(part)

        re_ordered = list(new_parts)
        for index, new_part in enumerate(new_parts):
            if re.findall(r' [A-Z][0-9]', new_part):
                re_ordered.append(re_ordered.pop(index))
        results.update({summary: ",".join(re_ordered).strip()})

    for key, value in results.items():
        for component in cal.walk():
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
        f.write(cal.to_ical())
    print("Refactored .ics saved to: " + filename)



if __name__ == "__main__":
    with open(sys.argv[1], 'rb') as f:
        cal = Calendar.from_ical(f.read())

    def help():
        print(
            "\nCommands:\n"
            "a = autorefactor\n"
            "p = print open calendar\n"
            "cls = clear screen\n"
            "q = quit\n"
            "? = help\n"
        )
    help()
    while True:
        command = input("> ")
        if command == 'q':
            break
        elif command == 'a':
            auto_refactor(cal)
        elif command == 'p':
            print("\n" + calToString(cal) + "\n")
        elif command == '?':
            help()
        elif command == 'cls':
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print("Not valid command. Type ? for help")
    