import requests,json,random

def fetch_api_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  # Assuming API returns JSON data
        else:
            print(f"Error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Example usage
api_url = "https://fakestoreapi.com/products"
data = fetch_api_data(api_url)
if data:

    json_data = json.dumps(data, indent=2)
    for item in data:
        if 'rating' in item:
            del item['rating']
        if 'quantity/available' in item:
            del item['quantity/available']
        item['rating'] = random.randint(3,5)
        item['available'] = random.randint(15,20)
    json_data_updated = json.dumps(data, indent=2)

    items = json.loads(json_data_updated)
    items = [item for item in items if item['category'] not in ['electronics', 'jewelery']]
    for index, item in enumerate(items):
        item["id"] = index + 1
    updated_json_data = json.dumps(items, indent=2)


    with open("Product_Details.json", "w") as file:
        file.write(updated_json_data)

else:
    print("Failed to fetch API data.")
