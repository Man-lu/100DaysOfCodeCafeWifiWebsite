from flask import Flask, render_template
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
    print(data)
    return render_template("single_cafe.html", cafe=data)


if __name__ == "__main__":
    app.run(debug=True)