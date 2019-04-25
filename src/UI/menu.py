import sys
from os import system

from Networking import net
from QuerieFields import querieFields
from utils import bcolors


def menuLoop():
    while True:
        func, extra = parseInput()

        if func is not None:
            func(extra)  # Kör funktionen


def parseInput():
    _in = input("> ").strip()  # Gets indata and removes whitespaces
    words = _in.split(" ")
    func = parseCommand(words[0].lower())

    return func, ' '.join([str(x) for x in words[1:]])


def parseCommand(x):
    return {
        'help': helper,
        '': None,
        'build': doBuilder,
        'b': doBuilder,
        'print': printer,
        'cls': clearScreen,
        'exit': killApp
    }.get(x, helper)


def helper(extra):
    print("\n## Commands ##\nHelp: Get Help\nbuild: Build a query")


def printer(extra):
    print(extra)


def doBuilder(extra):
    system("mode con:cols=80 lines=40")  # Changes window size
    fields = queryFieldBuilder()

    networker = net.Networking()

    networker.call(fields)

    # print(fields)


def queryFieldBuilder():
    selected = []

    qf = querieFields.QuerieFields()
    _list = qf.getList()

    while True:
        clearScreen(None)
        for i, e in enumerate(_list):

            if i in selected:
                print(bcolors.bcolors.OKGREEN, bcolors.bcolors.UNDERLINE, end="")

            print('{} {}: {}'.format(i, e.query, e.desc))
            print(bcolors.bcolors.ENDC, end="")

        print("\n'-1' when done")
        try:
            sel = int(input("Select field index: "))

            if sel < 0:  # Done. Exit loop
                break

            if sel in selected:  # Remove from list
                selected.remove(sel)

            else:  # Add to list
                # Failsafe. only accept a valid index
                if sel < len(_list):
                    selected.append(sel)

        except Exception:
            pass

    clearScreen(None)

    newList = []
    # Append selected items in a new list
    for e in selected:
        newList.append(_list[e].query)

    return ','.join(newList)


def clearScreen(extra):
    system("cls")


def killApp(extra):
    sys.exit(0)
