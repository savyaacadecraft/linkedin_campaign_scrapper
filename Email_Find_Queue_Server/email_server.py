from fastapi import FastAPI
from pydantic import BaseModel
from uvicorn import run

from pymongo import MongoClient
from bson import ObjectId
from threading import Thread, Lock


from validate_email_own import PatternCheck


app = FastAPI()

EMAIL_LIST = None
LIST_LOCK = None

CLIENT = MongoClient("mongodb://localhost:27017")
DB = CLIENT["LinkedIn_Scrapper"]
COLLECTION = DB["Temp"]

class emp_details(BaseModel):
    first_name:str
    last_name:str
    domain:str
    mongo_id:str

def email_operation():
    global EMAIL_LIST, LIST_LOCK, COLLECTION
    DAILY_LIMIT = 1000

    while True:

        if len(EMAIL_LIST):
            print("EMAIL_LIST: ", EMAIL_LIST)

            LIST_LOCK.acquire()
            user_data = EMAIL_LIST.pop(0)
            LIST_LOCK.release()

            f_name = user_data[0]
            l_name = user_data[1]
            domain = user_data[2]
            document_id = user_data[3]

            START_ID = 40
            MAX_ID = 50

            while (START_ID <= MAX_ID):
                try:
                    _, email, counter = PatternCheck(first_name=f_name, last_name=l_name, domain=domain, _idnum=START_ID)
                    break

                except Exception as E:
                    if "Refresh problem"  in E:
                        NULL_COUNTER += 1
                        if NULL_COUNTER >= 4:
                            return False

                        else:
                            NULL_COUNTER = 0


            if counter > DAILY_LIMIT:
                START_ID += 1

            if email:
                COLLECTION.update_one({"_id": ObjectId(document_id)}, {"$set": {"email": email, "email_source": "email_finder"}})
            else:
                COLLECTION.update_one({"_id": ObjectId(document_id)}, {"$set": {"email": False, "email_source": "email_finder"}})


@app.post("/send_employee_details")
async def push_to_email_queue(details: emp_details):
    global EMAIL_LIST, LIST_LOCK
    print("1")
    try:
        LIST_LOCK.acquire()
        print("2")
        EMAIL_LIST.append((details.first_name, details.last_name, details.domain, details.mongo_id))
        LIST_LOCK.release()
        print("3")
        return {"response": "Success"}
    except Exception as E:
        print(E)
        print("4")
        return {"response": "Failed"}


@app.get("/get_all_data")
async def get_url_data(URL: str):
    
    pass

if __name__ == "__main__":
    EMAIL_LIST = list()
    LIST_LOCK = Lock()


    Thread(target=email_operation).start()

    run(app, host="0.0.0.0", port=9000)
