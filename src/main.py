from os import system

from UI import menu


def main():
    system("cls")
    system("title Enter 'help' to get help")

    menu.menuLoop()


if __name__ == "__main__":
    main()
