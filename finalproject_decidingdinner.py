import mysql.connector
from mysql.connector import Error
from sql import create_connection
from sql import execute_query
from sql import execute_read_query
import flask
from flask import jsonify
from flask import request, make_response
import random

#link to database, username, password, name of database (not database instance)
conn = create_connection("fall2021cis3368.cvrxk2eq0qdf.us-east-2.rds.amazonaws.com","admin","cis3368password","cis3368fall2021")
cursor = conn.cursor(dictionary=True)

# create table for userprofile
create_userprofile_table = """
CREATE TABLE IF NOT EXISTS userprofile(
id INT AUTO_INCREMENT,
firstname VARCHAR(255) NOT NULL,
lastname VARCHAR(255) NOT NULL,
PRIMARY KEY (id)
)"""
execute_query(conn, create_userprofile_table)

# create table for restaurants
create_restaurants_table = """
CREATE TABLE IF NOT EXISTS restaurants(
id INT AUTO_INCREMENT,
name VARCHAR(255) NOT NULL,
PRIMARY KEY (id)
)"""
execute_query(conn, create_restaurants_table)

#setting up an application name
app = flask.Flask(__name__) 
app.config["DEBUG"] = True 

#extract restaurants from table
restaurants_SQL = "SELECT * FROM restaurants"
restaurants = execute_read_query(conn,restaurants_SQL)

@app.route('/', methods=['GET']) # default url 
def home():
    return "<h1> Homepage for restauraunt API. </h1>"

@app.route('/api/restaurants/all', methods=['GET']) #get all restaurants
def api_all():
    return jsonify(restaurants)

@app.route('/api/restaurants', methods=['GET']) #endppoint to get a single restaurant by id: http://127.0.0.1:5000/api/restaurants?id=1
def api_id():
    if 'id' in request.args: #only if an id is provided as an argument, proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: Not ID provided!'
    
    results = [] #resulting restaurant(s) to return
    for restaurant in restaurants: 
        if restaurant['id'] == id:
            results.append(restaurant)
    return jsonify(results)

#add a userprofile
@app.route('/api/adduserprofile', methods=['POST'])
def post_addcelestial():
    request_data = request.get_json()
    newfirstname = request_data['firstname']
    newlastname = request_data['lastname']
    #using post to input data into SQL
    add_statement = "INSERT INTO userprofile (firstname, lastname) VALUES ('%s','%s')"%(newfirstname,newlastname)
    execute_query(conn,add_statement)
    return 'POST REQUEST WORKED'

#updates useprofile and their names
@app.route('/api/changeprofile', methods=['POST'])
def post_changeprofile():
    request_data = request.get_json()
    input_id = request_data['id']
    newfirstname = request_data['firstname']
    newlastname = request_data['lastname']
    #using post to input data into SQL
    update_userstatement = "UPDATE userprofile SET firstname = '%s', lastname = '%s' WHERE id = %s"%(newfirstname,newlastname,input_id)
    execute_query(conn,update_userstatement)
    return 'POST REQUEST WORKED'

#using POST  to add restaurants
@app.route('/api/addrestaurant', methods=['POST'])
def post_addrestaurant():
    request_data = request.get_json()
    newname = request_data['name']
    #using post to input data into SQL
    add_statement = "INSERT INTO restaurants (name) VALUES ('%s')"%(newname)
    execute_query(conn,add_statement)
    return 'POST REQUEST WORKED'

#updates restaurant
#problem: have to access data FROM RESTAURANT TABLE???
@app.route('/api/changerestaurant', methods=['POST'])
def post_changeprofile():
    request_data = request.get_json()
    input_restid = request_data['restid']
    newrestname = request_data['name']
    #using post to input data into SQL
    update_reststatement = "UPDATE restaurants SET name = '%s' WHERE restid = %s"%(newrestname,input_restid)
    execute_query(conn,update_reststatement)
    return 'POST REQUEST WORKED'

#randomly select a resturant using random choice function
#reference: https://stackoverflow.com/questions/306400/how-can-i-randomly-select-an-item-from-a-list
@app.route('/api/selectedrestaurant',methods=['GET'])
def selected_restaurant():
    return (random.choice(restaurants))

app.run()