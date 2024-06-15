import requests
import logging
import time
import csv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_data_with_retry(url, retries=3, delay=4):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises HTTPError for bad responses
            if response.text:
                return response.json()
            else:
                logger.error(f"Attempt {attempt + 1} failed: Empty response for URL {url}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
        except ValueError:
            logger.error(f"Attempt {attempt + 1} failed: Invalid JSON response")
        time.sleep(delay)
    return None

def is_item_rising(item_data):
    trend30 = item_data['day30']['trend']
    trend90 = item_data['day90']['trend']
    trend180 = item_data['day180']['trend']

    # Check if all trends are positive
    return (trend30 == 'positive' or trend30 == 'neutral') and (trend90 == 'positive' or trend90 == 'neutral') and (trend180 == 'positive' or trend180 == 'neutral')

def estimate_margin(item_data):
    price = item_data['current']['price']
    if isinstance(price, str):
        current_price = int(price.replace(',', '').replace('k', '000').replace('m', '000000').replace('.', ''))
    else:
        current_price = price

    # Basic estimation logic for margin (example only)
    estimated_buy_price = int(current_price * 0.95)  # Assuming a 5% lower buy price
    estimated_sell_price = int(current_price * 1.05)  # Assuming a 5% higher sell price
    margin = estimated_sell_price - estimated_buy_price

    return estimated_buy_price, estimated_sell_price, margin

def fetch_item_details(item_ids):
    detail_url = "https://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item={}"
    positive_items = []
    for item_id in item_ids:
        url = detail_url.format(item_id)
        logger.info(f"Fetching details for item ID: {item_id} from URL: {url}")
        data = fetch_data_with_retry(url)
        if data:
            logger.info(f"Fetched details for item ID: {item_id}: {data}")
            item_data = data['item']
            if is_item_rising(item_data):
                estimated_buy, estimated_sell, margin = estimate_margin(item_data)
                if margin > 0:
                    positive_items.append({
                        'id': item_id,
                        'name': item_data['name'],
                        'estimated_buy_price': estimated_buy,
                        'estimated_sell_price': estimated_sell,
                        'margin': margin
                    })
                    logger.info(f"Rising Item - Estimated Buy Price: {estimated_buy}, Estimated Sell Price: {estimated_sell}, Margin: {margin}")
            else:
                logger.info(f"Item ID: {item_id} is not showing a consistent rising trend.")
        else:
            logger.warning(f"Failed to fetch details for item ID: {item_id}")

    # Save positive items to a CSV file
    save_to_csv(positive_items)

def save_to_csv(items):
    keys = items[0].keys() if items else []
    with open('positive_items.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        for item in items:
            # Ensure the prices and margin are integers
            item['estimated_buy_price'] = int(item['estimated_buy_price'])
            item['estimated_sell_price'] = int(item['estimated_sell_price'])
            item['margin'] = int(item['margin'])
            dict_writer.writerow(item)
    logger.info(f"Saved {len(items)} items to positive_items.csv")

def main():
    base_url = "https://services.runescape.com/m=itemdb_rs/api/catalogue/items.json"
    letters = 'abcdefghijklmnopqrstuvwxyz'
    category = 41  # https://runescape.wiki/w/Application_programming_interface#category
    all_fetched_items = []

    for letter in letters:
        page = 1
        while True:
            url = f"{base_url}?category={category}&alpha={letter}&page={page}"
            logger.info(f"Checking URL: {url}")
            data = fetch_data_with_retry(url)
            if data and data.get("items"):
                all_fetched_items.extend(data["items"])
                logger.info(f"Letter '{letter}', Page {page} fetched items: {len(data['items'])}")
                page += 1
            else:
                logger.warning(f"Letter '{letter}', Page {page} returned no items or reached the end")
                break

    logger.info(f"Total items fetched: {len(all_fetched_items)}")

    # Fetch details for all fetched items
    item_ids = [item["id"] for item in all_fetched_items]
    fetch_item_details(item_ids)

if __name__ == "__main__":
    main()
import requests
import logging
import time
import csv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_data_with_retry(url, retries=3, delay=4):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises HTTPError for bad responses
            if response.text:
                return response.json()
            else:
                logger.error(f"Attempt {attempt + 1} failed: Empty response for URL {url}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
        except ValueError:
            logger.error(f"Attempt {attempt + 1} failed: Invalid JSON response")
        time.sleep(delay)
    return None

def is_item_rising(item_data):
    trend30 = item_data['day30']['trend']
    trend90 = item_data['day90']['trend']
    trend180 = item_data['day180']['trend']

    # Check if all trends are positive
    return (trend30 == 'positive' or trend30 == 'neutral') and (trend90 == 'positive' or trend90 == 'neutral') and (trend180 == 'positive' or trend180 == 'neutral')

def estimate_margin(item_data):
    price = item_data['current']['price']
    if isinstance(price, str):
        current_price = int(price.replace(',', '').replace('k', '000').replace('m', '000000').replace('.', '').replace('b', '000000000'))
    else:
        current_price = price

    # Basic estimation logic for margin (example only)
    estimated_buy_price = int(current_price * 0.95)  # Assuming a 5% lower buy price
    estimated_sell_price = int(current_price * 1.05)  # Assuming a 5% higher sell price
    margin = estimated_sell_price - estimated_buy_price

    return estimated_buy_price, estimated_sell_price, margin

def fetch_item_details(item_ids):
    detail_url = "https://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item={}"
    positive_items = []
    for item_id in item_ids:
        url = detail_url.format(item_id)
        logger.info(f"Fetching details for item ID: {item_id} from URL: {url}")
        data = fetch_data_with_retry(url)
        if data:
            logger.info(f"Fetched details for item ID: {item_id}: {data}")
            item_data = data['item']
            if is_item_rising(item_data):
                estimated_buy, estimated_sell, margin = estimate_margin(item_data)
                if margin > 0:
                    positive_items.append({
                        'id': item_id,
                        'name': item_data['name'],
                        'estimated_buy_price': estimated_buy,
                        'estimated_sell_price': estimated_sell,
                        'margin': margin
                    })
                    logger.info(f"Rising Item - Estimated Buy Price: {estimated_buy}, Estimated Sell Price: {estimated_sell}, Margin: {margin}")
            else:
                logger.info(f"Item ID: {item_id} is not showing a consistent rising trend.")
        else:
            logger.warning(f"Failed to fetch details for item ID: {item_id}")

    # Save positive items to a CSV file
    save_to_csv(positive_items)

def save_to_csv(items):
    keys = items[0].keys() if items else []
    with open('positive_items.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        for item in items:
            # Ensure the prices and margin are integers
            item['estimated_buy_price'] = int(item['estimated_buy_price'])
            item['estimated_sell_price'] = int(item['estimated_sell_price'])
            item['margin'] = int(item['margin'])
            dict_writer.writerow(item)
    logger.info(f"Saved {len(items)} items to positive_items.csv")

def main():
    base_url = "https://services.runescape.com/m=itemdb_rs/api/catalogue/items.json"
    letters = 'abcdefghijklmnopqrstuvwxyz'
    category = 16  # https://runescape.wiki/w/Application_programming_interface#category
    all_fetched_items = []

    for letter in letters:
        page = 1
        while True:
            url = f"{base_url}?category={category}&alpha={letter}&page={page}"
            logger.info(f"Checking URL: {url}")
            data = fetch_data_with_retry(url)
            if data and data.get("items"):
                all_fetched_items.extend(data["items"])
                logger.info(f"Letter '{letter}', Page {page} fetched items: {len(data['items'])}")
                page += 1
            else:
                logger.warning(f"Letter '{letter}', Page {page} returned no items or reached the end")
                break

    logger.info(f"Total items fetched: {len(all_fetched_items)}")

    # Fetch details for all fetched items
    item_ids = [item["id"] for item in all_fetched_items]
    fetch_item_details(item_ids)

if __name__ == "__main__":
    main()
