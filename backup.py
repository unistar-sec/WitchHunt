from flask import request, render_template, Flask
from time import strftime
from os import system
import requests

app = Flask(__name__)
 
def getInfo():
    environ = request.environ
    shallow = request.shallow
    access_route = request.access_route
    charset = request.charset
    headers = request.headers
    remote_addr = request.remote_addr
    remote_user = request.remote_user
    return "Environ: %s\nshallow: %s\naccess_route: %s\ncharset: %s\nheaders: %s\nremote_addr: %s\nremote_user: %s\n" \
    %(environ, shallow, access_route, charset, headers, remote_addr, remote_user)


@app.errorhandler(404)
def record(e=None):
    timestamp = str(strftime("%m-%d %H:%M:%S"))+"\n"
    try:
        req = requests.get("http://ip-api.com/json/"+request.remote_addr).content
    except Exception as e:
        req = e
    for i in request.environ:
        result = timestamp + str(i) + ":\t" + str(request.environ[i]) + "\n"
    with open("potWeb.log", "a+") as f:
      print(result)
      print(req)
      f.write(result + req + "\n"*5)
    print()
    return render_template("500.html")



app.run(host="0.0.0.0", debug=False, port=80)
