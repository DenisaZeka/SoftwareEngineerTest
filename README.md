# Sky GCD Software Engineer Test

This project fetches data from specific API endpoints, processes the data, and performs various tasks .

## Project Structure

The project directory is structured as follows:

- **src/**: Contains the main application code.
  - **api_interaction.py**: Handles API interactions, including fetching data with retries.
  - **data_processing.py**: Contains the logic for processing fetched data.
  - **main.py**: Orchestrates API fetching and data processing tasks.

- **tests/**: Contains unit tests for the application.
  - **test_api_interaction.py**: Unit tests for `api_interaction.py`.
  - **test_data_processing.py**: Unit tests for `data_processing.py`.

- **README.md**: Project documentation file.
  
## Usage
To get the data from Api's
Run the main script (`main.py`):

## Components

### `main.py`

The main script (`main.py`) orchestrates the following tasks:
- **Fetching Data**: Utilizes `APIDataFetcher` to fetch data from specific endpoints (`VQ_ENDPOINT` and `TQ_ENDPOINT`) with retries.
- **Data Processing**: Uses `DataProcessor` to process fetched data.
  - **Task 1**: Retrieves titles playable on a specified device platform ('ROKU').
  - **Task 2**: Filters currently active items from the previous list based on start and end dates.
  - **Task 3**: Retrieves Level3 HD manifest paths for currently active items.


### `data_processing.py`

The `DataProcessor` class in `data_processing.py` provides methods to:
- **`get_titles_for_device(device_platform)`**: Extracts titles playable on a specific device platform from fetched API data.
- **`filter_currently_active_items(titles_for_roku)`**: Filters currently active items based on start and end dates for titles playable on ROKU.
- **`get_level3_hd_manifest_paths()`**: Retrieves Level3 HD manifest paths for currently active TV shows/movies.


### `api_interaction.py`

The `APIDataFetcher` class in `api_interaction.py` handles API interactions:
- **`fetch_data(endpoint, max_retries)`**: Fetches data from a specified API endpoint using basic authentication (`USERNAME` and `PASSWORD`) with retry mechanism.

```bash
python src/main.py

## Testing
Unit tests are provided in tests/ using unittest framework:

test_api_interaction.py: Tests for APIDataFetcher.
test_data_processing.py: Tests for DataProcessor.

To run tests click on project terminal:

bash:
python -m unittest discover -s tests

And click enter 

## Dependencies

Ensure you have the following dependencies installed:

 `requests`: For making HTTP requests in `api_interaction.py`.

Make sure to have `requests` installed in your Python environment. You can install it using `pip`:

```bash
pip install requests
