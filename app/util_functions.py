from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
from selenium.common.exceptions import TimeoutException
import tempfile
import requests

import os
import logging

def start_driver() -> webdriver.Chrome:

    s = Service("/bin/chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
    options.add_argument("start-maximized")
    # options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/95.0.4638.54 Safari/537.36")
    # options.add_argument("--disable-blink-features=AutomationControlled")

    # options.add_argument("window-size=1200x600")
    driver = webdriver.Chrome(service=s, options=options)
    # driver = webdriver.Chrome(
    #     'chromedriver', options=options)

    return driver


def random_phone(format=None, area_codes=[800]):
    
    # print(area_codes)
    
    area_code = str(random.choice(area_codes))
    # print(area_code)

    middle_three = str(random.randint(0,999)).rjust(3,'0')
    last_four = str(random.randint(0,9999)).rjust(4,'0')

    if format is None:
        format = random.randint(0,4)

    if format==0:
        return area_code+middle_three+last_four
    elif format==1:
        return area_code+' '+middle_three+' '+last_four
    elif format==2:
        return area_code+'.'+middle_three+'.'+last_four
    elif format==3:
        return area_code+'-'+middle_three+'-'+last_four
    elif format==4:
        return '('+area_code+') '+middle_three+'-'+last_four   

def random_email(fake_name: dict) -> str:
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com', 'icloud.com']
    
    prefix = fake_name["first_name"].lower() + fake_name["last_name"].lower() + str(random.randint(1, 1000))
    
    return prefix + '@' + random.choice(domains) 

def generate_fake_identity(fake: Faker) -> dict:
    
    
    
    # pick a random line from the file
    with open("data/zip_data.tsv", "r") as f:
        lines = f.readlines()
        local_data = random.choice(lines).strip().split("\t")
        
    print(local_data)
    
    name = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
    }
    fake_identity = {
        "first_name": name["first_name"],
        "last_name": name["last_name"],
        "email": random_email(name),
        "phone": random_phone(format=0, area_codes=local_data[3].split(",")),
        "address": fake.street_address(),
        "city": fake.city(),
        "state": local_data[1],  # Use the generated state abbreviation
        "zip": local_data[0],  # Generate a zip code for the specific state
        "county": local_data[2],  # Use the generated county name
    }
        

    return fake_identity

DOM_ELEMENTS = {
    "first_name": (By.ID, "info.firstName"),
    "last_name": (By.ID, "info.lastName"),
    "email": (By.ID, "info.email"),
    "phone": (By.ID, "info.cellPhone"),
    "address": (By.ID, "public-site-address-address-1"),
    "city": (By.ID, "public-site-address-city"),
    "state": (By.ID, "public-site-address-us-state"),
    "zip": (By.ID, "public-site-address-zip"),
}


def addTracking():
    # send post request
    r = requests.post("https://fight-tracking.gz4c.org")
    if r.status_code == 200:
        print("Application Logged")



def fake_sentence() -> str:
    """
    Generate a random sentence using the Faker library.
    """
    fake = Faker()
    return fake.sentence()

