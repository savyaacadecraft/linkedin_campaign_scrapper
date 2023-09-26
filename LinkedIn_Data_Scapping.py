from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

from time import sleep
from random import randint
from urllib.parse import quote_plus
from pymongo import MongoClient
import requests
import re



username = "manojtomar326"
password = "Tomar@@##123"
cluster_url = "cluster0.ldghyxl.mongodb.net"

# Encode the username and password using quote_plus()
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

# Create the MongoDB Atlas connection string with the encoded credentials
connection_string = f"mongodb+srv://{encoded_username}:{encoded_password}@{cluster_url}/test?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
CLIENT = MongoClient(connection_string)
DB = CLIENT["LinkedIn_Scrapper"]
COLLECTION = DB["New"]

def name_filter(input_string):
    pattern = r'\[[^\]]*\]|\([^)]*\)|[^a-zA-Z ]+'
    
    result = re.sub(pattern, '', input_string)
    
    return ' '.join(result.split()) 

def login(engine):
    username: str = "shubhamtomar033@gmail.com"
    password: str = "Acadecraft@12"

    engine.get("https://www.linkedin.com/?sign_in")
    sleep(5)

    engine.find_element(By.ID, "session_key").send_keys(username)
    sleep(1)

    engine.find_element(By.ID, "session_password").send_keys(password)
    sleep(1)

    engine.find_element(By.XPATH, '//button[@type="submit"]').click()
    sleep(5)
    input("Enter: ")

def apollo_code(engine, url):

    try:
        sleep(3)
        engine.execute_script("window.open('', '_blank');")
        sleep(1)
        engine.switch_to.window(engine.window_handles[1])
        engine.get(url)
    except Exception as E:
        print("Inside Apollo:")


    sleep(randint(0, 3))

    try:
        WebDriverWait(engine, 2).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Sign in')]")))
        print(datetime.now(), file=open("BLOCK_COUNTER.txt", "a"))
        # engine.save_screenshot(f'{datetime.now().strftime("%Y-%m-%dT%H:%M:%S.png")}')
        engine.close()
        engine.switch_to.window(engine.window_handles[0])
        
    
    except:
        # Searching for the Apollo Box for Checking
        try:
            WebDriverWait(engine, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "apollo-opener-icon"))).click()
        except Exception as E:
            print("Element not appeared by 10 Seconds Error.....")

        # Clicking on the View email address Textarea
        try:
            WebDriverWait(engine, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'View email address')]"))).click()
        except Exception as E:
            print("Clickable Text for Display Email was not found....")

        try:
            email = WebDriverWait(engine, 2).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[13]/div/div[2]/div/div/div[4]/div/div[1]/div[1]/div[3]/div[1]/div/div[1]/div/div[2]/div/div/span/div"))).text
            if email != "Verifying":

                # print(name, url, email, sep=",", file=open("Apollo_Email.csv", "a"))

                engine.close()
                engine.switch_to.window(engine.window_handles[0])

                return email
                
            else:
                email = "Not Found"
                # print(name, url, email, sep=",", file=open("Apollo_Email.csv", "a"))

                engine.close()
                engine.switch_to.window(engine.window_handles[0])

                return email
                

        except Exception as E:
            email = "Not Found"
            # print(name, url, email, sep=",", file=open("Apollo_Email.csv", "a"))

            engine.close()
            engine.switch_to.window(engine.window_handles[0])

            return email

def get_industry_and_head_count(engine, Company_URL):


    try:
        sleep(1.5)
        engine.execute_script("window.open('', '_blank');")
        engine.switch_to.window(engine.window_handles[1])

        url = Company_URL + "/about"
        engine.get(url)

        sleep(1)
    except Exception as E:
        print("Exception: ", Company_URL)
        # print(E)

        engine.close()
        engine.switch_to.window(engine.window_handles[0])

        return ("", "", "")

    try:
        head_count = engine.find_element(By.CLASS_NAME, "link-without-hover-state").text
        head_count = head_count.replace(" employees", "").replace(",", "")
    except Exception as E:
        head_count = ""
        print(Company_URL)
        print("Head Count Not Found")

    try:
        industry_text = engine.find_element(By.XPATH, "//dt[text() = 'Industry']")
        sleep(0.5)

        industry_name = industry_text.find_element(By.XPATH, 'following-sibling::*[1]').text
        industry_name = industry_name.replace(",", " ")
            
    except Exception as E:
        industry_name = ""
        print(Company_URL)
        print("Industry Not Found")
        
    try:
        website = engine.find_element(By.CLASS_NAME, "org-top-card-primary-actions__inner")
        site = website.find_element(By.TAG_NAME, "a").get_attribute("href")
        sleep(0.5)
    except Exception as E:
        print("website not found: ", Company_URL)
        site = ""

    engine.close()
    engine.switch_to.window(engine.window_handles[0])

    return (head_count, industry_name, site)

