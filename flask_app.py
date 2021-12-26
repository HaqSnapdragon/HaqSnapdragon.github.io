import flask
from flask import Flask
import matplotlib
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import requests
from bs4 import BeautifulSoup

# url = 'https://www.kinopoisk.ru/lists/top500/'


app = Flask(__name__)
matplotlib.use('Agg')
ANS = []
q1 = ""
q2 = ""
q3 = ""
Y = []
url = ''


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    global url
    if flask.request.method == 'POST':
        url = flask.request.form.get('url')
        global ANS
        ANS = []
        global Y
        Y = []

    return flask.render_template("home.html", url=url, answer=ANS)


@app.route("/about")
def about():
    return flask.render_template("about.html")


@app.route("/result", methods=['POST'])
def result():
    return


@app.route("/plot")
def plot():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    list2 = soup.find_all("span", {
        "class": ["rating__value rating__value_positive", "rating__value rating__value_neutral",
                  "rating__value rating__value_negative"]})
    list3 = []
    for item in list2:
        try:
            item_text = float(item.text)
        except ValueError:
            item_text = float(item.text[:2])
        if 0.0 <= item_text <= 10.0:
            list3.append(item_text)
        else:
            if 10 < item_text <= 100:
                list3.append(item_text / 10.0)
    list3.sort()
    x = []
    y = []

    for i in list3:
        statement = i
        if statement not in x:
            x.append(statement)
            y.append(list3.count(statement))
    fig = plt.figure()
    plt.plot(x, y)
    plt.grid()
    plt.xlabel('рейтинг ☆', fontsize=14)
    plt.ylabel('количество фильмов', fontsize=14)
    plt.scatter(ANS, Y, color='orange', s=40, marker='o')
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return flask.render_template("graph.html", picture=data, answer=ANS)


if __name__ == '__main__':
    app.run(debug=True)
