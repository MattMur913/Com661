from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from pathlib import Path
from functools import wraps
from bson import BSON, json_util, ObjectId
from pymongo import MongoClient

import uuid, datetime, bcrypt
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.com661
dbClimbs = db.Climbs




app = Flask(__name__)
CORS(app)

#Collection from this point forward
@app.route("/api/v1.0/addComment/<string:uid>/routes/<string:rid>",methods=["POST"])
def addComment(uid, rid):
    try:
        if ObjectId.is_valid(uid) and ObjectId.is_valid(rid):
            if "username" in request.form and "comment" in request.form and "rating" in request.form:
                new_comment = {
                    "id": str(uuid.uuid4()),
                    "username": request.form["username"],
                    "comment": request.form["comment"],
                    "rating": request.form["rating"]
                }
                result = dbClimbs.update_one(
                    {"_id": ObjectId(uid), 'Routes._id': ObjectId(rid)},
                    {"$push": {"Routes.$.comments": new_comment}}
                )
                if result.matched_count == 1:
                    edited_area_url = "http://localhost:5000/api/v1.0/areas/" + uid + "/routes/" + rid
                    return make_response(jsonify({'url': edited_area_url}), 200)
                else:
                    return make_response(jsonify({'error': "Area not found"}), 404)
            else:
                return make_response(jsonify({'error': "Incomplete or missing data"}), 400)
        else:
            return make_response(jsonify({'error': "Invalid Area ID format"}), 404)
    except Exception as e:
        print(e)
        return make_response(jsonify({'error': "Internal Server Error"}), 500)
    
    
@app.route("/api/v1.0/comments/<string:aid>/routes/<string:rid>",methods=['GET'])
def getComments(aid,rid):
    if ObjectId.is_valid(aid) and ObjectId.is_valid(rid):
        commentlist=[]
        targetArea = dbClimbs.find_one({'_id':ObjectId(aid)},{'Routes':1})
        if targetArea != None:
            targetArea['_id'] = str(targetArea['_id'])
            for route in targetArea['Routes']:
                if route['_id'] == ObjectId(rid):
                    route['_id'] = str(route['_id'])
                    if 'comments' in route:
                        for comment in route['comments']:
                            commentlist.append(comment)
                        return make_response(jsonify(commentlist),200)
                    else:
                        return make_response(jsonify([]), 200)
        else:
            return make_response(jsonify({'error': "Area not found"}),404)
    else:
        return make_response(jsonify({'error': "Invalid Area ID provided"}),404) 

@app.route("/api/v1.0/deletecomment/<string:aid>/routes/<string:rid>/cid/<string:cid>",methods=['DELETE'])
def deleteComment(aid,rid,cid):
    if ObjectId.is_valid(aid) and ObjectId.is_valid(rid) :
        result = dbClimbs.update_one(
            {'_id': ObjectId(aid), 'Routes._id': ObjectId(rid)},
            {'$pull': {'Routes.$.comments': {'id': cid}}}
        )
        if result.matched_count == 1:
            
            return make_response(jsonify({}),204)
        else:
            return make_response(jsonify({'error': "Area not found"}),404)
    else:
        return make_response(jsonify({'error': "Invalid Area ID format"}),404)

#Areas API collection from here forawrd
@app.route("/api/v1.0/areas", methods=["GET"])
def getAreas():
    page_num, page_size = 1, 10
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))
    areaList=[]
    for eachArea in dbClimbs.find({}).skip(page_start).limit(page_size):
        eachArea['_id'] = str(eachArea['_id'])
        for routes in eachArea['Routes']:
            routes['_id'] = str(routes['_id'])
        areaList.append(eachArea)
    return make_response(jsonify(areaList),200)

@app.route("/api/v1.0/areas/<string:aid>", methods=["GET"])
def getArea(aid):
        eachArea = dbClimbs.find_one({'_id':ObjectId(aid)})
        if eachArea != None:
            eachArea['_id'] = str(eachArea['_id'])
            for routes in eachArea['Routes']:
                routes['_id'] = str(routes['_id'])
            return make_response(jsonify([eachArea]),200)
        else:
            return make_response(jsonify({'error':  "Area not found"}),404)

