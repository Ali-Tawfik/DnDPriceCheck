from utils.smart_match import match_attr,attribute_to_acrynom
from utils.fetch_db import fetch_darkerdb_data
from datetime import datetime, timedelta
import statistics

def filter_by_days(data,action="sold",days_thresh=5):
    today = datetime.today()
    threshold_date = today - timedelta(days=days_thresh)
    # breakpoint()
    filtered_items = [item for item in data["body"]
    if datetime.strptime(item[f"{action}_at"], "%Y-%m-%d %H:%M:%S") > threshold_date
    ]
    return data

def check_secondary_prices(lines):
    result_dict = match_attr(lines)
    result=[]
    for attribute, val in result_dict["secondary"].items():
        data = fetch_darkerdb_data(result_dict["item_name"], result_dict["rarity"], price_range=None, secondary_attribute=[attribute, f"<={val}"], condense='1')
        if isinstance(data, str):
            print(data)
            continue
        try:
            data=filter_by_days(data)
        except:
            print("no sold")
        stats = calculate_price_stats(data)
        print(stats)
        if not isinstance(stats, str):
            result.append(f"{attribute_to_acrynom(attribute)} - {stats['median_price']} - [{stats['min_price']},{stats['average_price']},{stats['max_price']}]")
    final_string="\n".join(result)
    print(final_string)
    return final_string

def calculate_price_stats(data):
    if not isinstance(data, dict) or 'body' not in data:
        return "Invalid data format"

    items = data['body']
    if not items:
        return "No items found"

    prices = [item['price'] for item in items if 'price' in item]

    if not prices:
        return "No prices found"

    average_price = round(sum(prices) / len(prices))
    min_price = min(prices)
    max_price = max(prices)
    median_price = statistics.median(prices)

    return {
        'average_price': average_price,
        'min_price': min_price,
        'max_price': max_price,
        'median_price':median_price
    }
