from flask import Flask
import os
from backend.models import*

app = None  #initially nonoe

def init_app():
    home_app=Flask(__name__, static_folder='static')  #instance of Flask
    
    home_app.debug=True
    home_app.secret_key = "Tripur@ri2268"  #session management
    home_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///homeservice.sqlite3"
    home_app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "static", "uploads")
    
    home_app.app_context().push()  #direct access app by others modules
   
    db.init_app(home_app)
    
    if not os.path.exists(home_app.config["UPLOAD_FOLDER"]):
        os.makedirs(home_app.config["UPLOAD_FOLDER"])
    print("Home service app is started")
    return home_app


app = init_app() 

from backend.controllers import *

if __name__ == "__main__":
    app.run()