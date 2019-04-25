import sys
from os import system

from Networking import net
from QuerieFields import querieFields
from SQLite import database
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
        'db': databasePlus,
        'print': printer,
        'cls': clearScreen,
        'clear': clearScreen,
        'show': show,
        'exit': killApp
    }.get(x, helper)


def show(extra):
    args = extra.split(" ")
    if args[0] == "record":
        dbShowRecord()
    else:
        print("""'record'
        """)


def dbShowRecord():
    db = database.DB("databas.db")
    db.dbShowRecord()
    db.dbCloseConnection()


def databasePlus(extra):
    args = extra.split(" ")
    db = database.DB("databas.db")
    if args[0] == 'reset' or args[0] == 'r':
        db.createTables()
        print("Database reset and cleared")
    else:
        print("Error: '{}' is not valid!".format(args[0]))

    db.dbCloseConnection()


def helper(extra):
    print("""
## Commands ##
Help: Get Help
Build/b: Build a query
db "reset/r": Clears and resets the database
show "record": Displays the current item record
""")


def printer(extra):
    print(extra)


def doBuilder(extra):
    system("mode con:cols=80 lines=40")  # Changes window size
    fields = queryFieldBuilder()

    if len(fields) == 0:
        print("Error: Nothing selected")
        return

    # print(fields)
    # return
    networker = net.Networking()
    networker.makeRequest(fields)


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

        print("\nEnter when done, -1 to toogle everything")
        try:
            sel = input("Select field index: ").strip()  # Take input and remove spaces from start and end

            if sel == '':  # Check if only enter was pressed
                # if len(selected) > 0:
                break

            sel = int(sel)  # Turn into int

            if sel == -1:  # Toggle selected list
                if len(selected) == 0:  # Add everything if empty /  != len(_list)
                    selected = []
                    selected.extend(range(len(_list)))
                else:
                    # Remove everything if list has items
                    selected = []
            else:
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
