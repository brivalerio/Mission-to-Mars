from flask import Flask, render_template
from flask_pymongo import PyMongo
import mission_to_mars_scrape.py

app = Flask(__name__)



if __name__ == "__main__":
    app.run()