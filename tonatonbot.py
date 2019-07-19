# Author: Edem Agbakpe
# Function: Scrape tonaton.com/properties and send daily notifications of results via email

import csv
import yagmail
import schedule
import requests
from bs4 import BeautifulSoup


def tonaton_properties_crawler():

    page = 1
    link_list = []
    title_list = []
    price_list = []

    # Connect to the internet while it loops through pages
    while page <= 9:
        url = 'https://tonaton.com/en/ads/spintex/property?page=' + str(page)
        source_code = requests.get(url)
        source_code.raise_for_status()
        plaint_text = source_code.text
        soup = BeautifulSoup(plaint_text, features="html.parser")

        # get the price
        for price_in_cedis in soup.findAll('p', class_='item-info'):
            calculatable_price = price_in_cedis.string.strip('GH₵').strip('/month').replace(',', '').strip()
            integer_price = int(calculatable_price)
            price_list.append(integer_price)

        # get links for each property
        for link in soup.findAll('a', class_='item-title h4'):
            href = 'https://tonaton.com' + link.get('href')
            link_list.append(href)

            # get title for each property
            title = link.string.capitalize()
            title_list.append(title)

            # loop add one to page to move to next page
            page += 1

    # create csv file and write lists to it
    with open('dailyprops.csv', 'w', newline='') as f:
        the_writer = csv.writer(f)
        rows = zip(title_list, price_list, link_list)
        the_writer.writerow(['Title', 'Price', 'Link'])
        for row in rows:
            the_writer.writerow(row)


def email_function():

    password = "****"
    sender_email = "tonatonpropertydaily@gmail.com"
    receiver_email = 'edem.agbakpe@gmail.com'

    # connect to smtp server.
    yag_smtp_connection = yagmail.SMTP(user=sender_email, password=password, host='smtp.gmail.com')
    # email subject
    subject = 'Daily properties'
    # email content with attached file path.
    content = ['Hello, \n\nHere\'s a list of all properties for today:', 'dailyprops.csv']

    # send email :)
    yag_smtp_connection.send(receiver_email, subject, content)


schedule.every().day.at("16:05").do(email_function)

# Check if my task is pending to run
while True:
    schedule.run_pending()