import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # Exception handling for timeout
from bs4 import BeautifulSoup

# Variable to control the loop
successful_login = False

while not successful_login:
    # 1. Get login credentials from user
    user_input = input("Enter your username: ")
    password_input = input("Enter your password: ")

    try:
        # 2. Start ChromeDriver
        driver = webdriver.Chrome()

        # 3. Navigate to the site
        driver.get('https://sso.aztu.edu.az/')

        # 4. Locate username and password fields
        username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "UserId")))
        password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Password")))

        # 5. Enter username and password
        username.send_keys(user_input)  # Username from input
        password.send_keys(password_input)  # Password from input

        # 6. Locate login button and click it
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/section/div/div[1]/div/div/form/div[3]/button')))
        login_button.click()

        # 7. Wait for the page to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/aside[1]/div/nav/ul/li[1]/a')))

        # 8. Click the student section button
        student_section_button = driver.find_element(By.XPATH, '/html/body/div/aside[1]/div/nav/ul/li[1]/a')
        student_section_button.click()

        # 9. Click the departments section
        departments_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu6i"]/a/span[2]/span')))
        departments_button.click()

        # 10. Select Python course
        python_course_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu6i"]/ul/li[3]/a')))
        python_course_button.click()

        # 11. Navigate to attendance section
        attendance_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main_content"]/div[1]/div/div[2]/a[7]')))
        attendance_button.click()

        # 12. Wait for the page to load completely
        time.sleep(10)  # Waiting for the page to load fully

        # 13. Use BeautifulSoup to extract the page content
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 14. Search for dates and attendance information
        dates = soup.find_all('font', {'style': 'font-size:11px;'})  # Locate dates
        attendance = soup.find_all('span', {'class': 'attend-label'})  # Locate attendance status

        # 15. Print the data to the console
        if dates and attendance:
            for date, attend in zip(dates, attendance):
                date_text = date.get_text().strip()  # Clean the date text
                attendance_text = attend.get_text().strip()  # Clean the attendance text

                # Determine the status based on attendance text
                if attendance_text == "i/e":
                    status = "Student attended the class."
                elif attendance_text == "q/b":
                    status = "Student did not attend the class."
                else:
                    status = f"Unknown status: {attendance_text}"

                print(f"Date: {date_text}, Status: {status}")
        else:
            print("No attendance data found.")

        # 16. Exit the loop after successful login
        successful_login = True

    except TimeoutException:
        # If login fails
        print("Invalid username or password. Please try again.")
    except Exception as e:
        # Catch any other exceptions
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()
