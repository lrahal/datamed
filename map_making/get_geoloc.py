"""
Python script for batch geocoding of addresses using the Google Geocoding API.
This script allows for massive lists of addresses to be geocoded for free by pausing when the 
geocoder hits the free rate limit set by Google (2500 per day). If you have an API key for paid
geocoding from Google, set it in the API key section.
Addresses for geocoding can be specified in a list of strings "addresses". In this script, addresses
come from a dataframe's column, but it can be loaded from a csv file.
After every 500 successful geocode operations, a temporary file with results is recorded in case of
script failure / loss of connection later.
Addresses and data are held in memory, so this script may need to be adjusted to process files line
by line if you are processing millions of entries.
"""

import pandas as pd
import requests
import logging
import urllib
import time
import json
import os
import re

logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

# ------------------ CONFIGURATION -------------------------------

# Set your Google API key here.
# Even if using the free 2500 queries a day, its worth getting an API key since the rate limit is 50 / second.
# With API_KEY = None, you will run into a 2 second delay every 10 requests or so.
# With a "Google Maps Geocoding API" key from https://console.developers.google.com/apis/,
# the daily limit will be 2500, but at a much faster rate.
# Example: API_KEY = 'AIzaSyC9azed9tLdjpZNjg2_kVePWvMIBq154eA'
API_KEY = os.environ.get('GCP_KEY')
# Google Maps URL
BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'
# Backoff time sets how many minutes to wait between google pings when your API limit is hit
BACKOFF_TIME = 30
# Set your output file name here.
output_folder_path = '/Users/linerahal/Documents/GitHub/datamed/data/'
# Return Full Google Results? If True, full JSON results from Google are included in output
RETURN_FULL_RESULTS = False

# ------------------	FUNCTION DEFINITIONS ------------------------

def get_google_results(address):
    """
    Get geocode results from Google Maps Geocoding API.

    Note, that in the case of multiple google geocode reuslts, this function returns details of the FIRST result.

    @param address: String address as accurate as possible. For Example "18 Grafton Street, Dublin, Ireland"
    @param api_key: String API key if present from google.
                    If supplied, requests will use your allowance from the Google API. If not, you
                    will be limited to the free usage of 2500 requests per day.
    @param return_full_response: Boolean to indicate if you'd like to return the full response from google. This
                    is useful if you'd like additional location details for storage or parsing later.
    """
    # Set up your Geocoding url
    address = re.sub(' +', ' ', address)  # Remove multiple spaces
    parameters = {'address': address, 'key': API_KEY}
    geocode_url = f"{BASE_URL}{urllib.parse.urlencode(parameters)}"

    # Ping google for the results:
    results = requests.get(geocode_url)
    # Results will be in JSON format - convert to dict using requests functionality
    results = results.json()

    # if there's no results or an error, return empty results.
    if len(results['results']) == 0:
        output = {
            "formatted_address": None,
            "latitude": None,
            "longitude": None,
            "accuracy": None,
            "google_place_id": None,
            "type": None,
            "postcode": None,
            "country": None,
        }
    else:
        answer = results['results'][0]
        output = {
            "formatted_address": answer.get('formatted_address'),
            "latitude": answer.get('geometry').get('location').get('lat'),
            "longitude": answer.get('geometry').get('location').get('lng'),
            "accuracy": answer.get('geometry').get('location_type'),
            "google_place_id": answer.get("place_id"),
            "type": ",".join(answer.get('types')),
            "postcode": ",".join([x['long_name'] for x in answer.get('address_components')
                                  if 'postal_code' in x.get('types')],),
            "country": next((x['long_name'] for x in answer.get('address_components')
                             if 'country' in x.get('types')), None)
        }

    # Append some other details:
    output['input_string'] = address
    output['number_of_results'] = len(results['results'])
    output['status'] = results.get('status')
    if RETURN_FULL_RESULTS is True:
        output['response'] = results

    return output


# ------------------ PROCESSING LOOP -----------------------------

def get_locations(df, output_filename, nb_addresses=20):
    # Form a list of addresses for geocoding:
    # Make a big list of all of the addresses to be processed.
    # addresses = data[address_column_name].tolist()
    addresses = df.site_name.unique()

    test_result = get_google_results("London, England")
    if (test_result['status'] != 'OK') or (test_result['formatted_address'] != 'London, UK'):
        logger.warning("There was an error when testing the Google Geocoder.")
        raise ConnectionError('Problem with test results from Google Geocode '
                              '- check your API key and internet connection.')

    # Create a list to hold results
    results = []
    # Go through each address in turn
    for address in addresses[:nb_addresses]:
        # While the address geocoding is not finished:
        geocoded = False
        while geocoded is not True:
            # Geocode the address with google
            try:
                geocode_result = get_google_results(address)
            except Exception as e:
                logger.exception(e)
                logger.error("Major error with {}".format(address))
                logger.error("Skipping!")
                geocoded = True

            # If we're over the API limit, backoff for a while and try again later.
            if geocode_result['status'] == 'OVER_QUERY_LIMIT':
                logger.info("Hit Query Limit! Backing off for a bit.")
                time.sleep(BACKOFF_TIME * 60)  # sleep for 30 minutes
                geocoded = False
            else:
                # If we're ok with API use, save the results
                # Note that the results might be empty / non-ok - log this
                if geocode_result['status'] != 'OK':
                    logger.warning("Error geocoding {}: {}".format(address, geocode_result['status']))
                logger.debug("Geocoded: {}: {}".format(address, geocode_result['status']))
                results.append(geocode_result)
                geocoded = True

        # Print status every 100 addresses
        if len(results) % 100 == 0:
            logger.info("Completed {} of {} address".format(len(results), len(addresses)))

        # Every 500 addresses, save progress to file(in case of a failure so you have something!)
        if len(results) % 500 == 0:
            pd.DataFrame(results).to_csv("{}_bak".format(output_folder_path + output_filename))

    # All done
    logger.info("Finished geocoding all addresses")
    # Write the full results to csv using the pandas library.
    pd.DataFrame(results).to_csv(output_folder_path + output_filename, encoding='utf8')