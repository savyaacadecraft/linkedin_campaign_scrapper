from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from uvicorn import run

from pymongo import MongoClient
from urllib.parse import quote_plus
from bson import ObjectId

from threading import Thread, Lock
from time import sleep
from datetime import datetime
from validate_email_own import PatternCheck


app = FastAPI()

EMAIL_LIST = None
LIST_LOCK = None

ID_LIST = None
ID_LOCK = None

ID_RECORD = None
ID_RECORD_LOCK = None


username = "manojtomar326"
password = "Tomar@@##123"
cluster_url = "cluster0.ldghyxl.mongodb.net"

encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

connection_string = f"mongodb+srv://{encoded_username}:{encoded_password}@{cluster_url}/test?retryWrites=true&w=majority"

# connection_string = "mongodb://localhost:27017/"
CLIENT = MongoClient(connection_string)
DB = CLIENT["LinkedIn_Scrapper"]
COLLECTION = DB["New"]

def printf(*args):
    print(*args, file=open("Email_Server.txt", "a"))

class emp_details(BaseModel):
    first_name:str
    last_name:str
    domain:str
    mongo_id:str


def verify_email(f_name, l_name, site, user_id, ID):
    global COLLECTION, ID_LIST, ID_LOCK, ID_RECORD, ID_RECORD_LOCK

    printf(f"TIME:: {datetime.now()} ", f_name, l_name, site, user_id, ID)

    try:
        _, email, counter = PatternCheck(first_name=f_name, last_name=l_name, domain=site, _idnum=ID)
    except Exception as E:
        printf(E)
        counter = 0
        email = None
    
    ID_RECORD_LOCK.acquire()
    ID_RECORD[ID] -= counter
    ID_RECORD_LOCK.release()

    ID_LOCK.acquire()
    ID_LIST.append(ID)
    ID_LOCK.release()

    if email:
        COLLECTION.update_one({"_id": ObjectId(user_id)}, {"$set": {"email": email, "verification": True}})
        printf(f"TIME:: {datetime.now()} | verification - True | id: {user_id}  |  EMAIL_ID ::: {ID}")
    else:
        COLLECTION.update_one({"_id": ObjectId(user_id)}, {"$set": {"email": email, "verification": False}})
        printf(f"TIME:: {datetime.now()} | verification - False | id: {user_id}  |  EMAIL_ID ::: {ID}")


def email_operation():
    global EMAIL_LIST, LIST_LOCK, ID_LIST, ID_LOCK, ID_RECORD, ID_RECORD_LOCK

    while True:

        if len(EMAIL_LIST):

            LIST_LOCK.acquire()
            user_data = EMAIL_LIST.pop(0)
            LIST_LOCK.release()

            f_name = user_data[0]
            l_name = user_data[1]
            domain = user_data[2]
            document_id = user_data[3]

            email_id = None

            while True:

                if len(ID_LIST):
                    ID_LOCK.acquire()
                    ID = ID_LIST.pop()
                    ID_LOCK.release()

                    if ID_RECORD[ID] >= 16:
                        email_id = ID
                        break
            
            Thread(target=verify_email, args=(f_name, l_name, domain, document_id, email_id)).start()


@app.post("/send_employee_details")
async def push_to_email_queue(details: emp_details):
    global EMAIL_LIST, LIST_LOCK

    try:
        LIST_LOCK.acquire()
        EMAIL_LIST.append((details.first_name, details.last_name, details.domain, details.mongo_id))
        LIST_LOCK.release()
        return {"response": "Success"}
    except Exception as E:
        printf(E)
        return {"response": "Failed"}


@app.get("/get_all_data")
async def get_url_data(URL: str):

    data = COLLECTION.find({"$text": {"$search": URL}}, {"_id": 0, "f_name":1, "l_name":1, "designation":1, "email":1,"location":1, "company_name":1, "company_head_count":1, "industry": 1, "company_url":1})
    cols = ["first_name", "last_name", "designation", "email", "location", "company_name", "head_count", "industry", "company_url"]
    print(", ".join(cols), file=open("Data.csv", "w"))
    

    for i in data:
        print(i["f_name"], i["l_name"], i["designation"], i["email"], i["location"], i["company_name"], i["company_head_count"], i["industry"], i["company_url"], sep=", ",  file=open("Data.csv", "a"))

    
    return FileResponse("Data.csv", filename="Data.csv")
    

if __name__ == "__main__":
    EMAIL_LIST = list()
    LIST_LOCK = Lock()

    ID_LIST = [i for i in range(1, 52)]
    ID_LOCK = Lock()

    ID_RECORD = {k:1000 for k in ID_LIST}
    ID_RECORD_LOCK = Lock()

    printf(ID_LIST)
    printf(ID_RECORD)

    Thread(target=email_operation).start()

    run(app, host="0.0.0.0", port=9898)
