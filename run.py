from flask import request, render_template, Flask
import dataset
import os
import requests
from ast import literal_eval
#from datetime import datetime, timedelta

app = Flask(__name__)

# Setting up the in-memory database
db = dataset.connect("sqlite:///:memory:")
table = db["Case"]


def GetPreyInfo():
    # Generates a report regarding the prey who triggers the trap
    environ = request.environ
    ip = str(environ["REMOTE_ADDR"])
    port = str(environ["REMOTE_PORT"])
    ua = str(environ["HTTP_USER_AGENT"])
    method = str(environ["REQUEST_METHOD"])
    path = str(environ["PATH_INFO"])
    query = str(environ["QUERY_STRING"])
    cookie = str(environ["HTTP_COOKIE"])
    language = str(environ["HTTP_ACCEPT_LANGUAGE"])
    encoding = str(environ["HTTP_ACCEPT_ENCODING"])
    accept = str(environ["HTTP_ACCEPT"])
    # Make a request to fetch the detailed geo location regarding the prey
    response = requests.get("http://ip-api.com/json/" + ip).content
    # Convert String presentation of dict into a proper dict
    response = literal_eval(str(response)[2:-1])
    # Construct the report
    report = "Prey Information:\n\t" +\
        "IP: " + ip + "\n\t" +\
        "PORT: " + port + "\n\t" +\
        "User Agent: " + ua + "\n\t" +\
        "Request Method: " + method + "\n\t" +\
        "Path:" + path + "\n\t" +\
        "Query: " + query + "\n\t" +\
        "Cookie: " + cookie + "\n\t" +\
        "Language: " + language + "\n\t" +\
        "Encoding: " + encoding + "\n\t" +\
        "Accept: " + accept + "\n\n" + \
        "Geolocation Analysis:\n"
    for key in response.keys():
        report += key + ": " + response[key] + "\n"
    return report


def ScrapePage(target_url):
    # Creates a selenium instance to fetch the webpage source
    # Returns the webpage html given url
    from selenium import webdriver
    driver = webdriver.PhantomJS()
    driver.get(target_url)
    source = driver.page_source
    driver.quit()
    # Remove log file
    os.remove("ghostdriver.log")
    return source


def Setup(notes, url, content, time, email):
    # Set up the honeypot webpage given the information
    # Return value indicates the states of setup
    # Check if the self url already exists
    result = table.find_one(url=url)
    if result is not None:
        return "0"
    else:
        # Change content variable into the html source it's pointing to
        if content == "500":
            html = render_template("500.html")
        elif content == "404":
            html = render_template("404.html")
        else:
            html = ScrapePage(content)

        table.insert({
            "notes": notes,
            "url": url,
            "content": html,
            "time": time,
            "email": email
        })
    return "1"


@app.errorhandler(404)
def Catch(e=None):
    # Handles all trap and non-trap requests
    suffix = "/".join(request.url.split("/")[3:])
    # print(suffix)
    result = table.find_one(url=suffix)
    if result is None:
        # No trap here
        return "FUCK OFF"
    else:
        # Bingo !!! Trap is triggered !
        # Fetch all releavent information from database records
        trap_url = request.url
        email_title = result["notes"]
        email_addr = result["email"]
        html = result["content"]
        valid_time = result["time"]
        # Get all information about the prey
        report = GetPreyInfo()
        print(report)
        # Return the pre-defined fake webpage
        return html


@app.route("/set", methods=["GET", "POST"])
def Set_Trap():
    if request.method == "POST":
        # Fetch Settings
        notes = request.form["notes"]
        url = request.form["url"]
        content = request.form["content"]
        time = request.form["time"]
        email = request.form["email"]
        #print(notes, url, content, time, email)
        return Setup(notes, url, content, time, email)
    else:
        return render_template("trap_set.html")


app.run(host="0.0.0.0", debug=False, port=80)


# Need to get currrent timestamp of the time when set up
# If record already exist during setup, check if the existing record has expired, if so, overwrite.
# Calculate the expiry time when put in db
# Need to implement email functions for sending notifications regarding the prey's info and time and project name
