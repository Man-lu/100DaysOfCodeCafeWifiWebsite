from flask import Flask, render_template, redirect, url_for, request
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
import json

from api_routes import all_cafes


app = Flask(__name__)
Bootstrap(app)
fa = FontAwesome(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihccvsaBXox7C0sKR6b'


class AddCafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired()])
    map_url = StringField('Map Url', validators=[DataRequired()])
    has_sockets = BooleanField('Sockets', default="checked")
    has_wifi = BooleanField('Wifi', default="checked")
    seats = IntegerField('Seats', validators=[DataRequired()])
    coffee_price = FloatField('Coffee Price', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    response = requests.get(all_cafes)
    data = response.json()

    return render_template("index.html", cafes=data)


@app.route("/cafe/<id>")
def get_single_cafe(id):
    response = requests.get(f"{all_cafes}/{id}")
    data = response.json()
    return render_template("single_cafe.html", cafe=data)


@app.route("/<id>")
def delete_cafe(id):
    requests.delete(f"{all_cafes}/{id}")
    return redirect(url_for('home'))


@app.route("/cafes", methods=['POST'])
def search_cafes():
    location = request.form["location"]
    print(location)
    params = {"loc": location}
    response = requests.get("https://api-pretoria-cafe.herokuapp.com/api/cafes/search", params=params)
    data = response.json()
    return render_template("search_results.html", cafes=data, location=location)



@app.route("/cafe/add", methods=['GET', 'POST'])
def add_cafe():
    form = AddCafeForm()
    if form.validate_on_submit():
        new_cafe = {"name": form.name.data, "location": form.location.data, "img_url": form.img_url.data,
                    "map_url": form.map_url.data, "has_sockets": form.has_sockets.data,
                    "has_wifi": form.has_wifi.data,
                    "seats": form.seats.data, "coffee_price": form.coffee_price.data}

        headers = {"Content-Type": "application/json"}

        data = json.dumps(new_cafe)
        requests.post(all_cafes, data=data, headers=headers)
        print("post ran instead of update")
        return redirect(url_for('home'))
    return render_template("add.html", form=form, is_post = True)


@app.route("/cafe/edit/<id>", methods=['GET', 'POST'])
def edit_cafe(id):
    response = requests.get(f"{all_cafes}/{id}")
    data = response.json()

    form_edit = AddCafeForm(name=data["name"], location=data["location"],
                            img_url=data["img_url"],map_url=data["map_url"],
                            has_sockets=data["has_sockets"],has_wifi=data["has_wifi"],
                            seats=data["seats"], coffee_price=data["coffee_price"])

    if form_edit.validate_on_submit():
        headers = {"Content-Type": "application/json"}
        edited_cafe = {"name": form_edit.name.data, "location": form_edit.location.data,
                       "img_url": form_edit.img_url.data,"map_url": form_edit.map_url.data,
                       "has_sockets": form_edit.has_sockets.data,"has_wifi": form_edit.has_wifi.data,
                       "seats": form_edit.seats.data, "coffee_price": form_edit.coffee_price.data}

        data = json.dumps(edited_cafe)
        requests.put(f"{all_cafes}/{id}",data=data, headers=headers)
        return redirect(url_for('get_single_cafe', id=id))

    return render_template("add.html", form=form_edit, id=id)


if __name__ == "__main__":
    app.run(debug=True)