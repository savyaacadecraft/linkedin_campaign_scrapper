from pymongo import MongoClient
from urllib.parse import quote_plus
from bson import ObjectId
from validate_email_own import PatternCheck

RECORD = set()

def email_operation():
    global RECORD
    DAILY_LIMIT = 1000

    data = COLLECTION.find({"email": False}, {"f_name":1, "l_name":1, "company_url":1}).limit(1)

    if len(data["company_url"]) <= 3: return False
    if str(data["_id"]) in RECORD:
        return False
    else:
        RECORD.add(str(data["_id"]))
    

    f_name = data["f_name"]
    l_name = data["l_name"]
    domain = data["company_url"]
    document_id = data["_id"]

    START_ID = 34
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



# for i in range(255):
#     email_operation()


data = COLLECTION.find({"email": False}, {"f_name": 1, "l_name": 1, "company_url": 1})
record_count = {"Long_Last_Name": 0, "No_Firm_URL": 0, "Valid_False": 0}

for i in data:
    if (len(i["l_name"].split(" ")) > 1):
        record_count["Long_Last_Name"] += 1
    elif (len(i["company_url"]) < 3):
        record_count["No_Firm_URL"] += 1
    else:
        print(i["_id"], i["f_name"], i["l_name"], i["company_url"], sep=" | ")

        record_count["Valid_False"] += 1

print(record_count)