#Route API from here forward
@app.route("/api/v1.0/areas/<string:aid>/routes", methods=["GET"])
def getRoutes(aid):
    if ObjectId.is_valid(aid):
        routeList=[]
        targetArea = dbClimbs.find_one({'_id':ObjectId(aid)},{'Routes':1})
        if targetArea != None:
            targetArea['_id'] = str(targetArea['_id'])
            for route in targetArea['Routes']:
                route['_id'] = str(route['_id'])
                routeList.append(route)
            return make_response(jsonify(routeList),200)
        else:
            return make_response(jsonify({'error': "Area not found"}),404)
    else:
        return make_response(jsonify({'error': "Invalid Area ID provided"}),404)  

@app.route("/api/v1.0/areas/<string:aid>/routes/<string:rid>", methods=["GET"])
def getRoute(aid, rid):
    if ObjectId.is_valid(aid) and ObjectId.is_valid(rid):
        routeList=[]
        targetArea = dbClimbs.find_one({'_id':ObjectId(aid)},{'Routes':1})
        if targetArea != None:
            targetArea['_id'] = str(targetArea['_id'])
            for route in targetArea['Routes']:
                if route['_id'] == ObjectId(rid):
                    route['_id'] = str(route['_id'])
                    routeList.append(route)
                    return make_response(jsonify(routeList),200)
            if routeList != None:
                return make_response(jsonify({'error': "Route not found in this area"}),404)
        else:
            return make_response(jsonify({'error': "Area not found"}),404)
    else:
        return make_response(jsonify({'error': "Invalid Area ID provided"}),404)         

@app.route("/api/v1.0/areas/<string:aid>/routes", methods=["POST"])
def addRoute(aid):
    if ObjectId.is_valid(aid):
        if "route_name" in request.form and \
            "Location" in request.form and \
            "RouteType" in request.form and \
            "Grade" in request.form and \
            "Pitches" in request.form and \
            "Length" in request.form in request.form:
            result = dbClimbs.update_one({ "_id" : ObjectId(aid) }, {
                "$push" : {"Routes":{" Route" : request.form["route_name"],
                " Location" : request.form["Location"],
                " RouteType" : request.form["RouteType"],
                " Grade" : request.form["Grade"],
                " Pitches":request.form["Pitches"],
                " Length": request.form["Length"]
                }
            }} )
            added_area_url = "http://localhost:5000/api/v1.0/areas/"+aid+"/routes/"+result
            return make_response(jsonify({'url':added_area_url}),200)
        else:
            return make_response(jsonify({'error':"Area not found"}),404)
    else:
        return make_response(jsonify({'error': "Invalid Area ID provided"}),404)  
    
@app.route("/api/v1.0/areas/<string:aid>/routes/<string:rid>", methods=["PUT"])
def updateRoute(aid,rid):
    if ObjectId.is_valid(aid) and ObjectId.is_valid(rid):
        if "Route" in request.form and \
            "RouteType" in request.form and \
            "Grade" in request.form and \
            "Pitches" in request.form and \
            "Length" in request.form:
            result = dbClimbs.update_one({ "_id" : ObjectId(aid), 'Routes._id': ObjectId(rid) }, {
                "$set" : {"Routes.$.Route" : request.form["Route"],
                "Routes.$.RouteType" : request.form["RouteType"],
                "Routes.$.Grade" : request.form["Grade"],
                "Routes.$.Pitches" : request.form["Pitches"],
                "Routes.$.Length":request.form["Length"]
            }} )
            if result.matched_count==1:
                edited_area_url = "http://localhost:5000/api/v1.0/areas/"+aid+"/routes/"+rid
                return make_response(jsonify({'url':edited_area_url}),200)
            else:
                return make_response(jsonify({'error':"Area not found"}),404)
        else:
           return make_response(jsonify({'error':"Data not found"}),404)
    else:
        return make_response(jsonify({'error': "Invalid Area ID format"}),404)

@app.route("/api/v1.0/deleteroute/<string:aid>/routes/<string:rid>", methods=["DELETE"])
def deleteRoute(aid,rid): 
    if ObjectId.is_valid(aid) and ObjectId.is_valid(rid) :
        result = dbClimbs.update_one({'_id':ObjectId(aid)},{'$pull':{'Routes' : {'_id':ObjectId(rid)}},
                '$inc': {'routeCount': -1} }) 
        if result.matched_count == 1:
            
            return make_response(jsonify({}),204)
        else:
            return make_response(jsonify({'error': "Area not found"}),404)
    else:
        return make_response(jsonify({'error': "Invalid Area ID format"}),404)


if __name__ == "__main__":
    app.run(debug=True)