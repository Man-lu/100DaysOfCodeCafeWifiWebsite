from flask import Flask, render_template, redirect, url_for
import requests
from api_routes import all_cafes


app = Flask(__name__)


@app.route("/")
def home():
    response = requests.get(all_cafes)
    data = response.json()
    return render_template("index.html", cafes=data)


@app.route("/cafe/<id>")
def get_single_cafe(id):
    response = requests.get(f"{all_cafes}/{id}")
    data = response.json()
    print("get ran")
    return render_template("single_cafe.html", cafe=data)


@app.route("/<id>")
def delete_cafe(id):
    requests.delete(f"{all_cafes}/{id}")
    return redirect(url_for('home'))


@app.route("/cafes/<location>")
def search_cafes(location):
    PARAMS = {"loc": location}
    response = requests.get("https://api-pretoria-cafe.herokuapp.com/api/cafes/search", params=PARAMS)
    data = response.json()
    return render_template("search_results.html", cafes=data)


if __name__ == "__main__":
    app.run(debug=True)