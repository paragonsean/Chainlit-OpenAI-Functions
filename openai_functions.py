import requests
import json
import logging
import pandas as pd
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIFunctions:

    @staticmethod
    def get_historical_temperature(latitude: float, longitude: float, start_date: str, end_date: str) -> str:
        """Fetch the historical temperature data for a given location and date range"""
        try:
            # Prepare API request
            url = "https://archive-api.open-meteo.com/v1/archive"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "start_date": start_date,
                "end_date": end_date,
                "daily": "temperature_2m_max,temperature_2m_min",
                "timezone": "auto"
            }
            response = requests.get(url, params=params)
            response.raise_for_status()

            # Parse the response data
            weather_data = response.json()
            temperature_data = weather_data.get("daily", {})
            return json.dumps({"temperature_data": temperature_data}, indent=4)
        except Exception as e:
            logger.error(f"Failed to fetch historical temperature data: {e}")
            return json.dumps({"error": "Error in retrieving historical temperature data."}, indent=4)

    @staticmethod
    def get_price_trends(index: str, start_date: str, end_date: str) -> str:
        """Fetch stock price trends for a given index and date range"""
        try:
            # Load the cleaned stock market data
            data = pd.read_csv('/mnt/data/Cleaned_Stock_Market_Dataset.csv', parse_dates=["Date"])

            # Parse the start and end dates
            start_date_dt = pd.to_datetime(start_date, errors='coerce')
            end_date_dt = pd.to_datetime(end_date, errors='coerce')

            if start_date_dt is pd.NaT or end_date_dt is pd.NaT:
                return json.dumps({"error": "Invalid date format. Please use YYYY-MM-DD."}, indent=4)

            # Filter data between the specified start and end dates
            data_filtered = data[(data["Date"] >= start_date_dt) & (data["Date"] <= end_date_dt)]

            if data_filtered.empty:
                return json.dumps({"error": "No data available for the specified date range."}, indent=4)

            # Sort data by date to get a clean trend
            data_filtered = data_filtered.sort_values(by="Date")

            # Extract the date and the specific price trend
            trend_data = data_filtered[["Date", index]]

            # Convert to JSON format for easy trend visualization
            return trend_data.to_json(orient="records", date_format="iso", indent=4)

        except Exception as e:
            logger.error(f"Failed to retrieve price trends for index '{index}': {e}")
            return json.dumps({"error": "Error in retrieving price trends."}, indent=4)

    @staticmethod
    def get_stock_market_data(index, start_date=None, end_date=None):
        """Retrieve stock market data for a given index and optional date range"""
        available_indices = [
            "Natural_Gas_Price", "Natural_Gas_Vol.", "Crude_oil_Price", "Crude_oil_Vol.",
            "Copper_Price", "Copper_Vol.", "Bitcoin_Price", "Bitcoin_Vol.", "Platinum_Price", 
            "Platinum_Vol.", "Ethereum_Price", "Ethereum_Vol.", "S&P_500_Price", "Nasdaq_100_Price",
            "Nasdaq_100_Vol.", "Apple_Price", "Apple_Vol.", "Tesla_Price", "Tesla_Vol.", 
            "Microsoft_Price", "Microsoft_Vol.", "Silver_Price", "Silver_Vol.", "Google_Price", 
            "Google_Vol.", "Nvidia_Price", "Nvidia_Vol.", "Berkshire_Price", "Berkshire_Vol.", 
            "Netflix_Price", "Netflix_Vol.", "Amazon_Price", "Amazon_Vol.", "Meta_Price", 
            "Meta_Vol.", "Gold_Price", "Gold_Vol."
        ]

        if index not in available_indices:
            logger.warning(f"Invalid index provided: {index}")
            return json.dumps({"error": f"Invalid index. Please choose from available indices: {', '.join(available_indices)}"}, indent=4)

        try:
            # Load the cleaned stock market data
            data = pd.read_csv('/mnt/data/Cleaned_Stock_Market_Dataset.csv', parse_dates=["Date"])

            # Convert start_date and end_date to datetime objects if provided
            if start_date:
                start_date_dt = pd.to_datetime(start_date, errors='coerce')
            if end_date:
                end_date_dt = pd.to_datetime(end_date, errors='coerce')

            # Validate that dates are properly parsed
            if start_date and (start_date_dt is pd.NaT or end_date_dt is pd.NaT):
                return json.dumps({"error": "Invalid date format. Please use YYYY-MM-DD."}, indent=4)

            # Filter data for the given index and optional date range
            if start_date and end_date:
                mask = (data["Date"] >= start_date_dt) & (data["Date"] <= end_date_dt)
                data_filtered = data.loc[mask, ["Date", index]]
            else:
                data_filtered = data[["Date", index]]

            # Check if the filtered data is empty
            if data_filtered.empty:
                return json.dumps({"error": f"No data available for index '{index}' in the given date range."}, indent=4)

            # Convert the DataFrame into a dictionary (Date as key, index values as values)
            data_filtered["Date"] = data_filtered["Date"].dt.strftime('%Y-%m-%d')
            data_dict = data_filtered.set_index("Date")[index].to_dict()

            return json.dumps(data_dict, indent=4)

        except Exception as e:
            logger.error(f"Failed to retrieve stock data for index '{index}': {e}")
            return json.dumps({"error": f"Error in retrieving stock data."}, indent=4)

# Map function names to methods in OpenAIFunctions
FUNCTIONS_MAPPING = {
    "get_historical_temperature": OpenAIFunctions.get_historical_temperature,
    "get_price_trends": OpenAIFunctions.get_price_trends,
    "get_stock_market_data": OpenAIFunctions.get_stock_market_data,
    "get_current_weather": OpenAIFunctions.get_current_weather,  # Assuming this method exists
}
