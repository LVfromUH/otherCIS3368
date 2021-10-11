import mysql.connector
from mysql.connector import Error
from sql import create_connection
from sql import execute_query
from sql import execute_read_query
import flask
from flask import jsonify
from flask import request, make_response


#link to database, username, password, name of database (not database instance)
conn = create_connection("fall2021cis3368.cvrxk2eq0qdf.us-east-2.rds.amazonaws.com","admin","cis3368password","cis3368fall2021")
cursor = conn.cursor(dictionary=True)

#create table for celestialobjects
create_celestialobject_table = """
CREATE TABLE IF NOT EXISTS celestialobjects(
id INT AUTO_INCREMENT,
name VARCHAR(255) NOT NULL,
distance INT,
description VARCHAR(255) NOT NULL,
discoverydate DATE,
PRIMARY KEY (id)
)"""
execute_query(conn, create_celestialobject_table)

#setting up application name
app = flask.Flask(__name__) #sets up application
app.config["DEBUG"] = True #allow to show errors

celestial_sql = "SELECT * FROM celestialobjects"
celestials = execute_read_query(conn,celestial_sql)
#print(celestials)

@app.route('/', methods=['GET']) # default url without any routing as GET request
def home():
    return "<h1> Welcome to the Celestial Objects API! </h1>"

@app.route('/api/celestials/all', methods=['GET']) #get all celestials
def api_all():
    return jsonify(celestials)

#using POST to add celestial objects, method used in class to add cars
@app.route('/api/addcelestialobject', methods=['POST'])
def post_addcelestial():
    request_data = request.get_json()
    newname = request_data['name']
    newdistance = request_data['distance']
    newdescription = request_data['description']
    newdiscovery = request_data['discoverydate']
    #using post to input data into SQL
    add_statement = "INSERT INTO celestialobjects (name, distance, description, discoverydate) VALUES ('%s',%s,'%s','%s')"%(newname,newdistance,newdescription,newdiscovery)
    execute_query(conn,add_statement)
    return 'POST REQUEST WORKED'

#use POSt to delete celestial object
@app.route('/api/deletecelestialobject/<token>', methods=['POST'])
def post_deletecelestial(token):
    if token == "880e0d76": #given token that's required to access
        request_data = request.get_json()
        id_delete = request_data['id']
        #using post to delete data from SQL
        delete_statement = "DELETE FROM celestialobjects WHERE id = %s "%(id_delete)
        execute_query(conn,delete_statement)
        return 'POST REQUEST WORKED'
    else:
        return "INVALID ACCESS TOKEN"

#use get because my intention it to output data
@app.route('/api/getfurthestcelestialobject', methods=['GET'])
def get_furthestcelestialobject():
    #variable that will hold the furthest distance
    furthestdistance = 0
    #use forloop to find the furthest distance
    for celestialobject in celestials:
        if celestialobject['distance']>furthestdistance:
            furthestdistance=celestialobject['distance']
    #after finding furthest distance, i want to find celestial object with that distance and output it
    for celestialobject in celestials:
        if celestialobject['distance']==furthestdistance:
            return jsonify(celestialobject)

#use get method again because my intention it to output data
@app.route('/api/getmostrecentthree', methods=['GET'])
def get_threelatest():
    celestial_dates = []
    results=[]
    for celestial in celestials:
        celestial_dates.append(celestial['discoverydate'])
    celestial_dates.sort()
    celestial_dates.reverse()
   # return jsonify(celestial_dates)
   #thought process: make a list of the dates, sort it then reverse, get the first 3 values from the reversed list
    new_celestial_dates = celestial_dates[:3]
   # return jsonify(new_celestial_dates)
   #for loop that will search for celestial that has discovery date in the new celestial date list
    for celestial in celestials:
        if celestial['discoverydate']==new_celestial_dates[0] or celestial['discoverydate']==new_celestial_dates[1] or celestial['discoverydate']==new_celestial_dates[2]:
            results.append(celestial)
    #append the celestial with matching dates into results and output results
    return jsonify(results)

app.run()
