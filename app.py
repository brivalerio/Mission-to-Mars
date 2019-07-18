from flask import Flask, render_template
from flask_pymongo import PyMongo
import mission_to_mars_scrape.py

app = Flask(__name__)

# Mongo connection
mongo = PyMongo(app,uri="mongod:localhost:27017/mars")

@appp.route("/")
def index():
    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", data = mars_data)

@app.route("/scrape")
def scrape():
    mars_data = mission_to_mars_scrape.scrape_all()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run()