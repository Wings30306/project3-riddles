import json
import random
import os
from collections import OrderedDict
from flask import Flask, redirect, render_template, request, flash, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sign_in", methods=["POST"])
def sign_in():
    user = request.form["username"]
    with open("data/users.txt", "r") as file:
        active_users = file.read().splitlines()
        if user in active_users:
            render_template("riddles.html", username=user)
            return redirect(url_for("riddles"))
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


@app.route("/riddles", methods=["GET", "POST"])
def riddles():
    score = 0
    total_questions = 0
    # opens the riddles.json file to get the riddles and answer keywords
    with open("data/riddles.json") as riddle_data:
        data = json.load(riddle_data)
        random.shuffle(data["riddles"])
        for riddle in data["riddles"]:
          # For every riddle asked, 1 is added to the total_questions variable
            riddle = riddle["riddle"]
            total_questions += 1
            
        return render_template("riddles.html", riddle=riddle, score=score, total_questions=total_questions)

if __name__ == '__main__':
    app.run(host=os.getenv('IP'),
            port=os.getenv('PORT'),
            debug=True)
