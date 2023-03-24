import requests, json, os
import pandas as pd
from bs4 import BeautifulSoup
from helper import email_notification
import datetime

# scrape the website to get prices for the Garmin Descent Mk2s in black
URL= "https://www.bookdepository.com/Dungeons-Dragons-Core-Rules-Gift-Set-Wizards-RPG-Team/9780786966622?"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# Using find_all to get the prices of the book of interest
scrape_results = soup.find_all("div", class_="item-block")

new_prices = {}

for product in scrape_results:

    # Get product name
    product_name = product.find("h1")
    product_name = product_name.text.strip()
    
    # Get current product price
    product_price = product.find("span", class_ = "sale-price")
    product_price = product_price.text.strip()
    product_price = float(product_price.replace("SFr. ", ""))

    # Fill the dictionary with the product and price/price history
    new_prices[product_name] = product_price

""" Load the existing prices if available. Else create new file"""
try:
    # Open JSON/txt file and load it into a new dictionary
    with open("data/dnd_books.txt") as f:
        stored_price = json.load(f)

        for item in stored_price:
            if stored_price[item] == new_prices[item]:
                old_price = stored_price[item]
                email_notification(product_name, "Old Price: SFr. " + str(old_price) ,"New Price: SFr. " + str(product_price), "\nThe price has not changed.")
                print(f"Yesterday: \n{item} cost: SFr. {stored_price[item]}\n")
                print(f"Today: \n{item} cost: SFr. {new_prices[item]}")
                print("\nThe price has not changed.")
                print("-" * 50, "\n")
            
            else:
                print(f"Yesterday: \n{item} cost: SFr. {stored_price[item]}\n")
                print(f"Today: \n{item} cost: SFr. {new_prices[item]}")
                print("The price has changed.\n")
                print("-" * 50, "\n")

except FileNotFoundError:
    if not os.path.exists("data"):
        os.makedirs("data")
    with open("data/dnd_books.txt", "w") as file:
        file.write(json.dumps(new_prices))
    print("File does not exist. Creating file from new data...")

""" Load the existing prices history if available. Else create new file"""
write_string = str(product_name) + ","+ str(product_price) + "," + str(datetime.datetime.now())
try:
    # Open JSON/txt file and load it into a new dictionary
    with open("data/dnd_book_history.csv", "a") as f:
        f.write(write_string + "\n")

except FileNotFoundError: 
    with open("data/dnd_book_history.csv", "w") as f:
        f.write(write_string + "\n")
