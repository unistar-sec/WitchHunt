from flask import request, render_template, Flask
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
    suffix = "/".join(request.url.split("/")[3:])
    print(suffix)
    result = table.find_one(url=suffix)
    if result is None:
        # No trap here
        return "FUCK OFF"
    else:
        # Bingo!
        trap_url = request.url
        email_title = result["notes"]
        email_addr = result["email"]
        html = result["content"]
        valid_time = result["time"]
        print(trap_url, email_title, email_addr, valid_time)
        return html


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
