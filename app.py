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


@app.route("/signin", methods=["POST"])
def sign_in():
    user = request.form["username"]
    with open("data/users.txt", "r") as file:
        score = 0
        total_questions = 1
        active_users = file.read().splitlines()
        if user in active_users:
            return redirect(f"/riddles/{user}/{score}/{total_questions}")
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
    new_score = int(score)
    if request.method == "POST":
        guess = request.form.get("guess")
        guess = guess.lower()
        answer = open_riddles()[2]
        if answer in guess:
            new_score += 1
            return redirect(f"/rightanswer/{user}/{new_score}/{total_questions}")
        else:
            return redirect(f"/wronganswer/{user}/{new_score}/{total_questions}")
    riddle = open_riddles()[0]
"""


@app.route("/riddles/<username>/<score>/<total_questions>", methods=["GET", "POST"])
def show_riddles(username, total_questions, score):
    data = []
    with open("data/riddles.json", "r") as riddle_data:
        data = json.load(riddle_data)
        for riddle in data["riddles"]:
            answer = riddle["answer"]
    return render_template("riddles.html", username=username, total_questions=total_questions, score=score, riddles_data=data, answer=answer)


@app.route("/rightanswer/<username>/<score>/<total_questions>", methods=["GET", "POST"])
def result_correct(username, total_questions, score):
    user = username
    score = score
    if request.method == "POST":
        new_total_questions = int(total_questions) 
        new_total_questions += 1
        return redirect(f"/riddles/{user}/{score}/{new_total_questions}")
    return render_template("rightanswer.html", username=user, total_questions=total_questions, score=score)


@app.route("/wronganswer/<username>/<score>/<total_questions>", methods=["GET", "POST"])
def result_wrong(username, total_questions, score):
    user = username
    score = score
    if request.method == "POST":
        new_total_questions = int(total_questions) 
        new_total_questions += 1
        return redirect(f"/riddles/{user}/{score}/{new_total_questions}")
    return render_template("wronganswer.html", username=user, total_questions=total_questions, score=score)
    

if __name__ == '__main__':
    app.run(host=os.getenv('IP'),
            port=os.getenv('PORT'),
            debug=True)
