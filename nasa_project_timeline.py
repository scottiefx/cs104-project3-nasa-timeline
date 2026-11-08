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
Function 2: flightlog_create(photos)
Description: Takes in the dictionaries of the photos, searches them for relevant information (date, photo id, etc) and appends a "cleaned" version that consists of the time the photo was taken as well as a link to the photo into a new dictionary
Parameters:
photos (dictionary): the dictionary of the photo dictionaries
Return value:
The finished dictionary.

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
Function 5: set_api_key()
Description: prompts the user to set an api key, uses DEMO_KEY by default if they dont.
Parameters:
Return value: the api key
--------------------------------------------------------------------------------------------------------------
"""

def retrieve_epic_photos(api_key, date):
    endpoint_url = f"https://api.nasa.gov/EPIC/api/natural/date/{date}"
    params = {
        "api_key": api_key,
    }
    # fetches photos from api
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

def flightlog_create(photos):
    # Creates empty dictionary 'flightlog'
    # For every photo in the photos dictionary,
    # it makes an entry in flightlog that is a dictionary of the photo's date and image
    flightlog = {}
    if photos:
        for photo in photos:
            flightlog[photo['identifier']] = {
                "Date": photo['date'],
                "Image": photo['image']
            }
    return flightlog

def display_flightlog(flightlog):
    # Takes the inputted flightlog dictionary
    # displays how many entries it has
    # and lists each entry's identifier and Date values
    # then creates a link to the photo
    # using the api key, as well as the date created by set_date()
    if not flightlog:
        print("No photos taken on this date.")
    else:
        print(f"Photos on this date: {len(flightlog)}")
        for identifier, photo in flightlog.items():
            print(f"Photo ID: {identifier}\nTime taken: {photo['Date']}")
            p_year = photo['Date'][0:4]
            p_month = photo['Date'][5:7]
            p_day = photo['Date'][8:10]
            print(f"Link to photo: https://api.nasa.gov/EPIC/archive/natural/{p_year}/{p_month}/{p_day}/png/epic_1b_{identifier}.png?api_key={global_api_key}")

def set_api_key():
    # Prompts user, if they choose yes
    # then they are prompted to enter their api key
    # which is then used in display_flightlog and retrieve_epic_photos
    # otherwise, use DEMO_KEY
    user_choice = input("Would you like to set a custom API key? (Y/N) ")
    if user_choice.lower().strip() == "y":
        key = input("Enter your key here: ").strip()
        return key
    else:
        print("Demo API key will be used.")
        key = "DEMO_KEY"
        return key
   
if __name__ == "__main__":
    #introduce program
    print("This program will search the EPIC API for satellite images taken on a specific day.")
    #set the api key
    global_api_key = set_api_key()
    #set the date with set_date()
    print("Please enter the date you wish to view:")
    user_date = set_date()
    #create dictionary using the data gained from the api
    photos = retrieve_epic_photos(global_api_key, user_date)
    #strip dictionary into a new one with specific key/values
    log = flightlog_create(photos)
    #display information provided by new dictionary like time taken and link to view photo
    display_flightlog(log)
