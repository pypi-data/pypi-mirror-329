# scraper.py

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import random
from fake_useragent import UserAgent
import logging
from requests.exceptions import RequestException, ConnectionError, Timeout, HTTPError
from datetime import datetime

# Configure logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Constants
INITIAL_DELAY = 2
RETRY_LIMIT = 3
USER_AGENT_ROTATE = True
RANDOM_DELAY_MIN = 2
RANDOM_DELAY_MAX = 5

# State dictionary
states_dict = {
    "Alabama": "al",
    "Alaska": "ak",
    "Arizona": "az",
    "Arkansas": "ar",
    "California": "ca",
    "Colorado": "co",
    "Connecticut": "ct",
    "Delaware": "de",
    "Florida": "fl",
    "Georgia": "ga",
    "Hawaii": "hi",
    "Idaho": "id",
    "Illinois": "il",
    "Indiana": "in",
    "Iowa": "ia",
    "Kansas": "ks",
    "Kentucky": "ky",
    "Louisiana": "la",
    "Maine": "me",
    "Maryland": "md",
    "Massachusetts": "ma",
    "Michigan": "mi",
    "Minnesota": "mn",
    "Mississippi": "ms",
    "Missouri": "mo",
    "Montana": "mt",
    "Nebraska": "ne",
    "Nevada": "nv",
    "New Hampshire": "nh",
    "New Jersey": "nj",
    "New Mexico": "nm",
    "New York": "ny",
    "North Carolina": "nc",
    "North Dakota": "nd",
    "Ohio": "oh",
    "Oklahoma": "ok",
    "Oregon": "or",
    "Pennsylvania": "pa",
    "Rhode Island": "ri",
    "South Carolina": "sc",
    "South Dakota": "sd",
    "Tennessee": "tn",
    "Texas": "tx",
    "Utah": "ut",
    "Vermont": "vt",
    "Virginia": "va",
    "Washington": "wa",
    "West Virginia": "wv",
    "Wisconsin": "wi",
    "Wyoming": "wy"
}

# Initialize the UserAgent object
ua = UserAgent()

def get_random_user_agent():
    return ua.random if USER_AGENT_ROTATE else ua.chrome

def get_cookies(session, location_url):
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    try:
        response = session.get(location_url, headers=headers, timeout=(5, 10))
        response.raise_for_status()
        logging.info(f"Successfully retrieved cookies from {location_url}")
        return session.cookies
    except (HTTPError, ConnectionError, Timeout, RequestException) as e:
        logging.error(f"Error occurred while retrieving cookies: {e}")
    return None

def make_request(session, url, headers, cookies):
    delay = INITIAL_DELAY
    for attempt in range(1, RETRY_LIMIT + 1):
        try:
            response = session.get(url, headers=headers, cookies=cookies, timeout=(5, 10))
            response.raise_for_status()
            return response
        except (ConnectionError, Timeout, HTTPError, RequestException) as e:
            logging.warning(f"Attempt {attempt}: Error fetching {url}: {e}")
        
        time.sleep(delay + random.uniform(0, 1))  # Jitter
        delay *= 2  # Exponential backoff
    
    logging.error(f"Failed to retrieve {url} after {RETRY_LIMIT} attempts")
    return None

def extract_data_from_page(session, location, listing_type, page):
    url = f'https://www.zillow.com/{location}/{listing_type}/{page}_p/'
    
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept-Language": "en-US,en;q=0.9",
    }
    cookies = get_cookies(session, url)
    
    if not cookies:
        logging.error(f"Failed to retrieve cookies for location {location}. Skipping this location.")
        return None
    
    response = make_request(session, url, headers, cookies)
    
    if not response:
        logging.error(f"Failed to retrieve data from location {location}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    script_tag = soup.find("script", id="__NEXT_DATA__", type="application/json")

    if not script_tag:
        logging.error(f"Script tag not found for location {location}")
        return None

    json_data = json.loads(script_tag.string)
    properties = []
    
    try:
        results = json_data['props']['pageProps']['searchPageState']['cat1']['searchResults']['listResults']
        for result in results:
            property_data = {
                "address": result.get("address"),
                "days_on_zillow": result.get("hdpData", {}).get("homeInfo", {}).get("daysOnZillow"),
                "zestimate": result.get("zestimate"),
                "rent_zestimate": result.get("hdpData", {}).get("homeInfo", {}).get("rentZestimate"),
                "longitude": result.get("latLong", {}).get("longitude"),
                "latitude": result.get("latLong", {}).get("latitude"),
                "area": result.get("area"),
                "img_src": result.get("imgSrc"),
                "beds": result.get("beds"),
                "baths": result.get("baths"),
                "price_change": result.get("hdpData", {}).get("homeInfo", {}).get("priceChange"),
                "tax_assessed_value": result.get("hdpData", {}).get("homeInfo", {}).get("taxAssessedValue"),
                "lot_area_value": result.get("hdpData", {}).get("homeInfo", {}).get("lotAreaValue"),
                "home_type": result.get("hdpData", {}).get("homeInfo", {}).get("homeType"),
                "living_area": result.get("hdpData", {}).get("homeInfo", {}).get("livingArea"),
                "detail_url": result.get("detailUrl"),
                "listing_type": listing_type,
                "scraped_date": datetime.now()  # Add the current date and time
            }
            
            # Handle pricing logic
            if listing_type == "sold":
                property_data["price"] = None
                property_data["soldprice"] = result.get("soldPrice")
            elif listing_type in ["for_sale", "for_rent"]:
                property_data["soldprice"] = None
                property_data["price"] = result.get("price") or "price restricted"
            
            properties.append(property_data)
    except KeyError as e:
        logging.error(f"KeyError: {e} for location {location}")
        return None

    return properties

def scrape_selected_states(selected_states, selected_listing_type):
    all_data = []
    session = requests.Session()  # Reuse the same session for cookie handling
    
    for state_name, state_code in selected_states.items():
        for page in range(1, 21):  # Iterate over 20 pages
            logging.info(f"Scraping {selected_listing_type} listings for {state_name} on page {page}")
            properties = extract_data_from_page(session, state_code, selected_listing_type, page)
            
            if properties:
                all_data.extend(properties)
            
            time.sleep(random.uniform(RANDOM_DELAY_MIN, RANDOM_DELAY_MAX))
    
    df = pd.DataFrame(all_data)
    if selected_listing_type == "sold":
        df.drop(columns=["price"], inplace=True, errors='ignore')
    elif selected_listing_type in ["for_sale", "for_rent"]:
        df.drop(columns=["soldprice"], inplace=True, errors='ignore')
    return df
