import os

import requests
from flask import Flask, send_file, Response, redirect
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()


def pig_latinate(string):
    try:
        request_url = 'https://hidden-journey-62459.herokuapp.com/piglatinize/'
        data = {'input_text': string}
        r = requests.post(request_url, data, allow_redirects=False)

        soup = BeautifulSoup(r.text, "html.parser")
        url = soup.find_all("a")[0].getText()

        latinize_url = 'https://hidden-journey-62459.herokuapp.com' + url
    except ConnectionError:
        latinize_url = 'Connection failed, please retry. :('

    return latinize_url


@app.route('/')
def home():
    fact = get_fact()
    pig_latin_url = pig_latinate(fact)
    return redirect(pig_latin_url, code=302)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)