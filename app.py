import json
import random
import os
from collections import OrderedDict
from flask import Flask, redirect, render_template, request, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
app = Flask(__name__)


#global variables
user = ""



"""
This is the starting menu. 
It is where users can sign in if they already have a username, or register if they don't.
If the input is anything other than 1, 2 or 3 the function will stop.
"""
@app.route("/", methods=["GET", "POST"])
def show_menu():
    print("1. Sign in")
    print("2. Register")
    print("3. See Leaderboard")

    option = input("Enter option: ")
    return option

def menu():
    while True:
        option = show_menu()
        if option == "1":
            sign_in()
        elif option == "2":
            register()
        elif option == "3":
            scoreboard()
        else: 
            break 
        print("")


"""
If option 1 is selected in the menu, this function will allow the user to sign in.
If the username is not registered, the user will be asked to register.
"""
def sign_in():
    name = input("Your Username:\n")
    active_users = {}

    with open("data/users.txt", "r") as file:
        active_users = file.read().splitlines()
        if name in active_users:
            play_game(name)
        else:
            print("sorry, this username is incorrect. New user? Please register.")

    number_of_members = len(active_users)
    print("{0} active players right now".format(number_of_members))


"""
If option 2 is selected in the menu, this function will allow the user to register.
If the username is already in use, the user will be notified.
"""
def register():
    name = input("Please choose a username\n>")
    active_users = {}

    with open("data/users.txt", "r") as file:
        active_users = file.read().splitlines()
        if name in active_users:
            print("sorry, this username is taken. Please choose a different username.")
        else:            
            file = open("data/users.txt", "a")
            file.write(name + "\n")
            print("You are now registered. Please sign in to continue.") 


"""
After signing in, users will be asked twenty riddles from the json file
"""
def play_game(name):
    #These vars ensure the score is set to 0 before playing.
    score = 0 
    total_questions = 0
    #opens the riddles.json file to get the riddles and answer keywords
    with open("data/riddles.json") as riddle_data:
        data = json.load(riddle_data)
        random.shuffle(data["riddles"])
        for riddle in data["riddles"]:
          #For every riddle asked, 1 is added to the total_questions variable
            print(riddle["riddle"] + "\n")
            total_questions += 1
            #user's answer is registered in the guess variable
            guess = input("Your answer: ")
            guess = guess.lower()
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
    print("Congratulations {2}, you have completed the quiz and scored {0}/{1}.".format(score, total_questions, name))
    #define user function for easily writing to json
    def user(name, score):
        user = {"user": name, "score" : score }
        user = (user)
        return (user)
    #open json file to check content
    with open("data/score.json", "r") as score_data:
        leaderboard = json.load(score_data)
        leaderboard["users"].append(user(name, score))
        with open("data/score.json", "w") as score_data_updated:
            json.dump(leaderboard, score_data_updated, indent=2)



def scoreboard():
    with open("data/score.json", "r") as leaderboard:
        scoreboard = json.load(leaderboard)
        #sorted_scoreboard = sorted(scoreboard["users"][0:3], key=lambda x: x.score, reverse=True)
        print(scoreboard["users"][0]["user"], scoreboard["users"][0]["score"])
        print(scoreboard["users"][1]["user"], scoreboard["users"][1]["score"])
        print(scoreboard["users"][2]["user"], scoreboard["users"][2]["score"])
        #print("\n")
        #print(sorted_scoreboard)


menu()


if __name__ == '__main__':
    app.run(host=os.getenv('IP'),
            port=os.getenv('PORT'),
            debug=True)