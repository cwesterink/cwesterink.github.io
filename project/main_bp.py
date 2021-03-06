from flask import Blueprint, render_template, session, request, flash
from flask_login import login_required, current_user
import requests
from bs4 import BeautifulSoup
main_bp = Blueprint('main_bp', __name__, static_folder='static', template_folder='templates')


@main_bp.route('/unauthorized', methods=["GET"])
def unauthorized():
    return render_template("unauthorized.html")


@main_bp.route("/about-me")
def about():
    return render_template("aboutMe.html")

@main_bp.route('/', methods=['POST', "GET"])
def index():
    try:
        webpage_response = requests.get('https://www.merriam-webster.com/word-of-the-day')
        webpage = webpage_response.content
        soup = BeautifulSoup(webpage, "html.parser")

        word = soup.h1.text



        att = str(soup.find(['span'],{'class':'main-attr'}).text)


        pronunciation = str(soup.find(['span'], {'class': 'word-syllables'}).text)

        desc = att +" | "+pronunciation

        l = soup.find(['div'],{"class":"wod-definition-container"})
        defs = l.find_all(['p'])


        definitions = []
        for i in defs:
            if i.find(['strong']) == None:
                break
            definitions += [str(i.text)]

    except:
        word = ""
        definitions = []
        desc = ""

    def getDate():
        from datetime import datetime, timedelta, timezone

        current_time = datetime.now(timezone.utc) - timedelta(hours=8, minutes=0)
        months = ["January","February","March","April","May","June","July","August","September","October","November","December"]

        return months[current_time.month-1] + " " + str(current_time.day) + " " + str(current_time.year)


    if request.method == "GET" or request.method == 'POST':
        return render_template("index.html", wod = word, desc = desc, defs = definitions ,date = getDate())
