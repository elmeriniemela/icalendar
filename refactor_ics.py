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
        "\nCommands:\n" +
        "p = print open calendar\n"
        "q = quit\n" +
        "s = save to example.ics\n"+
        "r = refactor 1 or multiple lines\n" +
        "cls = clear screen (run 'cls' in terminal)"
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
    elif command == 'p':
        print("\n" + getCurrentCal() + "\n")
    elif command == '?':
        help()
    elif command == 'cls':
        os.system('cls')
    else:
        print("Not valid command. Type ? for help")
    