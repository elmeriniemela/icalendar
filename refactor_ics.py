from icalendar import Calendar, Event
import sys
import os

with open(sys.argv[1], 'rb') as f:
    cal = Calendar.from_ical(f.read())

def getCurrentCal():
    return '\n'.join(['%s: %s' % (k, v) for k, v in mapCal().items()])

def mapCal():
    count = 1
    mapping = {}
    for component in cal.walk(name='VEVENT'):
        old_name = str(component['summary'])
        if not old_name in mapping.values():
            mapping[count] = old_name
            count += 1
    return mapping

def auto_refactor():
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

    results = {

    }
    current_summarys = list(mapCal().values())
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

    with open(sys.argv[1].replace('.ics', '') + "_refactored.ics", 'wb') as f:
        f.write(cal.to_ical())

   
def handle_input():
    numbers = input("Number to replace (separate with comma if multiple selection ie. '1,2,3,4...'):\n")
    replacement = input("Give replacement:\n")
    list_of_nums = numbers.split(',')
    mapping = mapCal()
    for number in list_of_nums:
        try:
            number = int(number)
            old_name = mapping[number]
            for component in cal.walk():
                if component.name == 'VEVENT':
                    if old_name == str(component['summary']):
                        component['summary'] = replacement
        except Exception as error:
            print(error)

def help():
    print(
        "\nCommands:\n"
        "p = print open calendar\n"
        "q = quit\n"
        "s = save to example.ics\n"
        "r = refactor 1 or multiple lines\n"
        "a = autorefactor\n"
        "cls = clear screen (run 'cls' in terminal)\n"
        "? = help\n"
    )
help()
while True:
    command = input("> ")
    if command == 'q':
        break
    elif command == 's':
        f = open('example.ics', 'wb')
        f.write(cal.to_ical())
        f.close()
    elif command == 'r':
        handle_input()
    elif command == 'a':
        auto_refactor()
    elif command == 'p':
        print("\n" + getCurrentCal() + "\n")
    elif command == '?':
        help()
    elif command == 'cls':
        os.system('cls')
    else:
        print("Not valid command. Type ? for help")
    