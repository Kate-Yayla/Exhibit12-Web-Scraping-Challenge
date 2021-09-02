from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
#import pandas as pd
import mars_scrape


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri = "mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars_data=mars)


@app.route("/scrape")
def scrape():
    mars=mongo.db.mars
    mars_data = mars_scrape.scrape()
    print(mars_data)
    mars.update({}, mars_data , upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)