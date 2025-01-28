import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver
from firebase_admin import credentials, firestore, initialize_app
from selenium.webdriver.common.keys import Keys
import re
# Initialize Firebase Admin
cred = credentials.Certificate("E:/Projs/iHub/SMA/SMA_clone/SMA_clone/linkedinscrap2-37c62-firebase-adminsdk-n9j6u-f3748a562d.json")
initialize_app(cred)
db = firestore.client()

# Initialize the Selenium driver
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = Driver(uc=True, headless=False)

def login():
    try:
        with open(r'E:/Projs/iHub/SMA/SMA_clone/SMA_clone/sdk.txt') as login_file:
            lines = login_file.readlines()
            email = lines[0].strip()
            password = lines[1].strip()
        
        driver.get("https://www.linkedin.com/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)
        time.sleep(5)
        driver.find_element(By.ID, "password").send_keys(password + Keys.RETURN)
        WebDriverWait(driver, 10).until(EC.title_contains("LinkedIn"))
    except Exception as e:
        print("Login error:", e)

def scrape_followers(profile_link, name):
    try:
        driver.get(profile_link)

        # List of potential posts buttons
        possible_posts_buttons = [
            "//a[contains(@href, '/school/snsinstitutions/posts/')]",
            "//a[contains(@href, '/school/kct/posts/')]",
            "//a[contains(@href, '/school/psg-college-of-technology/posts/')]"
        ]

        for xpath in possible_posts_buttons:
            try:
                posts_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                posts_button.click()
                time.sleep(3)  # Wait for the page to load after clicking the button
                break  # Exit the loop if we successfully clicked a button
            except Exception as e:
                print(f"Could not find or click the button with xpath: {xpath}. Error: {e}")

        # After clicking the posts button, retrieve the followers count
        followers_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.t-14.t-normal.text-align-center")))
        followers_text = followers_element.text

# Use regex to extract only the numeric part
        followers_count = re.sub(r'/D', '', followers_text)

        return followers_count

    except Exception as e:
        print("Error retrieving followers count for {}: {}".format(name, e))
        return None


def store_data(name, followers_count):
    now = time.localtime()
    date_str = time.strftime("%Y-%m-%d", now)
    day_str = time.strftime("%A", now)
    time_str = time.strftime("%H:%M:%S", now)

    data = {
        "Name": name,
        "Followers Count": followers_count,
        "Date": date_str,
        "Day": day_str,
        "Time": time_str
    }

    # Store in Firebase
    db.collection('followers_data').add(data)

    # Append to CSV
    try:
        with open('followers_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, followers_count, date_str, day_str, time_str])
    except Exception as e:
        print("Error writing to CSV:", e)

def store_data(name, followers_count):
    now = time.localtime()
    date_str = time.strftime("%Y-%m-%d", now)
    day_str = time.strftime("%A", now)
    time_str = time.strftime("%H:%M:%S", now)

    data = {
        "Name": name,
        "Followers Count": followers_count,
        "Date": date_str,
        "Day": day_str,
        "Time": time_str
    }

    # Store in Firebase
    db.collection('followers_data').add(data)

    # Append to CSV
    try:
        with open(r'E:/Projs/iHub/SMA/SMA_clone/SMA_clone/followers_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, followers_count, date_str, day_str, time_str])
    except Exception as e:
        print("Error writing to CSV:", e)

def main():
    while True:
        # Initialize the Selenium driver
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = Driver(uc=True, headless=False)

        login()

        try:
            with open(r'E:\Projs\iHub\SMA\SMA_clone\SMA_clone\input_profiles.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    Name, profile_link = row
                    followers_count = scrape_followers(profile_link, Name)

                    if followers_count:
                        print(f"Followers count for {Name}: {followers_count}")
                        store_data(Name, followers_count)
        except Exception as e:
            print("Error reading input CSV:", e)

        # Quit the driver
        driver.quit()

        # Wait for 15 minutes before starting again
        print("Waiting for 5 minutes before the next cycle...")
        time.sleep(300)  # 5 minutes in seconds


        # Quit the driver
        driver.quit()

        # Wait for 15 minutes before starting again
        print("Waiting for 5 minutes before the next cycle...")
        time.sleep(300)  # 5 minutes in seconds

if __name__ == "__main__":
    main()
