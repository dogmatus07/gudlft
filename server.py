import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
        return render_template("welcome.html", club=club, competitions=competitions)
    except IndexError:
        flash("Sorry, this email address is not recognized")
        return render_template("index.html")


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]

    # check if the competition has already taken place
    competitionDate = datetime.strptime(foundCompetition["date"], "%Y-%m-%d %H:%M:%S")
    if competitionDate < datetime.now():
        flash("Sorry, you cannot book a competition that has already taken place")
        return render_template(
            "welcome.html", club=foundClub, competitions=competitions
        )

    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])

    # check if the user is trying to book more than 12 places
    if placesRequired > 12:
        flash("Sorry, you cannot book more than 12 places")
        return render_template("welcome.html", club=club, competitions=competitions)

    pointsRequired = placesRequired * 1

    # check if the user has enough points to book the places
    if pointsRequired > int(club["points"]):
        flash("Sorry, you do not have enough points to redeem the places")
        return render_template("welcome.html", club=club, competitions=competitions)

    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
