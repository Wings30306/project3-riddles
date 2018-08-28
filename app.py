import json

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
            sign_in()
        elif option == "2":
            register()
        else: 
            break 
        print("")


"""
If option 1 is selected in the menu, this function will allow the user to sign in.
If the username is not registered, the user will be asked to register.
"""
def sign_in():
    username = input("Your Username:\n")
    active_users = {}

    with open("data/users.txt", "r") as file:
        active_users = file.read().splitlines()
        if username in active_users:
            play_game()
        else:
            print("sorry, this username is incorrect. New user? Please register.")

    number_of_members = len(active_users)
    print("{0} active players right now".format(number_of_members))


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
            file = open("data/users.txt", "a")
            file.write(user + "\n")
            print("You are now registered. Please sign in to continue.") 


"""
After signing in, users will be asked twenty riddles from the json file
"""
def play_game():
    #These vars ensure the score is set to 0 before playing.
    user = ""
    score = 0 
    total_questions = 0
    #opens the riddles.json file to get the riddles and answer keywords
    with open("data/riddles.json") as riddle_data:
        data = json.load(riddle_data)
        for riddle in data["riddles"]:
          #For every riddle asked, 1 is added to the total_questions variable
            print(riddle["riddle"] + "\n")
            total_questions += 1
            #user's answer is registered in the guess variable
            guess = input("Your answer: ").lower
            answer = riddle["answer"]
            #this if statement checks whether the answer keyword from the file is in the guess
            #this prevents answers from being read as wrong due to an article or a verbose phrasing
            if answer in guess:
                print("Well done!\n")
                score += 1
            else:
                print("I'm sorry, this answer is incorrect.\n")
            print("You have so far answered {0} out of {1} question(s) correctly.\n\n".format(score, total_questions))
    #when all riddles are answered, this marks the end of the quiz    
    print("Congratulations {2}, you have completed the quiz and scored {0}/{1}.".format(score, total_questions, user))



menu()