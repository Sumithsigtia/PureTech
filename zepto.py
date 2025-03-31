import requests
from bs4 import BeautifulSoup

def extract_zepto_product_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch page, Status Code: {response.status_code}")
        return None, None, None, None

    soup = BeautifulSoup(response.content, "html.parser")

    # Extract Product Title
    try:
        title = soup.find("h1").text.strip()
    except AttributeError:
        title = "Title not found"

    # Extract Price (Inside a <span> tag)
    try:
        price_element = soup.find("span", class_="text-[32px] font-medium leading-[30px] text-[#262A33]")
        price = price_element.text.strip() if price_element else "Price not found"
    except AttributeError:
        price = "Price not found"

    # Extract Image URL (From <img> tag)
    image_url = []
    try:
        img_tag = soup.find("img", class_="w-full")  # Adjust class if needed
        if img_tag and img_tag.get("src"):
            image_url.append(img_tag["src"])
        else:
            image_url.append("Image not found")
    except AttributeError:
        image_url.append("Image not found")

    # Extract ingredients_list from <h3> and corresponding <p>
    try:
        ingredients_list = "ingredients_list not found"
        highlights_div = soup.find("div", id="productHighlights")
        if highlights_div:
            for div in highlights_div.find_all("div", class_="flex items-start gap-3"):
                h3 = div.find("h3")
                if h3 and "ingredients_list" in h3.text.lower():
                    p_tag = div.find("p")
                    if p_tag:
                        ingredients_list = p_tag.text.strip()
                        break
    except AttributeError:
        ingredients_list = "ingredients_list not found"

    
    return title, price, image_url, ingredients_list


# # **Example Usage**
# url = "https://www.zeptonow.com/pn/mtr-3-min-poha/pvid/f1cb2683-de80-41c8-86e3-65d8638063da"  # Replace with a valid Zepto product URL
# title, price, image_urls, ingredients_list = extract_zepto_product_info(url)

# # **Print the extracted data**
# print(f"Title: {title}")
# print(f"Price: {price}")
# print(f"Image URL: {image_urls}")
# print(f"ingredients_list: {ingredients_list}")
