
import sys
import os
from tabulate import tabulate  # Correct import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.fetch_db import fetch_darkerdb_data
from dnd_process import calculate_price_stats,filter_by_days
items_recipes = {
    "Gold Coin Bag": {"Troll Pelt": 1, "Wolf Pelt": 4},
    **{f"{ore} Ingot": {f"{ore} Ore": 3} for ore in ["Froststone", "Gold", "Rubysilver"]},
    **{f"{ore} Powder": {f"{ore} Ore": 2} for ore in ["Froststone", "Gold", "Rubysilver"]}
    # Add more recipes here as needed
    # "Another Item": {"Material1": 2, "Material2": 3},
}
def check_price_min_max(item="Troll Pelt"):
    result={}
    # breakpoint()
    data = fetch_darkerdb_data(item, rarity=None, price_range=None, secondary_attribute=None, limit=None, condense=None,has_sold=0)
    data = filter_by_days(data,action='created')
    result["listed"]=calculate_price_stats(data)
    data = fetch_darkerdb_data(item, rarity=None, price_range=None, secondary_attribute=None, limit=None, condense=None,has_sold=1)
    data = filter_by_days(data,action='sold')
    result["sold"]=calculate_price_stats(data)
    return result


def get_craft_price(item="Gold Coin Bag"):
    if item not in items_recipes:
        return {"error": f"No recipe found for {item}"}

    # Get the recipe for the item
    craft_items = items_recipes[item]

    # Fetch prices for all items in the recipe
    item_prices = {}
    for c_item in craft_items.keys():
        item_prices[c_item] = check_price_min_max(c_item)
    item_prices[item] = check_price_min_max(item)

    # Calculate crafting cost dynamically
    craft_cost = {c_item: item_prices[c_item]['sold']['median_price'] * qty for c_item, qty in craft_items.items()}
    craft_cost_tot = sum(craft_cost.values())

    # Get selling price
    selling_price = item_prices[item]['sold']['median_price']

    # Compute profit or loss
    profit = selling_price - craft_cost_tot

    # Return all information as a dictionary
    return {
        "item": item,
        "craft_cost": craft_cost,
        "total_craft_cost": craft_cost_tot,
        "selling_price": selling_price,
        "profit": profit,
    }
        


if __name__ == "__main__":
    #  Run multiple recipes
    results = []
    for item in items_recipes.keys():
        result = get_craft_price(item)
        results.append([
            result["item"],
            result["total_craft_cost"],
            result["selling_price"],
            result["profit"],
        ])

    # Print results in a table
    headers = ["Item", "Crafting Cost", "Selling Price", "Profit"]
    print(tabulate(results, headers=headers, tablefmt="grid"))
# craft_price = {
#     "coin_bag": price_dict["troll_pelt"] + 4 * price_dict["wolf_pelt"],
#     "cobalt_armor": 10 * price_dict["cobalt_ingot"],
#     "rubysilver_cuirass": 10 * price_dict["rubysilver_ingot"],
#     # Add more items and their crafting costs as needed
# }