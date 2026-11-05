import requests

"""
Plans:

--------------------------------------------------------------------------------------------------------------
Function 1: retrieve_epic_photos(api_key, date)
Description: Requests EPIC photo data for one date and turns the response into a list of dictionaries, one per photo
Parameters:
api_key (string): the NASA API key
date (string): a date in YYYY-MM-DD format
Return value:
Returns a list of dictionaries of EPIC photo data (empty if no photos exist for that date) or None if the status code is not 200

--------------------------------------------------------------------------------------------------------------
Function 2: flightlog_create(photo)
Description: Takes in the dictionary of the photo, searches it for relevant information (date, photo id, etc) and appends a "cleaned" version that consists of the time the photo was taken as well as a link to the photo into a new dictionary
Parameters:
photo (dictionary): the dictionary of the photo
Return value:
Nothing. The dictionary will be handled globally.

--------------------------------------------------------------------------------------------------------------
Function 3: set_date()
Description: Asks the user to input a date, which is then formatted and returned.
Parameters: 
None.
Return value:
The formatted date.

--------------------------------------------------------------------------------------------------------------
Function 4: display_flightlog(flightlog)
Description: uses the flight log (dictionary) filled out by Function 2 and displays it to the user in a more readable form.
Parameters:
flightlog(dictionary): the dictionary created by flightlog_create(photo)
Return value:
Nothing. This instead prints each of the entries in the created dictionary.
--------------------------------------------------------------------------------------------------------------
"""

def retrieve_epic_photos(api_key, date):
    endpoint_url = f"https://api.nasa.gov/EPIC/api/natural/date/{date}"
    params = {
        "api_key": api_key,
    }

    response = requests.get(endpoint_url, params=params)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403:
        print(f"403: The given API code is invalid.")
        return None
    elif response.status_code == 429:
        print(f"429: This API key has been rate limited.")
        return None    
    else:
        print(f"Data not received. Status code: {response.status_code}")
        return None
def set_date():
    # Takes the year, month and day from the user.
    # Then removes spaces and reject if input has too many characters or has numbers.
    # Then combines year, month, and day values into one date string, which is returned.
    year = input("Enter the year (YYYY): ").strip()
    if not year.isdigit() or len(year) != 4:
        print("Invalid year. Year will be set to default.")
        year = "2016"
    month = input("Enter the month (MM): ").strip()
    if not month.isdigit() or len(month) != 2:
        print("Invalid month. Month will be set to default.")
        month = "03"
    day = input("Enter the day (DD): ").strip()
    if not day.isdigit() or len(day) != 2:
        print("Invalid day. Day will be set to default.")
        day = "08"
    date = f"{year}-{month}-{day}"
    return date

if __name__ == "__main__":

    date = "2016-03-08"
    photos = retrieve_epic_photos("DEMO_KEY", date)
"""
    if photos:
        print(f"Photos on this date: {len(photos)}")
        print()
        for photo in photos:
            print(f"{photo}")
    else:
        print("No photos for this date.")
"""

