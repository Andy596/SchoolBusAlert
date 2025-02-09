from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta, time as dt_time

counter = 0
url = 'https://x.com/cpabusdeparture' #url of CpaBusDeparture's twitter
start_time = dt_time(15, 20) #Start running on 15:30
end_time = dt_time(16, 0) #stop running on 16:00
last_alert_time = None
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
sender_email = "Include_Sender_Email"
receiver_email = "Include_Reciever_SMS_Email"
email_password = "Sender_Email_Password"
#Twitter Login:
login_email = "Login_Email_For_Twitter"
username = "Twitter_Username"
login_password = "Twitter_Login_Password"

def login_to_twitter():
    try:
        driver.get("https://x.com")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Sign in"))).click()

        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))
        email_field.send_keys(login_email)
        email_field.send_keys(Keys.RETURN)
        time.sleep(2)

        username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))
        username_field.send_keys(username)
        username_field.send_keys(Keys.RETURN)
        time.sleep(2)

        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        password_field.send_keys(login_password)
        password_field.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[aria-label='Home']")))
        print("Logged in successfully!")

    except Exception as e:
        print(f"An error occurred during login: {e}")

def check_for_bus_departure():
    global last_alert_time
    try:
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tweets = soup.find_all("article")
        print(f"Found {len(tweets)} tweet containers.")
        found = False
        for tweet in tweets:
            tweet_text = tweet.get_text().strip()

            print(f"Checking tweet: {tweet_text}")

            if "2018" in tweet_text:
                print("Found 2018!")
                tweet_time = find_2018_date(tweet)

                if tweet_time and is_recent(tweet_time):
                    today = datetime.now().date()
                    current_time = datetime.now()

                    if not last_alert_time or (current_time - last_alert_time).total_seconds() > 12 * 3600:
                        send_alert("2018 IN BUS LOOP!!!")
                        last_alert_time = current_time
                        found = True
                        break
        if not found:
            print("2018 not found yet.")

    except Exception as e:
        print(f"An error occurred: {e}")


def find_2018_date(tweet_element):
    try:
        time_element = tweet_element.find("time")
        if time_element:
            tweet_time_str = time_element['datetime']
            tweet_time = datetime.strptime(tweet_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            tweet_time = tweet_time - timedelta(hours=3)
            print(f"Tweet time: {tweet_time}")
            return tweet_time
        else:
            print("No time element found for tweet.")

    except Exception as e:
        print(f"An error occurred in find_2018_date: {e}")
    return None

def is_recent(tweet_time):
    current_time = datetime.now()
    print(f"Current Time: {current_time}")
    print(f"Tweet time: {tweet_time}")
    time_difference = current_time - tweet_time
    print(f"Time Difference: {time_difference}")
    return time_difference.total_seconds() <= 2 * 3600

def send_alert(message):
    try:
        msg = MIMEText(message)
        msg['Subject'] = 'Bus Alert'
        msg['From'] = sender_email
        msg['To'] = receiver_email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, email_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Alert sent successfully!")
    except Exception as e:
        print(f"Error sending alert: {e}")

login_to_twitter()
while True:
    current_time = datetime.now().time()
    if start_time <= current_time <= end_time:
        counter += 1
        print(f"Checked {counter} times.")
        check_for_bus_departure()
    else:
        print("Outside the time window. Waiting...")
    time.sleep(30)