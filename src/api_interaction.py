import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError, RequestException
import time
import logging

# Configuration of logging to output debug-level messages with a timestamp :
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class APIDataFetcher:
    def __init__(self, username, password):
        #APIDataFetcher instance with the provided username and password for basic authentication.
        self.username = username
        self.password = password



    def fetch_data(self, endpoint, max_retries=5):
        """
        Fetching of data from the API's endpoint and retries on failure.

        - endpoint : The API endpoint URL.
        - max_retries : Maximum number of retries for http errors.

        Returns:
        - dict: JSON response that comes as a dictionary.
        """
        auth = HTTPBasicAuth(self.username, self.password)
        headers = {
            'Content-Type': 'application/json'
        }

        for retry in range(max_retries):
            try:
                response = requests.get(endpoint, auth=auth, headers=headers)
                response.raise_for_status()  # Raising httperrorr in cases of bad responses 
                return response.json()  # Return JSON response if everything goes successfuly

            except HTTPError as http_err:
                logging.error(f"HTTP error occurred: {http_err}")
            except RequestException as req_err:
                logging.error(f"Request exception occurred: {req_err}")
            except Exception as err:
                logging.error(f"An error occurred: {err}")

            # Retry logic with exponential backoff
            if retry < max_retries - 1:
                logging.info(f"Retrying... Retry attempt {retry + 1} of {max_retries}")
                time.sleep(2 ** retry)  # Exponential backoff 

        # in cases of all retries fail,there comes raised an exception indicating failure to fetch data
        raise Exception(f"Failed to fetch data from endpoint: {endpoint}")

# Basic API authentication here we have the username and password of API's
USERNAME = 'gcd-test'
PASSWORD = 'V2VsbCBkb25lIG9uIGRlY29kaW5nIHRoaXMsIG1lbnRpb24gdGhpcyBpbiB5b3VyIGludGVydmlldy4='