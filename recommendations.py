import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

def scrape_products(search_term=""):
    search_term_encoded = search_term.replace(" ", "+")
    base_url = "https://www.secureshe.com"
    url = f"{base_url}{search_term_encoded}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []
    
    # Update the selector based on actual HTML structure
    for item in soup.select('.s-main-slot .s-result-item'):
        title = item.h2.text.strip() if item.h2 else "No title available"
        link = item.h2.a['href'] if item.h2 and item.h2.a else "#"
        products.append({'title': title, 'link': link})
    
    return products

# Streamlit app setup remains the same
st.set_page_config(page_title="Product Recommendations", page_icon="🛒")
st.title("Product Recommendations")
st.markdown("## Find amazing products just for you!")

search_term = st.text_input("Search for a product:", placeholder="e.g., Bathing soap")

if search_term:
    products = scrape_products(search_term)
    time.sleep(1)  # Adding a delay between requests
    
    if products:
        st.markdown("### Recommended Products:")
        for product in products:
            st.write(f"- [{product['title']}]({product['link']})")
    else:
        st.warning("No products found. Please try another search term.")
