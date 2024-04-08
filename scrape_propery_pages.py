# Standard
import json
import logging

# Request library
import requests


def main():
    """
    Fetch the room id data from the badi API and save it to a json file
    """
    URL = "https://api.badiapp.com/v1/application/search/rooms/markers"

    # All the parameters you want to send in the query string
    params = {
        "page": 1,
        "per": 10000,
        "price_types[]": 3,
        # TODO Adjust the bounds to the area you want to search
        "bounds[ne][lat]": 41.421027,
        "bounds[ne][lng]": 2.211315,
        "bounds[sw][lat]": 41.363462,
        "bounds[sw][lng]": 2.119133,
        "sort_by": "relevance",
        # TODO change the max_price to the max price you want to search
        "max_price": 650,
        # TODO change the available_from to the date you want to search from
        "available_from": "2024-04-20",
        "length_of_stay[]": "short",
        "place_types[]": 1,
        "marketplace_segments[]": "badi_community",
    }

    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer 21c08ecc583ae9cef7c003ad63b1f218942ce9e134e8574e91552f98f5a9d575",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    # Make the GET request
    response = requests.get(URL, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response if needed, for example, print the JSON response
        rooms_data: dict[str, any] = response.json()
    else:
        print(response.text)
        print("Failed to fetch data: ", response.status_code)
        return

    with open("rooms_data.json", "w") as f:
        json.dump(rooms_data, f, indent=4)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
