from pymongo import MongoClient
from urllib.parse import quote_plus
import re



Server = "prod"

if Server == "prod":
    username = "manojtomar326"
    password = "Tomar@@##123"
    cluster_url = "cluster0.ldghyxl.mongodb.net"

    encoded_username = quote_plus(username)
    encoded_password = quote_plus(password)

    connection_string = f"mongodb+srv://{encoded_username}:{encoded_password}@{cluster_url}/test?retryWrites=true&w=majority"
    CLIENT = MongoClient(connection_string)
    DB = CLIENT["LinkedIn_Scrapper"]
    COLLECTION = DB["New"]

    URL = "search/people?query=(spellCorrectionEnabled%3Atrue%2CrecentSearchParam%3A(id%3A2514245881%2CdoLogHistory%3Atrue)%2Cfilters%3AList((type%3ACURRENT_TITLE%2Cvalues%3AList((text%3Alearning%2520and%2520development%2CselectionType%3AINCLUDED)))%2C(type%3ACOMPANY_HEADCOUNT%2Cvalues%3AList((id%3AI%2Ctext%3A10%252C000%252B%2CselectionType%3AINCLUDED)))%2C(type%3AREGION%2Cvalues%3AList((id%3A102221843%2Ctext%3ANorth%2520America%2CselectionType%3AINCLUDED))))%2Ckeywords%3Alearning%2520%2526%2520development)&sessionId=P8mjcRoxTI%2Bys6v0A4iaOQ%3D%3D&viewAllFilters=true"


if Server == "dev":

    CLIENT = MongoClient("mongodb://localhost:27017")
    DB = CLIENT["LinkedIn_Scrapper"]
    COLLECTION = DB["New"]
    URL = "search/people?savedSearchId=1741602674&sessionId=UwGXMekGTFWTc%2F0l%2F1hsVQ%3D%3D&viewAllFilters=true"


domain = set()

data = COLLECTION.find({"email": False}, {"company_url":1})

for i in data:
    domain.add(i["company_url"])

for i in domain:
    print(domain_suffix_remover(i))
    











































# import re

# def remove_special_chars_and_enclosed_strings(input_string):
#     pattern = r'\[[^\]]*\]|\([^)]*\)|[^a-zA-Z ]+'
    
#     result = re.sub(pattern, '', input_string)
    
#     return ' '.join(result.split()) 


# input_string = "_.A_.n_.i_.p_._r_i_y_a😀 Ver💫ma (She/Her)"
# output_string = remove_special_chars_and_enclosed_strings(input_string)
# print(output_string) 

