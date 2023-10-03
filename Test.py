from pymongo import MongoClient
from urllib.parse import quote_plus
from time import sleep
# from bson import ObjectId
from requests import post


def request_to_email_finder(first_name, last_name, domain, mongo_id):
    request_body = {
        "first_name": first_name,
        "last_name": last_name,
        "domain": domain,
        "mongo_id": str(mongo_id)
    }

    url = "http://0.0.0.0:9090/send_employee_details"
    try:
        post(url=url, json=request_body)
    except Exception as E:
        print(E)
        print("Execption while calling the API Function")



Server = "prod"

if Server == "prod":
    username = "manojtomar326"
    password = "Tomar@@##123"
    cluster_url = "cluster0.ldghyxl.mongodb.net"

    encoded_username = quote_plus(username)
    encoded_password = quote_plus(password)

    connection_string = f"mongodb+srv://{encoded_username}:{encoded_password}@{cluster_url}/test?retryWrites=true&w=majority"
    CLIENT = MongoClient(connection_string)
    DB = CLIENT["mydatabase"]
    COLLECTION = DB["Employee_Collection"]

    # URL = "search/people?query=(spellCorrectionEnabled%3Atrue%2CrecentSearchParam%3A(id%3A2514245881%2CdoLogHistory%3Atrue)%2Cfilters%3AList((type%3ACURRENT_TITLE%2Cvalues%3AList((text%3Alearning%2520and%2520development%2CselectionType%3AINCLUDED)))%2C(type%3ACOMPANY_HEADCOUNT%2Cvalues%3AList((id%3AI%2Ctext%3A10%252C000%252B%2CselectionType%3AINCLUDED)))%2C(type%3AREGION%2Cvalues%3AList((id%3A102221843%2Ctext%3ANorth%2520America%2CselectionType%3AINCLUDED))))%2Ckeywords%3Alearning%2520%2526%2520development)&sessionId=P8mjcRoxTI%2Bys6v0A4iaOQ%3D%3D&viewAllFilters=true"


# if Server == "dev":

#     CLIENT = MongoClient("mongodb://localhost:27017")
#     DB = CLIENT["LinkedIn_Scrapper"]
#     COLLECTION = DB["New"]
#     URL = "search/people?savedSearchId=1741602674&sessionId=UwGXMekGTFWTc%2F0l%2F1hsVQ%3D%3D&viewAllFilters=true"



data = COLLECTION.find({"verification": "pending"}, {"fname": 1, "lname": 1, "domain": 1, "_id": 1})

for i in data:
    try:
        print(i["fname"], i["lname"], i["domain"], i["_id"])
        request_to_email_finder(i["fname"], i["lname"], i["domain"], i["_id"])
        sleep(1)
    except KeyboardInterrupt:
        break















# visited_profiles = dict()
# duplicate_profiles = set()

# data = COLLECTION.find({"Scrapped_Time": {"$exists": True}}, {"profile_url": 1})


# for i in data:
#     profile_id = str(i["_id"])
#     profile_url = i["profile_url"]


#     if profile_url not in visited_profiles.keys():
#         visited_profiles[profile_url] = profile_id
#     else:
#         duplicate_profiles.add(profile_id)
    


# for i in visited_profiles.keys():
#     print(i, visited_profiles[i], sep=",", file=open("Original_Records_2.csv", "a"))

# for i in duplicate_profiles:
#     print(i, file=open("Duplicate.txt", "a"))
#     COLLECTION.delete_one({ "_id": ObjectId(i)})


































# import re

# def remove_special_chars_and_enclosed_strings(input_string):
#     pattern = r'\[[^\]]*\]|\([^)]*\)|[^a-zA-Z ]+'
    
#     result = re.sub(pattern, '', input_string)
    
#     return ' '.join(result.split()) 


# input_string = "_.A_.n_.i_.p_._r_i_y_a😀 Ver💫ma (She/Her)"
# output_string = remove_special_chars_and_enclosed_strings(input_string)
# print(output_string) 

