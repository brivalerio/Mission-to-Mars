from flask import Flask, render_template
from flask_pymongo import PyMongo
import mission_to_mars_scrape.py

app = Flask(__name__)

@appp.route("/")
def index():

@app.route("/scrape")
def scrape():
    mars_data = mission_to_mars_scrape.scrape_all()

if __name__ == "__main__":
    app.run()