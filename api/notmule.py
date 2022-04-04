import imp
from this import s
from fastapi import APIRouter
from fastapi import Request, FastAPI
import pymongo
from bson import json_util, ObjectId
import os
from dotenv import load_dotenv
import json
notmule = APIRouter()

load_dotenv()
mongourl = os.getenv("MONGO")


myclient = pymongo.MongoClient(
    mongourl,)
db = myclient["db1"]
col = db["orders"]


@notmule.post("/await")
async def aww(request: Request):
    re = (await request.json())
    print(re)
    orders = []
    dat = db.orders.find({"sellerid": re["sellerid"]})
    dat_san = json.loads(json_util.dumps(dat))

    for x in dat_san:
        orders.append(x)

    for user in orders:

        buy = db.users.find_one({"_id": ObjectId(user["buyerid"])}, {'_id': 0})
        user["buyerName"] = buy["username"]
        user["avatarURL"] = buy["avatarURL"]
    for item in orders:
        listing = db.users.find_one({"_id": ObjectId(
            item["sellerid"]), "listings.id": item["listingid"]}, {"listings.$": 1, '_id': 0})
        item["title"] = listing["listings"][0]["oname"]
        item["price"] = listing["listings"][0]["oprice"]

    return orders


@notmule.post("/previous-orders")
async def prevv(request: Request):
    re = (await request.json())
    print(re)
    orders = []
    dat = db.orders.find({"buyerid": re["userid"]})
    dat_san = json.loads(json_util.dumps(dat))

    for x in dat_san:
        orders.append(x)

    for user in orders:

        buy = db.users.find_one({"_id": ObjectId(user["buyerid"])}, {'_id': 0})
        user["sellerName"] = buy["username"]

    for item in orders:
        listing = db.users.find_one({"_id": ObjectId(
            item["sellerid"]), "listings.id": item["listingid"]}, {"listings.$": 1, '_id': 0})
        item["title"] = listing["listings"][0]["oname"]
        item["price"] = listing["listings"][0]["oprice"]
        item["imgURL"] = listing["listings"][0]["opic"]

    return orders


@notmule.post("/orderstat")
async def stat(request: Request):
    re = (await request.json())
    print(re)
    db.orders.update_one({"_id": ObjectId(re["orderid"])}, {
                         "$set": {"status": re["status"]}})

    return {"message": "success"}

@notmule.post("/teams")
async def teams(request: Request):
    re = (await request.json())
    print(re)
    teams = []
    dat = db.users.find({"skill": (re["skill"])})
    dat_san = json.loads(json_util.dumps(dat))

    for x in dat_san:
        del x["password"]
        teams.append(x)
        

    return teams