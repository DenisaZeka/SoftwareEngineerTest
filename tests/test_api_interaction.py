import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from requests.exceptions import HTTPError
# ensuring that src directory is in the sys path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from api_interaction import APIDataFetcher, USERNAME, PASSWORD

class TestAPIDataFetcher(unittest.TestCase):

    #@patch Decorator is used to mock the requests.get method
    @patch('api_interaction.requests.get') 
    def test_fetch_data_success(self, mock_get):
        # Mock the response to return a successful JSON response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None  
        mock_response.json.return_value = {"key": "value"}  
        mock_get.return_value = mock_response

        # creating of an instance of APIDataFetcher with mock credentials and call fetch_data method with a fake endpoint just for testing purpose
        fetcher = APIDataFetcher(USERNAME, PASSWORD)
        response = fetcher.fetch_data("http://fake-endpoint")
        
        self.assertEqual(response, {"key": "value"})
        mock_get.assert_called_once_with("http://fake-endpoint", auth=unittest.mock.ANY, headers={'Content-Type': 'application/json'})



    @patch('api_interaction.requests.get') 
    def test_fetch_data_failure(self, mock_get):
        # Mock the response to raise an HTTPError in cases when raise_for_status is called
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = HTTPError("HTTP Error")
        mock_get.return_value = mock_response

        #creating an instance of APIDataFetcher with mock credentials and call fetch_data method with a fake endpoint just for testing purpose with retries max 3
        fetcher = APIDataFetcher(USERNAME, PASSWORD)
        with self.assertRaises(Exception) as context:
            fetcher.fetch_data("http://fake-endpoint", max_retries=3)

        #in cases of faliure :
        self.assertTrue("Failed to fetch data from endpoint: http://fake-endpoint" in str(context.exception))
        self.assertEqual(mock_get.call_count, 3)

if __name__ == "__main__":
    unittest.main()
