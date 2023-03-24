import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
import json
import datetime

# scrape the website to get prices for different twinsets
URL= "https://www.deepstop.de/en/171-sets-for-twintanks"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# Using find_all to get the prices of all the twin sets they have. Use find if just browsing individual set like XTX-50
results = soup.find_all("div", class_="product-meta")

new_prices = {}

for product in results:

    # Get product name
    product_name = product.find("a", class_ = "product-name")
    product_name = product_name.text.strip()
    
    # Get current product price
    product_price = product.find("span", class_ = "price product-price")
    product_price = product_price.text.strip()
    product_price = float(product_price.replace("€", "").replace(",", ""))

    # Fill the dictionary with the product and price/price history
    new_prices[product_name] = product_price

""" Load the existing prices if available. Else create new file"""
try:
    # Open JSON/txt file and load it into a new dictionary
    with open("data/twinset_prices.txt") as f:
        stored_prices = json.load(f)

        prices = [1064.85, 1295]

        for item in stored_prices:
            if new_prices[item] != stored_prices[item]:
                print(f"Yesterday: \n{item} cost {stored_prices[item]}\n")
                print(f"Today: \n{item} cost {new_prices[item]}")
                print("\nThe price has changed.")
                print("-" * 50, "\n")
            
            else:
                pass

except FileNotFoundError:
    if not os.path.exists("data"):
        os.makedirs("data")
    with open("data/twinset_prices.txt", "w") as file:
        file.write(json.dumps(new_prices))
    print("File does not exist. Creating file from new data...")




