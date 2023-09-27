from pymongo import MongoClient
from urllib.parse import quote_plus
from bson import ObjectId
from validate_email_own import PatternCheck


def email_operation(data):
    DAILY_LIMIT = 1000

    for i in data:
        if len(i["company_url"]) <= 3: continue
        print(i["_id"], i["f_name"], i["l_name"], i["company_url"])

        f_name = i["f_name"]
        l_name = i["l_name"]
        domain = i["company_url"]
        document_id = i["_id"]

        START_ID = 31
        MAX_ID = 40

        while (START_ID <= MAX_ID):
            try:
                _, email, counter = PatternCheck(first_name=f_name, last_name=l_name, domain=domain, _idnum=START_ID)
                break
                
            except Exception as E:
                print("Exception Occoured :::", E)
                
        if counter > DAILY_LIMIT:
            START_ID += 1
            
        if email:
            COLLECTION.update_one({"_id": ObjectId(document_id)}, {"$set": {"email": email, "email_source": "email_finder"}})
        else:
            COLLECTION.update_one({"_id": ObjectId(document_id)}, {"$set": {"email": False, "email_source": "email_finder"}})


username = "manojtomar326"
password = "Tomar@@##123"
cluster_url = "cluster0.ldghyxl.mongodb.net"

encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

connection_string = f"mongodb+srv://{encoded_username}:{encoded_password}@{cluster_url}/test?retryWrites=true&w=majority"

CLIENT = MongoClient(connection_string)
DB = CLIENT["LinkedIn_Scrapper"]
COLLECTION = DB["New"]


data = COLLECTION.find({"email": False}, {"f_name":1, "l_name":1, "company_url":1})    

email_operation(data)
