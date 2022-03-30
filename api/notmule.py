from this import s
from fastapi import APIRouter
import pymongo
from bson import ObjectId
notmule = APIRouter()

myclient = pymongo.MongoClient(
    "mongodb+srv://dhanushyp:.Coders#wow@cluster0.lshuz.mongodb.net")
db = myclient["dbdb"]
col = db["orders"]


@notmule.get("/await")
def root():
    orders=[]
    for x in db.orders.find({"sellerid":"6239e282d27797c9810aed12"},{'_id': 0}):
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





    
