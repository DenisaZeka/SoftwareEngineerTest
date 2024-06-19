import datetime
import logging

class DataProcessor:
    def __init__(self, vq_data, tq_data):
        self.vq_data = vq_data
        self.tq_data = tq_data
        self.logger = logging.getLogger(__name__)


    def get_titles_for_device(self, device_platform):
        """
        Extracts titles that can be played on a specific device platform from API data.
        
        - device_platform (str): The device platform to filter titles for.
        
        Returns:
        - list: List of titles playable on the specified device platform.
        """
        titles = []
        for entry in self.vq_data.get('results', []):
            rights = entry.get('rights', {})
            terms = rights.get('terms', [])
            for term in terms:
                devices = term.get('devices', [])
                for device in devices:
                    if device['devicePlatform'] == device_platform:
                        local_info = entry.get('localizableInformation', [])
                        for info in local_info:
                            title = info.get('titleNameMedium')
                            if title:
                                titles.append(title)
                        break  # using continue to skip if date parsing fails
        return titles



    def filter_currently_active_items(self, titles_for_roku):
        """
        Filters currently active items based on start and end dates.
        
        - titles_for_roku (list): List of titles to filter for currently active items.
        
        Returns:
        - list: List of currently active items with their details (title, start date, end date).
        """
        current_date = datetime.datetime.now()
        active_items = []

        for title in titles_for_roku:
            for entry in self.vq_data.get('results', []):
                local_info = entry.get('localizableInformation', [])
                for info in local_info:
                    if info.get('titleNameMedium') == title:
                        rights = entry.get('rights', {})
                        terms = rights.get('terms', [])
                        for term in terms:
                            start_date_str = term.get('startDateTime', '')
                            end_date_str = term.get('endDateTime', '')
                            try:
                                start_date = datetime.datetime.fromisoformat(start_date_str[:-1])
                                end_date = datetime.datetime.fromisoformat(end_date_str[:-1])
                                if start_date <= current_date <= end_date:
                                    active_items.append((title, start_date, end_date))
                                    break  # once the items are found we use break to term the function
                            except ValueError as e:
                                self.logger.error(f"Error parsing date for title '{title}': {e}")
                                continue   # using continue to skip if date parsing fails
        
        return active_items

    def get_level3_hd_manifest_paths(self):
        """
        Extracts Level3 HD manifest paths for all TV shows / movies that are currently within the start and end dates.
        
        Returns:
        - list: List of Level3 HD manifest paths for currently active TV shows / movies.
        """
        current_date = datetime.datetime.now()
        manifest_paths = []

        for entry in self.vq_data.get('results', []):
            rights = entry.get('rights', {})
            terms = rights.get('terms', [])
            for term in terms:
                start_date_str = term.get('startDateTime', '')
                end_date_str = term.get('endDateTime', '')
                try:
                    start_date = datetime.datetime.fromisoformat(start_date_str[:-1])
                    end_date = datetime.datetime.fromisoformat(end_date_str[:-1])
                    if start_date <= current_date <= end_date:
                        assets = [asset for asset in self.tq_data.get('results', []) if asset['contentId'] == entry['contentId']]
                        for asset in assets:
                            for endpoint in asset.get('assets', []):
                                if endpoint.get('videoFormat') == 'HD' and 'level3' in endpoint.get('endpoints', [{}])[0].get('origin', ''):
                                    manifest_paths.append(endpoint.get('endpoints', [{}])[0].get('path', ''))
                        break  # once the items are found we use break to term the function
                except ValueError as e:
                    self.logger.error(f"Error parsing date for entry '{entry.get('contentId', '')}': {e}")
                    continue  # using continue to skip if date parsing fails

        return manifest_paths
