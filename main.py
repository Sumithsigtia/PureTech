import streamlit as st
from google import genai

# Importing custom scraping functions
from amazon import extract_amazon_product_info
from flipkart import extract_flipkart_product_info
from bigbasket import extract_bigbasket_product_info
from zepto import extract_zepto_product_info

# Set Streamlit theme
st.set_page_config(page_title="PureTech")

# Title and description
st.markdown("<h1 style='text-align: center;'>PureTech</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Uncover the secrets of beloved Products</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Securely sorted and wisely chosen</p>", unsafe_allow_html=True)

# Input for the product URL
url = st.text_input('Enter Product URL:')

if url:
    # Identify the website
    if 'amazon' in url:
        website_name = 'Amazon'
    elif 'flipkart' in url:
        website_name = 'Flipkart'
    elif 'bigbasket' in url:
        website_name = 'BigBasket'
    elif 'zepto' in url:
        website_name = 'Zepto'
    else:
        website_name = None

    if website_name:
        try:
            # Extract product information
            if website_name == 'Amazon':
                title, price, image_url, ingredients_list = extract_amazon_product_info(url)
            elif website_name == 'Flipkart':
                title, price, image_url, ingredients_list = extract_flipkart_product_info(url)
            elif website_name == 'BigBasket':
                title, price, _, ingredients_list = extract_bigbasket_product_info(url)
                image_url = None  # No image for BigBasket
            elif website_name == 'Zepto':
                title, price, image_url, ingredients_list = extract_zepto_product_info(url)

            if title and price:
                # Display product details
                st.subheader(title)
                st.write(f"**Price:** {price}")
                if image_url:
                    st.image(image_url, caption='Product Image')

                # Load API Key
                GOOGLE_API_KEY = st.secrets["api_keys"]["google_api_key"]

                # Initialize Gemini API
                client = genai.Client(api_key=GOOGLE_API_KEY)
                chat = client.chats.create(model="gemini-2.0-flash")

                if st.button('Analyze Your Product'):
                    with st.expander("Ingredients Analysis"):
                        # Get ingredients from Gemini
                        response = chat.send_message(
                            f"Please list all the ingredients of {title}, if unavailable, try alternative sources. This is the available ingredients on the url: {ingredients_list}. return the merged ingredient_list making sure not to repeat stuff"
                        )
        
                        final_response = chat.send_message(
                            f"Here is the merged ingredient list: {response}. "
                            "Without repeating a single ingredient just list them and Analyze and mark ✅ for safe ingredients and ❌ for unhealthy ones. keep it short and simple"
                        )
                        safety_score_response = chat.send_message(
                            f"Compute the safety score based on unhealthy ingredients in {final_response.text}. "
                            "Use this formula: safety_score = 100 - (4 * number of unhealthy ingredients). Return only the score only once."
                        )
                        st.markdown(final_response.text)
                        st.markdown(f"**Safety Score:** {safety_score_response.text}")

                    with st.expander("Harmful Ingredient Effects"):
                        harmful_analysis = chat.send_message(
                            f"List the unhealthy ingredients in {title} and their health effects in a table format."
                        )
                        st.markdown(harmful_analysis.text)

                    with st.expander("Better Alternatives & Reviews"):
                        category_recommendation = chat.send_message(
                            f"Recommend a better alternative for {title} with an {url} link."
                        )
                        reviews_summary = chat.send_message(
                            f"Analyze the top 5 reviews of {title} from {url}. Summarize sentiment in max 4 lines."
                        )
                        st.write(category_recommendation.text)
                        st.write(reviews_summary.text)
            else:
                st.error("Could not extract product information. Please check the URL.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

    else:
        st.error("Invalid URL. Please enter a valid product URL.")

st.markdown("<p style='text-align: center;'>Made by - Sumith, Vidhan, Swathi, and Venkat</p>", unsafe_allow_html=True)
