from flask import Flask 
from flask import render_template, flash, redirect, url_for
  
app = Flask(__name__) 
  
@app.route("/") 
def home_view(): 
        return render_template('index.html')