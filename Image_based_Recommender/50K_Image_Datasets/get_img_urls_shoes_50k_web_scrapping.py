import os
from selenium.webdriver.chrome.options import Options
import requests
import shutil
import time
import random
import pandas as pd
import numpy as np
import urllib.parse
import matplotlib.pyplot as plt
from selenium import webdriver
from bs4 import BeautifulSoup
from PIL import Image as PilImage
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor


# Get productIds
shoes_df = pd.read_csv('./Dataset_csv/amazon_reviews_us_Shoes_v1_00_help_voted_And_cut_lognTail.csv')
raw_productIds = shoes_df['product_id'].to_list()
unique_products = list(np.unique(raw_productIds))
#products_10k = random.sample(unique_products,10000)
#products_20k = random.sample(unique_products,20000)
products_50k = random.sample(unique_products, 50000)

print("Raw shoes dataset:", len(raw_productIds))
print("Unique shoes products:", len(unique_products))
#print("10K samples:", len(products_10k))
#print("20K samples:", len(products_20k))
print("50K samples:", len(products_50k))


# top 1 recommended products for each user.
# Get productIds
shoes_df = pd.read_csv('./Dataset_csv/Shoes_for_100_users_per_100_products_prediction_Ver4.csv')
productIds_for_100_users = shoes_df['asin'].to_list()
top100recommended = [productIds_for_100_users[i] for i in range(0, 1000, 10)]


# for item in top100recommended:
#    products_10k.append(item)
# for item in top100recommended:
#    products_20k.append(item)
for item in top100recommended:
    products_50k.append(item)

#products_10k = list(np.unique(products_10k))
#products_20k = list(np.unique(products_20k))
products_50k = list(np.unique(products_50k))

#print("10K sample:", len(products_10k))
#print("20K_sample:", len(products_20k))
print("50K_sample:", len(products_50k))


# Get website url
product_url_50k = {}
for i in products_50k:
    url = urllib.parse.urljoin('https://www.amazon.com/dp/', i)
    product_url_50k[i] = url


print("Successfully get product_urls!")
print("Total number for product_url_dict:", len(list(product_url_50k.items())))

# Execute Chromedriver
options = Options()
options.headless = True
options.add_argument("user-agent=whatever you want")
driver = webdriver.Chrome(options=options)


def get_imageurl(product, image_url_50k):
    i, asin, url = product[0], product[1][0], product[1][1]
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, "lxml")
    print(i)
    for div in soup.find_all('div', id="imgTagWrapperId"):
        image = div.find('img', alt=True)
        image_url_50k[asin] = (image['src'])


product_list = enumerate(list(product_url_50k.items()))

image_url_50k = {}

start = time.time()
with ThreadPoolExecutor(max_workers=12) as executor:
    executor.map(
        lambda product: get_imageurl(product, image_url_50k), product_list)

elapsed = time.time() - start
print(elapsed)

# Extract img urls
#image_url_50k = {}
# for i, product in enumerate(list(product_url_50k.items())):
#    asin, url = product[0], product[1]
#    driver.get(url)
#    content = driver.page_source
#    soup = BeautifulSoup(content, "lxml")
#    print(i)
#    for div in soup.find_all('div', id="imgTagWrapperId"):
#        image = div.find('img', alt=True)
#        image_url_50k[asin] = (image['src'])


print("Successfully get image_urls!")
print("Total number for image_url_dict:", len(list(image_url_50k.items())))


# Save as csv file (asin/url)
asin_url_50k_df = pd.DataFrame.from_dict(
    image_url_50k,
    orient='index',
    columns=['url']).reset_index().rename(
        columns={
            'index': 'asin'})
asin_url_50k_df.to_csv(r'./asin_url_for_50k.csv', index=False, header=True)


# Download images
for asin, url in image_url_50k.items():
    # Open the url image, set stream to True, this will return the stream content.
    resp = requests.get(url, stream=True)
    # Open a local file with wb ( write binary ) permission. (created increment filename)
    path = os.path.join("./Images_50K/", asin + "." + "jpg")
#     print(path)
    local_file = open(path, 'wb')
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    resp.raw.decode_content = True
    # Copy the response stream raw data to local image file.
    shutil.copyfileobj(resp.raw, local_file)
    # Remove the image url response object.
    del resp
