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
            register()
        else: 
            break 
        print("")


"""
If option 2 is selected in the menu, this function will allow the user to register.
If the username is already in use, the user will be notified.
"""
def register():
    user = input("Please choose a username\n>")
    active_users = {}

    with open("data/users.txt", "r") as file:
        active_users = file.read().splitlines()
        if user in active_users:
            print("sorry, this username is taken. Please choose a different username.")
        else:
            print("You are now registered. Please sign in to go to the game.")
            file = open("data/users.txt", "a")
            file.write(user + "\n")



menu()