def request_to_email_finder(first_name, last_name, domain, mongo_id):
    request_body = {
        "first_name": first_name,
        "last_name": last_name,
        "domain": domain,
        "mongo_id": str(mongo_id)
        }

    url = "http://0.0.0.0:9000/send_employee_details"
    try:
        requests.post(url= url, json=request_body)
    except Exception as E:
        print(E)
        print("Execption while calling the API Function")
  
def priyam_code(driver, URL):
    global COLLECTION
    
    Company_Dict = dict()

    def Wait(xpth):
        return WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpth)))

    driver.get(URL)
    sleep(8)
    i = 0
    
    while i<50:
        # input("Enter: ")
        try:
            
            url=driver.find_element(by=By.XPATH,value=f'/html/body/main/div[1]/div[2]/div[2]/div/ol/li[{i+1}]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/a')
            title = driver.find_elements(by=By.CSS_SELECTOR,value=f'span[data-anonymize="person-name"]')[i].get_attribute('innerText')
            title = name_filter(title)
            f_name = title.split(" ")[0]
            l_name = " ".join(title.split(" ")[1:])
            desn = driver.find_elements(by=By.CSS_SELECTOR,value=f'span[data-anonymize="title"]')[i].get_attribute('innerText')

            desn = desn.replace(",", "|")
            profile_url = url.get_attribute('href')
            profile_url_id = profile_url.split("lead/")[1].split(",")[0]
            newProfileUrl = f'https://www.linkedin.com/in/{profile_url_id}'

            try:
                firm = driver.find_element(by=By.XPATH, value=f'/html/body/main/div[1]/div[2]/div[2]/div/ol/li[{i+1}]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[2]/a')
                firm_name = firm.get_attribute('innerText')
                firm_name = firm_name.replace(",", "|")
                firm_url = firm.get_attribute("href")
                firm_url = firm_url.split("?")[0].replace("/sales", "")
                
            except Exception as E:
                print(E)
                print("Firm name not found")
            
            try:
                if firm_url in Company_Dict.keys():
                    head_count, industry, site = Company_Dict[firm_url]
                else:
                    Company_Dict[firm_url] = get_industry_and_head_count(driver, firm_url)
                    head_count, industry, site = Company_Dict[firm_url]
                    
            except Exception as E:
                head_count = ""
                industry = ""
                site = ""
                print("Company Details Not Found", firm_url)

            try:
                location = driver.find_elements(by=By.CSS_SELECTOR, value=f'span[data-anonymize="location"]')[i].get_attribute('innerText')
                location = location.replace("," , "|")
            except Exception as E:
                print(E)
                print("location not found")

            try:
                obj = COLLECTION.insert_one({"f_name": f_name, "l_name": l_name, "designation": desn, "profile_url": newProfileUrl, "email": "Not Found", "email_source": "", "location": location, "company_name": firm_name, "company_linkedin_url": firm_url, "company_head_count":head_count, "industry": industry, "company_url": site, "search_url": URL})
            except Exception as E:
                print(E)
                print("Error while Inserting data in DB")

            try:
                email = apollo_code(driver, newProfileUrl)
                
            except Exception as E:
                print("Apollo Error: ", E)
                email = "Not Found"
            
            try:
                if email == "Not Found":
                    request_to_email_finder(f_name, l_name, site, obj.inserted_id)
                else:
                    COLLECTION.update_one({"_id": obj.inserted_id}, {"$set": {"email": email, "email_source": "apollo"}})
                    pass
            except Exception as E:
                print(E)
                print("Error while calling Email Finder API")

            # print(f_name, l_name, desn, newProfileUrl, email, location, firm_name, firm_url, head_count, industry, site, sep=",", file=open("All_Data.csv", "a"))

            print(f"i: {i} and Updating- {title}")
            try:
                # driver.implicitly_wait(2)
                sleep(1)
                driver.execute_script("arguments[0].scrollIntoView();", url)
            except Exception:
                pass
        except Exception as e:
            driver.implicitly_wait(5)

            print(e)
            try:
                print('Page Change')
                # page+=1☻
                i=-1
                try:
                    driver.execute_script("window.scrollBy(0, 1000);")  
                    sleep(1)
                    driver.execute_script("arguments[0].scrollIntoView();", url)
                except Exception:
                    pass
                Wait('/html/body/main/div[1]/div[2]/div[2]/div/div[4]/div/button[2]')
                driver.find_element(by=By.XPATH,value=f'/html/body/main/div[1]/div[2]/div[2]/div/div[4]/div/button[2]').click()

            except:
                pass
        i+=1


if __name__ == "__main__":

    URL_1 = "https://www.linkedin.com/sales/search/people?savedSearchId=1741602674&sessionId=UwGXMekGTFWTc%2F0l%2F1hsVQ%3D%3D&viewAllFilters=true"

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")

    options.add_experimental_option("debuggerAddress", "localhost:9999")
    service = Service("/home/lightning_sin_wrath/chromedriver")

    engine = webdriver.Chrome(service=service, options=options)
    engine.maximize_window()

    print("Operation Started-----")
    priyam_code(engine, URL_1)
