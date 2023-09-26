from pymongo import MongoClient

CLIENT = MongoClient("mongodb://localhost:27017")

DB = CLIENT["LinkedIn_Scrapper"]
COLLECTION = DB["Temp"]






# obj = COLLECTION.insert_one({"f_name": "Savya", "l_name": "Sachi"})
# print(obj.inserted_id)


# COLLECTION.update_one({"_id": obj.inserted_id}, {"$set": {"email": "savya@acadecraft.net"}})



# import re

# def remove_special_chars_and_enclosed_strings(input_string):
#     pattern = r'\[[^\]]*\]|\([^)]*\)|[^a-zA-Z ]+'
    
#     result = re.sub(pattern, '', input_string)
    
#     return ' '.join(result.split()) 


# input_string = "_.A_.n_.i_.p_._r_i_y_a😀 Ver💫ma (She/Her)"
# output_string = remove_special_chars_and_enclosed_strings(input_string)
# print(output_string) 

