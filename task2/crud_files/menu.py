from crud_files import handler

EXIT_ITEMS = ("exit", "quit", "e", "q")


def menu(db):
    while True:
        choice = input(
            f'Do you want to work with DB "cats" collection? (enter {EXIT_ITEMS} for exit or any other for proceed):  '
        )
        if choice.lower() in EXIT_ITEMS:
            print("Programm succesfully stopped")
            break
        choice = input(
            'Enter type of operation: \t "i": insert record(s);\n\t\t\t\t "d": delete record(s);\n\t\t\t\t "u": update (change) record(s);\n\t\t\t\t "r": read (find) record(s);\n\t\t\t\t "e": exit\n'
        )
        match choice.lower():
            case "i":
                handler.insert(db)
            case "d":
                handler.delete(db)
            case "u":
                handler.update(db)
            case "r":
                handler.read(db)
            case "e":
                print("Programm succesfully stopped")
                break
            case _:
                print("Incorrect input")
