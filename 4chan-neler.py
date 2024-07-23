import requests
from bs4 import BeautifulSoup
import re
import json

def scrape_and_process_website_json(url, target_tag, regex):
    """/
        Scrapes a website, extracts specific tag/content, and
        processes it with regex to output JSON data with an indent of 4.

        If request of url fails an exception of the error is raised and the program quits

    Args:
      url (str): The URL of the website to scrape.
      target_element (str): The HTML tag that contains the desired content.
      regex_pattern (str): The regular expression pattern to match within the content.

        /"""

    try:
      response = requests.get(url)
      response.raise_for_status()  # Raise an exception for non-200 status codes
    except requests.exceptions.ConnectionError as e:
      print(f"Error making request to {url}: {e}")
      return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract target elements based on tag and optional attributes
    if target_tag:
      target_elements = soup.find_all(type = target_tag)  # Find elements with the specified
    else:
      target_elements = soup.find_all(target_tag)  # Find all elements with the tag name

    extracted_data = []
    for element in target_elements[2]:
        if element:
          element_str = str(element)
          matches = re.findall(regex, element_str)
          extracted_data.extend(matches)
          for match in matches:
            try:
                # Assuming the captured data is valid JSON
                json_data = json.loads(match)
                # Access data within json_data (e.g., json_data["date"])
                json_dump = json.dumps(json_data, indent=4)
            except json.JSONDecodeError:
                print(f"Error parsing JSON data: {match}")  # Handle invalid JSON

    return json_dump

def get_key_from_json(json_data):
    """/
        Takes data from json_data and parses it
        to find the name of each of the JSON objects
        /"""
    key_match = re.findall(r'("\d+"): {', f"{json_data}")

    return key_match

def create_dict_from_website_json(page):
    """/
        Args:
            Page to pass into the website_url variable of scrape_and_process_website_json

        scrape_and_process_website_json in function:
            Extracts JSON data from the the Website provided in the
            webite_url (currently 4chan.org) variable and places the page
            arg inside the url to properly request the correct page using the
            scrape_and_process_website_json function.

            The function then uses the target_tag (currently text/javascript)
            variable to assign the tag to search for, and uses the regex pattern in the regex
            variable to properly parse the data and pass it into the json_data
            variable.

        Takes data returned from scrape_and_process_website_json and stores
        it in the json_data variable and then stores the loaded json data into
        jdata_loads.

        The value_key variable uses regex from the get_key_from_json() function
        to return the name of the json object (the data is retuned as strings
        with quotations e.g: '"000000001"','"000000002"')

        The data of value_key is then seperated and stored in a list called data_key.

        The jdata_loads output is then iterated through using the for loop and appends
        the value within the list created from jdata_loads to seppearate the object
        values from the JSON data and places it into the data_value list.

        The page variable creates a dictionary of the values in the lists data_key and data_value.

        The function finally returns the dictionary stored in the page variable.

        /"""
    # Example usage (replace with the actual website URL and your desired content/regex)
    website_url = f"https://boards.4chan.org/{page}/catalog"  # Replace with the target website
    target_tag = "text/javascript"  # Replace with desired type or tag to search for
    regex = r'{"\d+":[\s\S]*}}'  # Replace with your desired regex pattern

    json_data = scrape_and_process_website_json(website_url, target_tag, regex)

    jdata_loads = json.loads(json_data)

    value_key = get_key_from_json(json_data)

    data_key = []
    for key in value_key:
            data_key.append(key)

    data_value = []
    for value in jdata_loads:
        data_value.append(f"{jdata_loads[f"{value}"]}")

    page = dict(zip(data_key,data_value))

    return page


def show_key(page):
    """/
        Extracts the keys from the dictionary
        create_dict_from_website function and
        returns a list of the keys
        /"""
    show_keys = create_dict_from_website_json(page)
    show = list(show_keys.keys())
    return show


def convert_key_to_int(page):
    """/
        Converts the list result from the show_key()
        function and returns a list of intagers
        /"""

    ints = []
    for i in show_key(page):
        ints.append(i.strip('"'))
    return ints

if __name__ == '__main__':
    #   create_dict_from_website_json("b")
    print(f'{convert_key_to_int("b")},\n{show_key("b")}')
