FUNCTIONS_SCHEMA = [
    {
        "name": "get_current_time",
        "description": "Get the current time in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location name. The pytz is used to get the timezone for that location.",
                }
            },
            "required": ["location"],
        },
    },
    {
        "name": "get_stock_market_data",
        "description": "Get the stock market data for a given index and optional date range",
        "parameters": {
            "type": "object",
            "properties": {
                "index": {
                    "type": "string",
                    "enum": [
                        "Natural_Gas_Price", "Natural_Gas_Vol.", "Crude_oil_Price", "Crude_oil_Vol.",
                        "Copper_Price", "Copper_Vol.", "Bitcoin_Price", "Bitcoin_Vol.", "Platinum_Price", 
                        "Platinum_Vol.", "Ethereum_Price", "Ethereum_Vol.", "S&P_500_Price", "Nasdaq_100_Price",
                        "Nasdaq_100_Vol.", "Apple_Price", "Apple_Vol.", "Tesla_Price", "Tesla_Vol.", 
                        "Microsoft_Price", "Microsoft_Vol.", "Silver_Price", "Silver_Vol.", "Google_Price", 
                        "Google_Vol.", "Nvidia_Price", "Nvidia_Vol.", "Berkshire_Price", "Berkshire_Vol.", 
                        "Netflix_Price", "Netflix_Vol.", "Amazon_Price", "Amazon_Vol.", "Meta_Price", 
                        "Meta_Vol.", "Gold_Price", "Gold_Vol."
                    ],
                },
                "start_date": {
                    "type": "string",
                    "description": "The start date for the data (in YYYY-MM-DD format). Optional.",
                },
                "end_date": {
                    "type": "string",
                    "description": "The end date for the data (in YYYY-MM-DD format). Optional.",
                }
            },
            "required": ["index"],
        },
    },


    {
        "name": "get_historical_temperature",
        "description": "Fetches the historical temperature data for a given location and date range.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {
                    "type": "number",
                    "description": "The latitude of the location."
                },
                "longitude": {
                    "type": "number",
                    "description": "The longitude of the location."
                },
                "start_date": {
                    "type": "string",
                    "description": "The start date for the historical data (in YYYY-MM-DD format)."
                },
                "end_date": {
                    "type": "string",
                    "description": "The end date for the historical data (in YYYY-MM-DD format)."
                }
            },
            "required": ["latitude", "longitude", "start_date", "end_date"]
        }
    }
]
