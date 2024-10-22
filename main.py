from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from db import connect
from query import getOTP, getPhoneNumber
from app import consume_otp_endpoint
import aiohttp
import asyncio



async def fetch_platorm_otp():
    url = "http://127.0.0.1:5000/consume-otp"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            otp_result = await response.text()
            return otp_result

async def fetch_credit_otp():
    url = "http://127.0.0.1:5000/consume-cc-otp"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            otp_result = await response.text()
            return otp_result

async def main():
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.flipkart.com/apple-iphone-15-pro-black-titanium-512-gb/p/itm6cec19f8ee1c3?pid=MOBGTAGPKHHNRHXH&lid=LSTMOBGTAGPKHHNRHXHRO9D8C&marketplace=FLIPKART&q=iphone+15+pro&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&iid=ff10b13c-32fb-4df8-a2b0-63a3e0b508fe.MOBGTAGPKHHNRHXH.SEARCH&ssid=1hpje91nvk0000001729626619675&qH=c9de95b3b911a866")
        time.sleep(5)

        # Click the 'Buy Now' button
        buy_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'QqFHMw') and contains(@class, '_7Pd1Fp')]"))
        )
        buy_now_button.click()

        # Input phone number
        phone_number = "9123924829"  # Assuming this retrieves the phone number for the given ID
        phone_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text' and contains(@class, 'r4vIwl')]"))
        )
        phone_input.clear()
        phone_input.send_keys(phone_number)


        # Click 'Continue' button
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'QqFHMw') and contains(@class, '_7Pd1Fp')]"))
        )
        continue_button.click()

        # Wait for the OTP input field to appear
        otp_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@maxlength='6' and @type='text']"))
        )

        # Introduce a delay of 60 seconds to allow the OTP to be generated
        print("Waiting for OTP to be generated...")
        # Wait for 60 seconds before fetching the OTP
        
        otp_result = await fetch_platorm_otp()
        print(otp_result)
        if otp_result:
            print("OTP retrieved:", otp_result)

            # Input OTP
            otp_input.clear()
            otp_input.send_keys(otp_result)

            # Click 'Login' button
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'QqFHMw') and contains(@class, '_7Pd1Fp')]"))
            )
            login_button.click()

            deliver_here_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Deliver Here')]"))
            )
            deliver_here_button.click()

            continue_button_2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'QqFHMw') and contains(@class, '_7Pd1Fp')]"))
            )
            continue_button_2.click()
            print("71")
            

            wait = WebDriverWait(driver, 10)
            accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept & Continue']")))
            
            # Click the "Accept & Continue" button
            accept_button.click()

            print("76")
            time.sleep(5)

            span_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Credit / Debit / ATM Card']"))
            )

            # Click the span
            span_element.click()
            time.sleep(5)
            cvv_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@maxlength='4' and @type='password']"))
            )
            cvv_input.clear() 
            cvv_input.send_keys("123")

            time.sleep(2)
            card_number = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@maxlength='16' and @type='text']"))
            )
            card_number.clear()
            card_number.send_keys("5334670041809605")      

            time.sleep(2)
            month_dropdown = Select(driver.find_element(By.XPATH, "//select[@name='month']"))
            year_dropdown = Select(driver.find_element(By.XPATH, "//select[@name='year']"))  # Update 'year' to match the actual name or locator for the year dropdown

            # Select the month and year by value
            month_dropdown.select_by_value("01")
            time.sleep(2)
            year_dropdown.select_by_value("29")  
            time.sleep(2)

            pay_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'QqFHMw') and contains(@class, '_7Pd1Fp')]"))
            )
            pay_button.click()
            time.sleep(2)

            maybe_later = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Maybe later']")))
            maybe_later.click()
            time.sleep(2)
            time.sleep(15)

            cc_otp = await fetch_credit_otp()
            print(cc_otp)
            credit_otp = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password' and @name='otpValue']"))
            )
            credit_otp.clear()
            credit_otp.send_keys(cc_otp)

            time.sleep(4)
            confirm = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Confirm']")))
            confirm.click()

            time.sleep(20)
            


        
        
        else:
            print("No OTP found for the given ID.")


        time.sleep(6)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        driver.quit()


# Run the asynchronous event loop
if __name__ == "__main__":
    asyncio.run(main())




