import requests

def retrieve_epic_photos(api_key, date):
    endpoint_url = f"https://api.nasa.gov/EPIC/api/natural/date/{date}"
    params = {"api_key": api_key}

    response = requests.get(endpoint_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Data not received. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    photos = retrieve_epic_photos("DEMO_KEY", "2016-03-08")

    if photos:
        print(f"Photos on this date: {len(photos)}")
        print()
        for key, value in photos[0].items():
            print(f"{key}: {value}")
    else:
        print("No photos for this date.")
