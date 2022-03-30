import imp
from this import s
from fastapi import APIRouter
import pymongo
from bson import ObjectId
import os
from dotenv import load_dotenv
notmule = APIRouter()

load_dotenv()
mongourl=os.getenv("MONGO")


myclient = pymongo.MongoClient(
    mongourl,)
db = myclient["dbdb"]
col = db["orders"]


@notmule.post("/await")
def aww(payload:dict):
    sell = payload["sellerid"]

    orders=[]
    for x in db.orders.find({"sellerid":sell},{'_id': 0}):
        orders.append(x)
    for user in orders:
        
        buy = db.users.find_one({"_id": ObjectId(user["buyerid"])},{'_id': 0})
        user["buyerName"] = buy["username"]
        user["avatarURL"] = buy["avatarURL"]
    for item in orders:
        listing = db.users.find_one({"_id": ObjectId(item["sellerid"]),"listings.id":item["listingid"]},{"listings.$":1,'_id': 0})
        item["title"] = listing["listings"][0]["oname"]
        item["price"] = listing["listings"][0]["oprice"]
        print(listing)

    return orders





    
