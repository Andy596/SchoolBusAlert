# SchoolBusAlert
SchoolBusAlert is an automated bus departure tracking system that monitors Twitter (X) for updates about school bus arrivals and departures. It uses Selenium and BeautifulSoup to scrape tweets from a specific account and sends SMS alerts when a relevant bus update is detected. The program logs into Twitter automatically, checks for bus departure tweets within a specific time window (3:20pm-4:00pm), compares the tweet time to the current time to ensure relevance and ensures alerts are sent only when necessary.

Take note that this program is currently in beta, Created in November 2024.
This program will only detect bus 2018 (My bus) for now, future updates will allow this program to detect all other buses, and provide convenience for everyone.


To use this program, you need to first edit some variables, like sender_email, receiver_email, email_password, login_email, username, login_password, etc.
