from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
mongo_username = os.getenv('MONGO_USERNAME')
mongo_password = os.getenv('MONGO_PASSWORD')

# client = MongoClient("mongodb+srv://" + mongo_username + ":" + mongo_password + "@cluster0.w6poc.mongodb.net/test?retryWrites=true&w=majority&authSource=admin")

# db=client.admin

# serverStatusResult=db.command("serverStatus")
# print(serverStatusResult)
# print(client.list_database_names())
# print(client["greenNet"].list_collection_names())

# client[database name][collection name]
# x = client["greenNet"]["data"].insert_one({"screen_name": "ASDF", "score": 0.0, "tokens": {"oauth": "XXXX_XXXX", "oauth2": "XXXX_XXXX"}})
# print(x)

def addUser(screen_name, oauth_token, oauth_secret, oauth_verifier, access_token_list):
    client = MongoClient("mongodb+srv://" + mongo_username + ":" + mongo_password + "@cluster0.w6poc.mongodb.net/test?retryWrites=true&w=majority&authSource=admin")
    x = client["greenNet"]["data"].insert_one({"screen_name": screen_name, "score": 0.0, "tokens": {"oauth_token": oauth_token, "oauth_secret": oauth_secret, "oauth_verifier": oauth_verifier, "access_token_list": access_token_list}, "recent_activity": {}})
    return x

def updatePoints(screen_name, points, classification):
    client = MongoClient("mongodb+srv://" + mongo_username + ":" + mongo_password + "@cluster0.w6poc.mongodb.net/test?retryWrites=true&w=majority&authSource=admin")
    currScore = getPoints(screen_name)
    newScore = currScore + points
    x = client["greenNet"]["data"].update_one({"screen_name": screen_name}, {"$set": {"score": newScore}})
    if classification != '':
        currActivity = get_recent_activity(screen_name)
        print('currAcc:', currActivity)
        currActivity[classification] = points
        newActivity = currActivity
        print("newACC: ", newActivity)
        x = client["greenNet"]["data"].update_one({"screen_name": screen_name}, {"$set": {"recent_activity": newActivity}})
    return getPoints(screen_name)

def getPoints(screen_name):
    client = MongoClient("mongodb+srv://" + mongo_username + ":" + mongo_password + "@cluster0.w6poc.mongodb.net/test?retryWrites=true&w=majority&authSource=admin")
    x = client["greenNet"]["data"].find_one({"screen_name": screen_name})
    return x["score"]

def get_access_token_list(screen_name):
    client = MongoClient("mongodb+srv://" + mongo_username + ":" + mongo_password + "@cluster0.w6poc.mongodb.net/test?retryWrites=true&w=majority&authSource=admin")
    x = client["greenNet"]["data"].find_one({"screen_name": screen_name})
    return x["tokens"]["access_token_list"]

def get_recent_activity(screen_name):
    client = MongoClient("mongodb+srv://" + mongo_username + ":" + mongo_password + "@cluster0.w6poc.mongodb.net/test?retryWrites=true&w=majority&authSource=admin")
    x = client["greenNet"]["data"].find_one({"screen_name": screen_name})
    print(x['recent_activity'])
    return x["recent_activity"] 