import requests
from bs4 import BeautifulSoup
import time

def extract_flipkart_product_info(url):
    time.sleep(2)  # Delay to avoid getting blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    # Send GET request
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch page, Status Code: {response.status_code}")
        return None, None, None, None

    soup = BeautifulSoup(response.content, "html.parser")

    # **Extract Product Title**
    title = None
    title_element = soup.find("span", class_=lambda x: x and "VU-ZEz" in x)
    if title_element:
        title = title_element.get_text(strip=True)

    # **Extract Product Price**
    price = None
    price_element = soup.find("div", class_=lambda x: x and "Nx9bqj CxhGGd" in x)
    if price_element:
        price = price_element.get_text(strip=True)

    # **Extract Ingredients Properly**
    ingredients_list = "Not found"

    # Find the table row that contains "Ingredients"
    ingredient_row = soup.find("td", string=lambda x: x and "Ingredients" in x)

    if ingredient_row:
        

        # Find the next <td> (where ingredients are listed)
        next_td = ingredient_row.find_next_sibling("td")

        if next_td:
            # Extract all <li> elements inside this <td>
            ingredients = [li.get_text(strip=True) for li in next_td.find_all("li")]
            if ingredients:
                ingredients_list = ", ".join(ingredients)

    # **Extract Image URL**
    image_url = None
    image_div = soup.find("div", class_=lambda x: x and "vU5WPQ" in x)
    if image_div:
        img_tag = image_div.find("img")  # Find the first img tag inside the div
        if img_tag and "src" in img_tag.attrs:
            image_url = img_tag["src"]  # Get the image URL

    return title, price, image_url, ingredients_list

# # **Example Flipkart Product URL**
# url = "https://www.flipkart.com/bingo-mad-angles-achaari-masti-chips/p/itmffxrj9nnbgsq8?pid=SNSEUCYSXTFVST6D&lid=LSTSNSEUCYSXTFVST6DMSQVIS"

# # Fetch Data
# title, price, image_url, ingredients_list = extract_flipkart_product_info(url)

# # **Print Results**
# print("\n--- FINAL OUTPUT ---")
# print(f"Title: {title}")
# print(f"Price: {price}")
# print(f"Image URL: {image_url}")
# print(f"Ingredients: {ingredients_list}")

# # Add delay to avoid getting blocked
# time.sleep(2)
