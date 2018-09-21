# dependencies
from flask import Flask, render_template, jsonify, redirect
import pymongo
from pymongo import MongoClient
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = MongoClient("mongodb://localhost:27017")
db = client.mars_db
collection = db.mars_info

@app.route("/")
def index():
    mars = db.mars_info.find_one()
    return render_template("index.html", mars = mars)


# route for trigger scrape functions
@app.route("/scrape")
def scrape():
    mars = db.mars_info
    data=scrape_mars.scrape()
    mars.update({}, data, upsert=True)

    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True