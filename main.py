from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from db import connection
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
    phone_number = "7828933347"  # Assuming this retrieves the phone number for the given ID
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
    time.sleep(25)  # Wait for 60 seconds before fetching the OTP

    db = connection()
    cursor = db.cursor()

    # Fetch OTP from the database
    cursor.execute(getOTP(), (1,))
    otp_result = cursor.fetchone()

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
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'QqFHMw') and contains(@class, '_7Pd1Fp')]"))
        )
        deliver_here_button.click()

        print("Login clicked")
    else:
        print("No OTP found for the given ID.")

    cursor.close()

    time.sleep(6)

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()
