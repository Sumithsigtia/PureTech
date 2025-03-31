import requests
from bs4 import BeautifulSoup
import random
import time
import re

# List of User-Agent strings to rotate
user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

def extract_bigbasket_product_info(url):
    headers = {"User-Agent": random.choice(user_agent_list)}

    # Request HTML content
    response = requests.get(url, headers=headers)
    time.sleep(random.uniform(2, 5))  # Random delay to avoid blocking

    if response.status_code != 200:
        print(f"Failed to fetch page, Status Code: {response.status_code}")
        return None, None, None, None

    soup = BeautifulSoup(response.content, "html.parser")

    # **Extract Product Title**
    title_element = soup.find("h1")
    title = title_element.text.strip() if title_element else "Not found"

    # **Extract Product Price**
    price_element = soup.find("td", class_=re.compile(r"Description___StyledTd"))
    price = None
    if price_element:
        price_text = price_element.text.strip()
        price_match = re.search(r'₹\s?([\d,.]+)', price_text)  # Extract price using regex
        price = price_match.group(1) if price_match else "Not found"

    # **Extract Product Image**
    image_element = soup.find("img", src=True)
    image_url = image_element["src"] if image_element else "Not found"

    ingredients_list="Not found"
    return title, price, image_url, ingredients_list


# # **Example Usage**
# url = "https://www.bigbasket.com/pd/40322608/centrum-kids-multivitamin-protein-health-drink-powder-chocolate-200-g-carton/?nc=Similar+Products&t_pos_sec=5&t_pos_item=2&t_s=Kids+Multivitamin+%2526+Protein+Nutrition+Drink+Powder+-+Chocolate"
# title, price, image_url, ingredients = extract_bigbasket_product_info(url)

# # **Final Output**
# print(f"\n--- FINAL OUTPUT ---")
# print(f"Title: {title}")
# print(f"Price: {price}")
# print(f"Image URL: {image_url}")
# print(f"Ingredients: {ingredients}")
