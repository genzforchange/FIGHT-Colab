import time
import os
from resume_faker import make_resume
from util_functions import start_driver, generate_fake_identity, fill_form_app1, fill_form_app2, check_if_app_exists, start_driver_local, fill_form_all
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import random

fake = Faker()



urls = ["https://recruiting.paylocity.com/Recruiting/Jobs/Apply/3173329","https://recruiting.paylocity.com/Recruiting/Jobs/Apply/3223576", "https://recruiting.paylocity.com/Recruiting/Jobs/Apply/2978847", "https://recruiting.paylocity.com/Recruiting/Jobs/Apply/3292538"]



def get_random_url(driver):
    """Select a random URL from the list."""
    
    while True:
        url = random.choice(urls)
        try:
            print("checking if app exists...")
            if not check_if_app_exists(driver, url):
                print("Application does not exist, selecting a new URL...")
                continue
                         
            return urls.index(url)
        except Exception as e:
            print(f"Error accessing URL: {e}")
            time.sleep(2)
            
        
    
    
    return random.choice(urls)


if __name__ == "__main__":
    
    while True:
        try:
            

            print("Starting a new iteration...")
        
            # driver = start_driver_local()
            driver = start_driver()
            
            print("Driver started successfully.")
            print("generating fake identity...")
            fake_identity = generate_fake_identity(fake)
            
            name = f"{fake_identity['first_name']} {fake_identity['last_name']}"
            # Generate a resume with default settings
            print("Generating resume...")
            resume = make_resume(name, fake_identity['email'], f"{name}.pdf")

            print("Resume generated successfully.")
            # Select random form of the 2

            # match get_random_url(driver):
            #     case 0:
            #         print("Filling out form for Application 1...")
            #         fill_form_app1(driver, fake_identity)
            #     case 1:
            #         print("Filling out form for Application 2...")
            #         fill_form_app2(driver, fake_identity)
            #     case 2:
            #         print("Filling out form for Application 3...")
            #         fill_form_all(driver, fake_identity, urls[2])
            #     case _:
            #         print("No valid application found, retrying...")
            #         continue
                        
                    
            print("Filling out the form...")
            
            url = get_random_url(driver)
            fill_form_all(driver, fake_identity, urls[url], url)


            
            # print("Filling out the form...")
            # fill_form(driver, fake_identity)
            
            print("Form filled successfully.")
            # Wait for a few seconds before the next iteration
            print("Waiting for 2 seconds before the next iteration...")
            time.sleep(2)
            

        except Exception as e:
            print(f"An error occurred: {e}")
            # Optionally, you can add a delay before retrying
            time.sleep(5)
        finally:
            # Close the driver after each iteration
            try:
                driver.quit()
            except Exception as e:
                print(f"Error closing driver: {e}")
            
            
        

    




