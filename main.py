from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from db import connect
from query import getOTP, getPhoneNumber

try:
    driver = webdriver.Chrome()
    driver.get("https://www.flipkart.com/mivi-play-5-w-portable-bluetooth-speaker/p/itmb0a3cf7d68909?pid=ACCG25T4GTENPNFN&lid=LSTACCG25T4GTENPNFNZY7YW9&marketplace=FLIPKART&store=0pm%2F0o7&srno=b_1_1&otracker=browse&fm=organic&iid=en_wZB5SPAKDvwMwdu0EUpkf6AQQCaD9Jo1W14usB0IwvpqeOormxFw-PdbFDtXFIzK-qKY2W4avqlWyKfGzhcZIQ%3D%3D&ppt=browse&ppn=browse&ssid=n4shli00u80000001729421680932")

    time.sleep(6)

    # Click the 'Buy Now' button
    buy_now_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'QqFHMw') and contains(@class, '_7Pd1Fp')]"))
    )
    buy_now_button.click()

    # Input phone number
    phone_number = "9509652141"  # Assuming this retrieves the phone number for the given ID
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
    time.sleep(40)  # Wait for 60 seconds before fetching the OTP
    db=connect()
    mycursor = db.cursor()
    mycursor.execute(getOTP(), (1,)) 
    otp_result = mycursor.fetchall()  

    mycursor.execute("select * from card_details_table;") 
    card_data = mycursor.fetchall()
    card_details=card_data[0]  

    if otp_result:
        otp_value = otp_result[0]
        print("OTP retrieved:", otp_value)

        # Input OTP
        otp_input.clear()
        otp_input.send_keys(otp_value)

        # Click 'Login' button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'QqFHMw') and contains(@class, '_7Pd1Fp')]"))
        )
        login_button.click()

        deliver_here_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Deliver Here')]"))
        )
        deliver_here_button.click()
        time.sleep(5)
        print("66")
        continue_button_2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'QqFHMw') and contains(@class, '_7Pd1Fp')]"))
        )
        continue_button_2.click()
        print("71")
        time.sleep(5)
        

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


        card_number = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@maxlength='16' and @type='text']"))
        )
        card_number.clear()
        card_number.send_keys("4799598795097161")      

        time.sleep(2)
        month_dropdown = Select(driver.find_element(By.XPATH, "//select[@name='month']"))
        year_dropdown = Select(driver.find_element(By.XPATH, "//select[@name='year']"))  # Update 'year' to match the actual name or locator for the year dropdown

        # Select the month and year by value
        month_dropdown.select_by_value("11")
        time.sleep(2)
        year_dropdown.select_by_value("30")  
        time.sleep(2)

        pay_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'QqFHMw') and contains(@class, '_7Pd1Fp')]"))
        )
        pay_button.click()
        time.sleep(5)

        maybe_later = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Maybe later']")))
        maybe_later.click()


        time.sleep(10)
        credit_otp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@maxlength='6' and @type='password']"))
        )
        credit_otp.clear()
        credit_otp.send_keys("696969")
        time.sleep(5)
    
    else:
        print("No OTP found for the given ID.")


    time.sleep(6)
    mycursor.close()

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()
