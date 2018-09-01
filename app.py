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


@app.route("/", methods=["GET", "POST"])
def sign_in():
    name = request.form["username"]
    with open("data/users.txt", "r") as file:
        active_users = file.read().splitlines()
        if name in active_users:
            render_template("riddles.html", username=name)
            return redirect(url_for("riddles"))
        else:
            signin_message = "Sorry, this username is incorrect. New user? Please register."
            return render_template("index.html", signin_message=signin_message)


@app.route("/", methods=["GET", "POST"])
def register():
    name = request.form["new_user"]
    with open("data/users.txt", "r") as file:
        active_users = file.read().splitlines()
        if name in active_users:
            register_message = "Sorry, this username is taken. Please choose a different username."
        else:            
            file = open("data/users.txt", "a")
            file.write(name + "\n")
            register_message = "You are now registered. Please sign in to continue."
        return render_template("index.html", register_message=register_message)


@app.route("/riddles", methods=["GET", "POST"])
def riddles():
    score = "X"
    total_questions = "Y"
    return render_template("riddles.html", score=score, total_questions=total_questions)

if __name__ == '__main__':
    app.run(host=os.getenv('IP'),
            port=os.getenv('PORT'),
            debug=True)
