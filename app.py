"""
This is the starting menu. 
It is where users can sign in if they already have a username, or register if they don't.
If the input is anything other than 1 or 2, the function will stop.
"""
def show_menu():
    print("1. Sign in")
    print("2. Register")

    option = input("Enter option: ")
    return option

def menu():
    while True:
        option = show_menu()
        if option == "1":
            print("You have chosen Sign in")
        elif option == "2":
            print("You have chosen Register")
        else: 
            break 
        print("")

menu()


