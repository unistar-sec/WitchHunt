from flask import request, render_template, Flask
from flask_sqlalchemy import SQLAlchemy
import dataset


app = Flask(__name__)

db = dataset.connect("sqlite:///:memory:")

table = db["Case"]


def ScrapePage(target_url):
    # Creates a selenium instance to fetch the webpage source
    # Returns the webpage html given url
    from selenium import webdriver
    driver = webdriver.PhantomJS()
    driver.get(target_url)
    return driver.page_source


def Setup(notes, url, content, time, email):
    # Set up the honeypot webpage given the information
    # Return value indicates the states of setup
    # Check if the self url already exists
    if table.find_one(url=url) is not None:
        return 0
    table.insert(
        {
            "notes": notes,
            "url": url,
            "content": content,
            "time": time,
            "email": email
        }
    )
    return 1


@app.route("/set", methods=["GET", "POST"])
def Set_Trap():
    if request.method == "POST":
        notes = request.form["notes"]
        url = request.form["url"]
        content = request.form["content"]
        time = request.form["time"]
        email = request.form["email"]
        print(notes, url, content, time, email)
        return Setup(notes, url, content, time, email)
    else:
        return render_template("trap_set.html")


app.run(host="0.0.0.0", debug=False, port=80)
