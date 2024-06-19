import logging
from api_interaction import APIDataFetcher, USERNAME, PASSWORD
from data_processing import DataProcessor

VQ_ENDPOINT = "https://ko3vcqvszf.execute-api.eu-west-1.amazonaws.com/vq"
TQ_ENDPOINT = "https://ko3vcqvszf.execute-api.eu-west-1.amazonaws.com/tq"

def main():
    try:
        #API data fetcher with credentials username and password
        api_data_fetcher = APIDataFetcher(USERNAME, PASSWORD)

        # setting a logging level to ERROR to have debug and info messages
        logging.basicConfig(level=logging.ERROR)

        # Fetch data from endpoints with retries
        vq_data = api_data_fetcher.fetch_data(VQ_ENDPOINT)
        tq_data = api_data_fetcher.fetch_data(TQ_ENDPOINT)

        # Creating of a dataprocessor instance cause it serves to organize and work with the data fetched from both APIs
        processor = DataProcessor(vq_data, tq_data)



        # Task 1: Getting titles playable on ROKU
        titles_for_roku = processor.get_titles_for_device('ROKU')
        print("\nTitles playable on ROKU:")
        for title in titles_for_roku:
            print(title)
            print("")
        print("--------------------------------------")#using those just for aesthetic purpose ,so we can get an organized output



        # Task 2: Filter to find currently active items from the above result
        active_items = processor.filter_currently_active_items(titles_for_roku)
        print("\nCurrently active items:")
        for item in active_items:
            title, start_date, end_date = item
            print(f"Title: {title}")
            print(f"Start Date: {start_date}")
            print(f"End Date: {end_date}")
            print("")
        print("--------------------------------------")



        # Task 3: Getting level3 HD manifest paths for currently active items
        level3_hd_manifests = processor.get_level3_hd_manifest_paths()
        print("\nLevel3 HD Manifest Paths for currently active items:")
        for manifest in level3_hd_manifests:
            print(manifest)
            print("")
        print("--------------------------------------")




    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
