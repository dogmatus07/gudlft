import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    """
    Load the clubs from the clubs.json file    
    """
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    """
    Load the competitions from the competitions.json file
    """
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    """
    Render the index.html template
    """
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    """
    Show the summary of the club and competitions
    """
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
        return render_template(
            "welcome.html", club=club, competitions=competitions, clubs=clubs
        )
    except IndexError:
        flash("Sorry, this email address is not recognized")
        return render_template("index.html")


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """
    Book a competition
    """
    foundClub = next((c for c in clubs if c["name"] == club), None)
    foundCompetition = next((c for c in competitions if c["name"] == competition), None)
    
    if not foundClub:
        flash("Sorry, this club is not recognized")
        return render_template("welcome.html", competitions=competitions, clubs=clubs, club=foundClub)

    if not foundCompetition:
        flash("Sorry, this competition is not recognized")
        return render_template("welcome.html", competitions=competitions, clubs=clubs, club=foundClub)

    # check if the competition has already taken place
    competitionDate = datetime.strptime(foundCompetition["date"], "%Y-%m-%d %H:%M:%S")
    if competitionDate < datetime.now():
        flash("Sorry, you cannot book a competition that has already taken place")
        return render_template("welcome.html", club=foundClub, competitions=competitions, clubs=clubs)

    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)

@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    """
    Purchase places for a competition
    """
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])

    # check if the user is trying to book more than 12 places
    if placesRequired > 12:
        flash("Sorry, you cannot book more than 12 places")
        return render_template(
            "welcome.html", club=club, competitions=competitions, clubs=clubs
        )

    pointsRequired = placesRequired * 1

    # check if the user has enough points to book the places
    if pointsRequired > int(club["points"]):
        flash("Sorry, you do not have enough points to redeem the places")
        return render_template("welcome.html", club=club, competitions=competitions)


    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
    # update the number of points for the club after booking
    club["points"] = int(club["points"]) - pointsRequired
    
    flash("Great-booking complete!")
    return render_template(
        "welcome.html", club=club, competitions=competitions, clubs=clubs
    )


# TODO: Add route for points display
@app.route("/pointsBoard")
def pointsBoard():
    return render_template("points_board.html", clubs=clubs)


@app.route("/logout")
def logout():
    """
    Logout the user
    """
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
