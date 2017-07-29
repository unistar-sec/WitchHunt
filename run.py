from flask import request, render_template, Flask
from time import strftime
from os import system
import requests

app = Flask(__name__)

@app.route("/set")
def Set_Trap():
    return render_template()


app.run(host="0.0.0.0", debug=False, port=80)
