
import os
import sys

from icalendar import Calendar

from refactor_ics import distinct_summaries
from refactor_ics import auto_refactor

def print_summaries(ical_object):
    print(
        '\n'.join([
            '%s: %s' % (count, summary)
            for count, summary in enumerate(distinct_summaries(ical_object), start=1)
        ]),
    )
    


def save(ical_object):
    filename = sys.argv[1].rstrip('.ics') + "_refactored.ics"
    with open(filename, 'wb') as f:
        f.write(ical_object.to_ical())
    print("Refactored .ics saved to: " + filename)


def print_results(results):
    for key, value in results.items():
        print()
        print("Original:")
        print(key)
        print("Refactored:")
        print(value)
        print()





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
            print_results(auto_refactor(CAL))
            save(CAL)
        elif command == 'p':
            print_summaries(CAL)
        elif command == '?':
            help()
        elif command == 'cls':
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print("Not valid command. Type ? for help")
    