from flask import Flask, render_template
import requests
from api_routes import all_cafes

app = Flask(__name__)


@app.route("/")
def home():
    response = requests.get(all_cafes)
    data = response.json()
    return render_template("index.html", cafes=data)


if __name__ == "__main__":
    app.run(debug=True)