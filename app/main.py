import time
import os
from resume_faker import make_resume
from util_functions import start_driver, generate_fake_identity, fill_form
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import random

fake = Faker()





if __name__ == "__main__":
    
    while True:
        try:
            

            print("Starting a new iteration...")
        
            driver = start_driver()
            
            print("Driver started successfully.")
            print("generating fake identity...")
            fake_identity = generate_fake_identity(fake)
            
            name = f"{fake_identity['first_name']} {fake_identity['last_name']}"
            # Generate a resume with default settings
            print("Generating resume...")
            resume = make_resume(name, fake_identity['email'], f"{name}.pdf")

            print("Resume generated successfully.")
            print("Filling out the form...")
            fill_form(driver, fake_identity)
            
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
            
            
        

    




