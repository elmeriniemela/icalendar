
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

def accept_component(component, skip_words):
    if component.name == 'VEVENT':
        if any(w in component['SUMMARY'] for w in skip_words):
            return False
    return True


def filter_cal(ical_object, skip_words):
    ical_object.subcomponents = [c for c in ical_object.subcomponents if accept_component(c, skip_words)]

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
        data = f.read()

    NEW = Calendar.from_ical(data)
    OLD = Calendar.from_ical(data)


    def help():
        print(
            "\nCommands:\n"
            "a = autorefactor\n"
            "f = filter\n"
            "p = print edited calendar\n"
            "o = print original calendar\n"
            "cls = clear screen\n"
            "q = quit\n"
            "? = help"
        )
    help()
    while True:
        print()
        commands = input("> ").split(' ')
        if not commands:
            continue
        elif commands[0] == 'q':
            break
        elif commands[0] == 'f':
            filter_words = commands[1:]
            filter_cal(NEW, filter_words)
            save(NEW)

        elif commands[0] == 'a':
            print_results(auto_refactor(NEW))
            save(NEW)

        elif commands[0] == 'p':
            print_summaries(NEW)
        elif commands[0] == 'o':
            print_summaries(OLD)
        elif commands[0] == '?':
            help()
        elif commands[0] == 'cls':
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print("Not valid command. Type ? for help")
