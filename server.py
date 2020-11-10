from flask import Flask, render_template, send_from_directory, request, redirect
import os
import csv

app = Flask(__name__.split('.')[0])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)


def write_to_text_file(data: dict):
    with open("database.txt", mode="a") as database:
        email = data.get("email")
        subject = data.get("subject")
        message = data.get("message")
        database.write(f"\n{email}, {subject}: {message}")


def write_to_csv_file(data: dict):
    with open("database.csv", mode="a", newline="") as database:
        email = data.get("email")
        subject = data.get("subject")
        message = data.get("message")
        csv_writer = csv.writer(database, delimiter=",",
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


@app.route("/submit_form", methods=["POST", "GET"])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            write_to_csv_file(data)
            return redirect("/thankyou.html")
        except:
            return "Something went wrong... Not saved to Database."
    else:
        return "Something went wrong. Try again."
