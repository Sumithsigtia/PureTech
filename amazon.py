import requests
from bs4 import BeautifulSoup

def ensure_https(url):
        if not url.startswith("http"):
            return "https://" + url
        return url

def extract_amazon_product_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch page:", response.status_code)
        return None, None, None, None

    soup = BeautifulSoup(response.text, 'html.parser')


    # Scrape product title
    title_element = soup.select_one('#productTitle')
    title = title_element.text.strip() if title_element else "Not found"

    # Scrape product price
    price_element = soup.select_one('span.a-offscreen')
    price = price_element.text.strip() if price_element else "Not found"

    # Scrape product image (better approach)
    image_element = soup.select_one('#landingImage')
    if image_element and 'data-a-dynamic-image' in image_element.attrs:
        image_url = list(eval(image_element.attrs['data-a-dynamic-image']).keys())[0]
    else:
        image_url = "Not found"

    # Scrape product ingredients (multiple possible locations)
    ingredients_list = []
    
    # Check the 'important-information' section
    ingredients_element = soup.find('div', {'id': 'important-information'})
    if ingredients_element:
        ingredient_text = ingredients_element.get_text()
        if "Ingredients" in ingredient_text:
            ingredients_list = ingredient_text.split("Ingredients:")[1].split(".")[0].split(",")
            ingredients_list = [i.strip() for i in ingredients_list]

    # Check bullet points (backup method)
    if not ingredients_list:
        bullet_points = soup.select('#feature-bullets ul li span')
        for bullet in bullet_points:
            text = bullet.text.strip()
            if "Ingredients" in text:
                ingredients_list = text.split(":")[1].split(",")
                ingredients_list = [i.strip() for i in ingredients_list]
                break

    return title, price, image_url, ingredients_list

# # Example Usage
# url = "amazon.in/Lays-Magic-Masala-52g/dp/B002YZHXH2/ref=sr_1_2?dib=eyJ2IjoiMSJ9.p6b09L4UjsknpgXVHJXo9bfq8v88wckAXHXEwvBnX4k-t31w42PPDdtyTZjB3eKE9lGad47lJpkynHATS1BvPCbl-sEKEFliNjtBfoQNOJCw1YsT0StsQBW1aYp3mk6vKHf82k8UrDbciuxM-gBUCYvHTPJvziGsy59Vli6OEmW8hmb3aF_Szt3Yr3PuRuB8UG63XrjMZh7puJN1_aQzDfFDnBTinwm2AMyNEWH8Dk2GtIj66L_khnssoZX4dahGLSJjcO92Ny3wjgk5AX8l_WNrCbyktAth6_iskYntH5Eg_3cFWy7jLkED9gLIaM_o-dUGmkrCfi8Ygaiqe_lC-QIZDQtJJUcvMJDTg1RrMMQyYd3MFxcymWvHJ9MUZoRbiDuhWNA36CxvlLgqlcqCi2f-OYK0HXzGAYpxKIRdwjUzCSvsQwsmsEHY6x3Fp92l.zuGPpqFdTafw2rqEuKc-TVv51fGPzz3rY_Oy9kwMt7o&dib_tag=se&keywords=lays&nsdOptOutParam=true&qid=1743444388&sr=8-2&th=1"
# url = ensure_https(url)
# title, price, image, ingredients = extract_amazon_product_info(url)
# print(f"Title: {title}\nPrice: {price}\nImage: {image}\nIngredients: {ingredients}")
