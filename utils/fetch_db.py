import requests


def fetch_darkerdb_data(item, rarity=None, price_range=None, secondary_attribute=None, limit=None, condense=None,has_sold=None):
    # Base URL for the DarkerDB API
    base_url = 'https://api.darkerdb.com/v1/market'

    # Query parameters
    params = {
        'item': item,
    }

    # Add optional parameters if they are provided
    if rarity is not None:
        params['rarity'] = rarity
    if price_range is not None:
        params['price'] = price_range
    if secondary_attribute is not None:
        params[f'secondary[{secondary_attribute[0]}]'] = secondary_attribute[1]
    if limit is not None:
        params['limit'] = limit
    if condense is not None:
        params['condense'] = condense
    if has_sold is not None:
        params['has_sold'] = has_sold
    # Make the GET request
    response = requests.get(base_url, params=params)
    full_url = response.url

    # Print the full URL
    print("Full URL:", full_url)
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Return the JSON response from the API
    else:
        return f"Failed to retrieve data: {response.status_code}"

# Main test case
if __name__ == "__main__":
    # Test case parameters
    item = 'Lightfoot Boots'
    rarity = 'Rare|Epic'
    price_range = '50:500'  # Optional
    secondary_attribute = ['additional_move_speed','5']  # Optional
    limit = '5'  # Optional
    condense = '1'  # Optional

    # Fetch data using the function
    result = calculate_price_statistics(fetch_darkerdb_data(item, rarity, price_range, secondary_attribute, limit, condense))

    # Print the result
    print(result)