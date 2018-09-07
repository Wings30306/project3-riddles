import json
import random
import os
from collections import OrderedDict
from flask import Flask, redirect, render_template, request, flash, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sign_in", methods=["POST"])
def sign_in():
    user = request.form["username"]
    with open("data/users.txt", "r") as file:
        active_users = file.read().splitlines()
        if user in active_users:
            return redirect(f"/riddles/{user}")
        else:
            signin_message = "Sorry, this user is incorrect. New user? Please register."
            return render_template("index.html", signin_message=signin_message)


@app.route("/register", methods=["POST"])
def register():
    user = request.form["new_user"]
    with open("data/users.txt", "r") as file:
        active_users = file.read().splitlines()
        if user in active_users:
            register_message = "Sorry, this username is taken. Please choose a different username."
        else:
            file = open("data/users.txt", "a")
            file.write(user + "\n")
            register_message = "You are now registered. Please sign in to continue."
        return render_template("index.html", register_message=register_message)


def open_riddles():
    with open("data/riddles.json") as riddle_data:
        data = json.load(riddle_data)
        for riddle in data["riddles"]:
            riddle = riddle["riddle"]
        for answer in data["riddles"]:
            answer = answer["answer"]
            total_questions = len(data["riddles"])
        return riddle, total_questions, answer


"""
def riddles(username):
    total_questions = open_riddles()[2]
    riddle = open_riddles()[0]    
    return render_template("riddles.html", riddle=riddle, total_questions=total_questions, username=username)


def answers(username):
    user = username
    score = 0 
    guess = request.form.get("guess")
    guess = guess.lower
    answer = open_riddles()[1]
    if answer in guess:
        message = "Well done!"
        score += 1
    else:
        message = "I'm sorry, " + user + ", this answer is incorrect."
    return render_template("result.html", message=message, score=score, username=username)
"""


@app.route("/riddles/<username>", methods=["GET", "POST"])
def show_riddles(username):
    user = username
    total_questions = open_riddles()[1]
    score = 0
    if request.method == "POST":
        guess = request.form.get("guess")
        guess = guess.lower()
        answer = open_riddles()[2]
        if answer in guess:
            message = "Well done!"
            score += 1
        else:
            message = "I'm sorry, " + user + ", this answer is incorrect."
        return render_template("result.html", username=user, score=score, message=message, total_questions=total_questions) 
    riddle = open_riddles()[0]
    return render_template("riddles.html", riddle=riddle, username=user)


@app.route("/result/<username>", methods=["GET", "POST"])
def result(username):
    user = username
    if request.method == "POST":
        return redirect(f"/riddles/{user}")
    return render_template("result.html", username=user)
    

if __name__ == '__main__':
    app.run(host=os.getenv('IP'),
            port=os.getenv('PORT'),
            debug=True)
