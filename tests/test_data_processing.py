import sys
import os
import unittest
from unittest.mock import MagicMock, patch
import datetime
# ensuring the src directory is in the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from data_processing import DataProcessor

class TestDataProcessor(unittest.TestCase):
    
    def setUp(self):
        # Mocking data for vq and tq endpoints of our ApIs
        self.vq_data = {
            "results": [
                {
                    "rights": {
                        "terms": [
                            {
                                "devices": [{"devicePlatform": "ROKU"}],
                                "startDateTime": "2024-01-01T00:00:00Z",
                                "endDateTime": "2024-12-31T23:59:59Z"
                            }
                        ]
                    },
                    "localizableInformation": [
                        {"titleNameMedium": "Title 1"}
                    ],
                    "contentId": "1"
                }
            ]
        }
        self.tq_data = {
            "results": [
                {
                    "contentId": "1",
                    "assets": [
                        {
                            "videoFormat": "HD",
                            "endpoints": [{"origin": "level3", "path": "/path/to/manifest"}]
                        }
                    ]
                }
            ]
        }

    # function to test data titles playable on ROKU
    def test_get_titles_for_device(self):
        processor = DataProcessor(self.vq_data, self.tq_data)
        titles = processor.get_titles_for_device("ROKU")
        self.assertEqual(titles, ["Title 1"])


    # function to test filtering for currently active items based on todays date
    @patch('data_processing.datetime')
    def test_filter_currently_active_items(self, mock_datetime):
        processor = DataProcessor(self.vq_data, self.tq_data)
        current_date = datetime.datetime(2024, 6, 19)
        mock_datetime.datetime.now.return_value = current_date
        mock_datetime.datetime.fromisoformat.side_effect = datetime.datetime.fromisoformat

        active_items = processor.filter_currently_active_items(["Title 1"])
        self.assertEqual(len(active_items), 1)
        self.assertEqual(active_items[0][0], "Title 1")

    # function to test data filtered only to get Level3 HD manifest paths for currently active items
    @patch('data_processing.datetime')
    def test_get_level3_hd_manifest_paths(self, mock_datetime):
        processor = DataProcessor(self.vq_data, self.tq_data)
        current_date = datetime.datetime(2024, 6, 15)
        mock_datetime.datetime.now.return_value = current_date
        mock_datetime.datetime.fromisoformat.side_effect = datetime.datetime.fromisoformat
        manifest_paths = processor.get_level3_hd_manifest_paths()
        self.assertEqual(manifest_paths, ["/path/to/manifest"])

if __name__ == "__main__":
    unittest.main()