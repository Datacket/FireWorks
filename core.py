import json 
import pandas as pd
import numpy as np
import pymysql
import pymysql.cursors as pycurse
from datetime import datetime
from flask import Flask,jsonify,request
app=Flask(__name__)
@app.route("/",methods=["POST"])
def reply():
    
	
