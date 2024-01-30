import os
from datetime import datetime

from flask import Flask, request, render_template
import requests

app = Flask(__name__)

fqdn = os.getenv("FQDN")


@app.route('/books')
def retrieve_books_before():  # put application's code here
    before_year = request.args.get('before_year')
    response = requests.get(fqdn + "/api")
    if response.status_code != 200:
        return "Invalid api"
    print(before_year)
    if not before_year:
        return "Invalid year"
    before_year = int(before_year)

    data = response.json()
    for ind in range(len(data) - 1, -1, -1):
        if data[ind]['publication_year'] >= before_year:
            data.remove(data[ind])

    for dat in data:
        print(dat['publication_year'])
    return data

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/filter", methods=["POST", "GET"])
def filter_json():
    if request.method == 'GET':
        return home_page()
    ts = int(request.form.get("date-time"))
    year = datetime.utcfromtimestamp(ts).strftime('%Y')
    url = fqdn + "/api" + "?before_year=" + year
    return requests.get(url)



if __name__ == '__main__':
    app.run()
