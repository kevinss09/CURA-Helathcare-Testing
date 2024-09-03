from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime

driver = webdriver.Chrome()
driver.get("https://katalon-demo-cura.herokuapp.com/")


def test_correct_redirect(): 
  driver.find_element(By.ID, "btn-make-appointment").click()

  expected_url = "https://katalon-demo-cura.herokuapp.com/profile.php#login"

  assert expected_url == driver.current_url, f"Test Failed: Expected URL {expected_url}, but got {driver.current_url}"

  print(f'Test case 1: PASS - Redirect to {expected_url} ')

def test_valid_login():
  driver.get("https://katalon-demo-cura.herokuapp.com/profile.php#login")
  
  driver.find_element(By.ID, "txt-username").send_keys("John Doe")
  driver.find_element(By.ID, "txt-password").send_keys("ThisIsNotAPassword")

  driver.find_element(By.ID, "btn-login").click()
  
  expected_url = "https://katalon-demo-cura.herokuapp.com/#appointment"

  assert expected_url == driver.current_url, f"Test Failed: Expected URL {expected_url}, but got {driver.current_url}"
  print(f"Test case 2: PASS - Valid Login - Redirect to {expected_url} " )

  # Log out
  time.sleep(1) 
  driver.find_element(By.CSS_SELECTOR, ".fa-bars").click()
  time.sleep(1)
  driver.find_element(By.LINK_TEXT, "Logout").click()
  

def test_invalid_login():
  driver.get("https://katalon-demo-cura.herokuapp.com/profile.php#login")
  
  driver.find_element(By.ID, "txt-username").send_keys("dasdsads")
  driver.find_element(By.ID, "txt-password").send_keys("sdadsa")

  driver.find_element(By.ID, "btn-login").click()

  error_message = driver.find_element(By.CSS_SELECTOR, ".text-danger").text

  assert "Login failed! Please ensure the username and password are valid." in error_message, "Test Failed: Invalid Login Test Case 2."
  print("Test case 3: PASS - Invalid Login")


def test_empty_name():

  driver.get("https://katalon-demo-cura.herokuapp.com/profile.php#login")
  
  driver.find_element(By.ID, "txt-username").send_keys("")
  driver.find_element(By.ID, "txt-password").send_keys("ThisIsNotAPassword")

  driver.find_element(By.ID, "btn-login").click()

  error_message = driver.find_element(By.CSS_SELECTOR, ".text-danger").text

  assert "Login failed! Please ensure the username and password are valid." in error_message, "Test Failed: Empty Name Test Case 3."
  print("Test case 4: PASS - Empty name")

def test_empty_password():

  driver.get("https://katalon-demo-cura.herokuapp.com/profile.php#login")
  
  driver.find_element(By.ID, "txt-username").send_keys("JohnDoe")
  driver.find_element(By.ID, "txt-password").send_keys("")

  driver.find_element(By.ID, "btn-login").click()

  error_message = driver.find_element(By.CSS_SELECTOR, ".text-danger").text

  assert "Login failed! Please ensure the username and password are valid." in error_message, "Test Failed: Empty Password Test Case 4."
  print("Test case 5: PASS - Empty password")

def book_appointment_all_fields_filled():

  driver.get("https://katalon-demo-cura.herokuapp.com/profile.php#login")
  
  driver.find_element(By.ID, "txt-username").send_keys("John Doe")
  driver.find_element(By.ID, "txt-password").send_keys("ThisIsNotAPassword")
  driver.find_element(By.ID, "btn-login").click()

  # Fill all the fields
  driver.find_element(By.ID, "combo_facility").send_keys("Tokyo CURA Healthcare Center")
  driver.find_element(By.ID, "chk_hospotal_readmission").click()
  driver.find_element(By.ID, "txt_visit_date").send_keys("04/09/2024")
  driver.find_element(By.ID, "txt_comment").send_keys("asdsadasds")
  driver.find_element(By.ID, "btn-book-appointment").click()

  # Verify that the appointment was successfully booked
  confirmation_message = driver.find_element(By.TAG_NAME, "h2").text
  assert "Appointment Confirmation" in confirmation_message, "Test Failed: Appointment was not booked successfully."
  print("Test case 6: PASS - Book Appointment With All Fields Filled")

def book_appointment_required_fields_only():

  driver.find_element(By.XPATH, "//a[@class='btn btn-default']").click()

  time.sleep(2)

  # Fill the required fields
  driver.find_element(By.ID, "txt_visit_date").send_keys("04/09/2024")
  driver.find_element(By.ID, "btn-book-appointment").click()

  # Verify that the appointment was successfully booked
  confirmation_message = driver.find_element(By.TAG_NAME, "h2").text
  assert "Appointment Confirmation" in confirmation_message, "Test Failed: Appointment was not booked successfully. Test Case 7."
  print("Test case 7: PASS - Book Appointment With required Filled")

def book_appointment_invalid_date():

  driver.find_element(By.XPATH, "//a[@class='btn btn-default']").click()

  time.sleep(2)

  # Fill the required fields
  driver.find_element(By.ID, "txt_visit_date").send_keys("skjdsnfsjk")
  driver.find_element(By.ID, "btn-book-appointment").click()

  #  Test it
  assert driver.find_element(By.ID, "visit_date").text ==  datetime.now().strftime("%d/%m/%Y"), "Test Failed: Appointment was booked with invalid Date. Test Case 8."
  print("Test case 8: PASS - Book Appointment With Invalid Date")

# Book appointment with Empty Date Field
def book_appointment_empty_date():

  driver.find_element(By.XPATH, "//a[@class='btn btn-default']").click()

  # Fill the required fields
  driver.find_element(By.ID, "btn-book-appointment").click()

  #  Test it
  assert   driver.find_element(By.ID, "txt_visit_date").text ==  "", "Test Failed: No message even after no Visit Date which is required. Test Case 9."
  print("Test case 9: PASS - Book Appointment with no Visit Date")

# TODO: Book appointment with past date 
def book_appointment_past_date():

  # Fill the required fields
  driver.find_element(By.ID, "btn-book-appointment").click()
  driver.find_element(By.ID, "txt_visit_date").send_keys("01/09/2024")
  driver.find_element(By.ID, "btn-book-appointment").click()

 # Test it
  try:
    error_message = driver.find_element(By.CSS_SELECTOR, ".text-danger").text
    assert False, "Test Failed: An unexpected error message was found for a past date."
  except:
    print("Test case 10: FAIL - No error message when booking with a past date")


def book_appointment_logout():

  driver.find_element(By.XPATH, "//a[@class='btn btn-default']").click()

  # Log out
  time.sleep(1) 
  driver.find_element(By.CSS_SELECTOR, ".fa-bars").click()
  time.sleep(1)
  driver.find_element(By.LINK_TEXT, "Logout").click()

  expect_url = "https://katalon-demo-cura.herokuapp.com/"

  assert expect_url == driver.current_url, "Test Failed: Not able to Logout after appointment. Test Case 11."
  print("Test case 11: PASS - Log Out After Book Appointment")


# Run the test 
print("")
test_correct_redirect()
test_valid_login()
test_invalid_login()
test_empty_name()
test_empty_password()
book_appointment_all_fields_filled()
book_appointment_required_fields_only()
book_appointment_invalid_date()
book_appointment_empty_date()
book_appointment_past_date()
book_appointment_logout()

# Quit the browser
driver.quit()