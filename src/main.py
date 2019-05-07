from os import system

from UI import menu


def main():
    system("cls")
    system("title Enter 'help' to get help")

    menu.menuLoop()


def linkMaker():
    # Denna metod gör om ett itemID till en fungerade kringla länk

    base = 'http://www.kringla.nu/kringla/objekt?referens='  # Bas url till Kringla
    itemID = 'http://kulturarvsdata.se/raa/kmb/16000200041456'  # Exempel id

    url = itemID.split('e/', 1)[1]  # Splittar på .se/ och lämnar kvar 'raa/kmb/16000200041456'
    result = base + url  # Skapar en fungerade URL till kringla

    print(result)



if __name__ == "__main__":
    # linkMaker()
    main()