def fill_form(driver: webdriver.Chrome, fake_identity: dict) -> None:
    
    """
    Fill the form with the provided fake identity data.
    """
    try:
        driver.get("https://recruiting.paylocity.com/Recruiting/Jobs/Apply/3223576")
        
        # wait until the page is loaded with implicit wait
        driver.implicitly_wait(10)
        # time.sleep(1)
        
        time.sleep(3)
        
        
        print("hiding the modal")
        # style of .backdrop none
        driver.execute_script("document.querySelector('.backdrop').style.display = 'none'")
        # style of .modal-dialog none
        driver.execute_script("document.querySelector('.modal').style.display = 'none'")
        
        
        checkbox = driver.find_element("id", "useAttachedResumeToFillOutApplication")
        checkbox.click()
        time.sleep(1)
        
        
        print("attaching the resume")
        resume_input = driver.find_element("id", "btn-forceResume")
        resume_input.send_keys(os.path.join(os.getcwd(), f"{fake_identity['first_name']} {fake_identity['last_name']}.pdf"))
        driver.implicitly_wait(5)
        
        for key, value in DOM_ELEMENTS.items():
            
            print(f"Filling {key} with {fake_identity[key]}")
            
            # find the element with id value
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(value)
            )
            element.send_keys(fake_identity[key])
            
            if key == "state":
                time.sleep(1)
                
                
                # check if dropdown is open public-site-address-us-state-dropdown-list-container:
                if driver.find_element("id", "public-site-address-us-state-dropdown-list-container").is_displayed():
                    driver.find_element("id", "public-site-address-us-state-dropdown-list-container").click()
                    

                # time.sleep(1)
                
            time.sleep(1)
                
        driver.find_element("id", "info.smsOptedIn").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[contains(text(), 'Yes*')]").click()
        
        time.sleep(3)
        
        driver.find_element("id", "btn-submit").click()
        time.sleep(1)
        
        print("Waiting for the next page to load...")
        
        if "Please correct missing or invalid fields." in driver.page_source:
            
            
            # print(driver.page_source)
            
            
            
            print("Please correct missing or invalid fields.")
            raise Exception("Please correct missing or invalid fields.")
        
        
        
        if "Invalid email address" in driver.page_source:
            print("Invalid email address")
            # logger.log("Invalid email address")
            raise Exception("Invalid email address")
        
        time.sleep(2)
        
        
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "multiQuestionAnswer1285162_0"))
        )
        time.sleep(1)

        
        print("filling out page 2...")
        
        
        driver.find_element("id", f"multiQuestionAnswer1285162_{random.randint(0,3)}").click()
        time.sleep(1)
        driver.find_element("id", f"multiQuestionAnswer1285163_{random.randint(0,1)}").click()
        time.sleep(1)
        
        for i in range(7):
            
            # half of the time click the checkbox
            if random.randint(0,1) == 0:
                driver.find_element("id", f"multiQuestionAnswer1285164_{i}").click()
                time.sleep(1)
                
        # random text to screener-question-3-textarea
        driver.find_element("id", "screener-question-3-textarea").send_keys(fake_sentence())

        
        driver.find_element("id", f"multiQuestionAnswer1285182_{random.randint(0,1)}").click()
        time.sleep(1)
        driver.find_element("id", f"multiQuestionAnswer1285183_{random.randint(0,3)}").click()
        time.sleep(1)
        driver.find_element("id", f"multiQuestionAnswer1286455_{random.randint(0,1)}").click()
        time.sleep(1)
        
        
        driver.find_element("id", "btn-submit").click()
        time.sleep(1)
        time.sleep(1)
        
        print("Waiting for the next page to load...")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "acknowledgements.eeoGender"))
        )
        
        print("filling out page 3...")
        driver.find_element("id", "acknowledgements.eeoGender").click()
        time.sleep(1)
        #id acknowledgements.eeoGender__listbox__option__2
        driver.find_element(By.ID, f"acknowledgements.eeoGender__listbox__option__{random.randint(1,3)}").click()
        time.sleep(1)
        # acknowledgements.racialOrEthnicGroup__listbox__option__7
        driver.find_element("id", "acknowledgements.racialOrEthnicGroup").click()
        time.sleep(1)
        driver.find_element(By.ID, f"acknowledgements.racialOrEthnicGroup__listbox__option__{random.randint(1,8)}").click()
        # acknowledgements.militaryService
        time.sleep(1)
        driver.find_element("id", "acknowledgements.militaryService").click()
        time.sleep(1)
        driver.find_element(By.ID, f"acknowledgements.militaryService__listbox__option__{random.randint(1,3)}").click()
        # acknowledgements.disability__listbox__option__2
        time.sleep(1)
        driver.find_element("id", "acknowledgements.disability").click()
        time.sleep(1)
        driver.find_element(By.ID, f"acknowledgements.disability__listbox__option__{random.randint(1,3)}").click()
        
        
        print("Waiting for the next page to load...")
        time.sleep(1)
        driver.find_element("id", "btn-submit").click()
        time.sleep(1)
        
        print("Waiting for the next page to load...")
        time.sleep(1)
        driver.find_element("id", "btn-submit").click()
        time.sleep(1)
        
        print("filling out page 4...")
        time.sleep(1)
        
        driver.find_element("id", "acknowledgements.authorizedToWorkInUs").click()
        time.sleep(1)
        driver.find_element(By.ID, f"acknowledgements.authorizedToWorkInUs__listbox__option__{random.randint(1,2)}").click()
        time.sleep(1)
        
        print("submitting the form...")
        
        driver.find_element("id", "applyAcknowledgement").click()
        time.sleep(1)
        driver.find_element(By.ID, "btn-submit").click()
        
        time.sleep(1)
        addTracking()
        time.sleep(5)
    
    except TimeoutException as e:
        print(f"Timeout while waiting for element: {e}")    
    except Exception as e:
        print(f"Error filling form: {e}")
        raise e
    finally:
        os.remove(os.path.join(os.getcwd(), f'{fake_identity["first_name"]} {fake_identity["last_name"]}.pdf'))
        driver.quit()
        
        
