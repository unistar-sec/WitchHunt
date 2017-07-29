from flask import request, render_template, Flask
import requests

app = Flask(__name__)


@app.route("/set", methods=["GET", "POST"])
def Set_Trap():
    if request.method == "POST":
        notes = request.form["notes"]
        url = request.form["url"]
        content = request.form["content"]
        time = request.form["time"]
        email = request.form["email"]
        print(notes, url, content, time, email)
        return "\n".join([notes, url, content, time, email])
    else:
        return render_template("trap_set.html")


app.run(host="0.0.0.0", debug=False, port=80)
