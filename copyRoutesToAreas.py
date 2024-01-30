from bson import ObjectId
from flask import Flask, make_response, jsonify, request
from pymongo import MongoClient, cursor
import uuid, datetime, bcrypt
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.com661
dbAreas = db.Climbs
dbRoutes = db.Fixing

num_processed = 0

#Added the routes to the areas file
for area in dbAreas.find({},no_cursor_timeout=True):
    print(num_processed)
    area_routes=[]
    for route in dbRoutes.find({"Location":area["Area"]}):
        area_routes.append(route)
    dbAreas.update_one({"Area":area["Area"]}, 
                       {"$set":{"Routes":area_routes, "RouteCount" : len(area_routes)}})
    num_processed = num_processed +1
    if num_processed % 1000 == 0 :
        print(str(num_processed) + " routes processed")

