
# Version 1 README

## Overview

This version of the software provides tools for tracking cryptocurrency trades and funding rates via the Binance WebSocket API. It consists of several Python scripts designed to run asynchronously, capturing and logging real-time data for various cryptocurrencies.

## Included Files

### `recent_trades.py`

This script monitors live trade data for specified cryptocurrency symbols using Binance's WebSocket service. It filters and logs trades based on size, and saves them to a CSV file. Features include:
- Connection to WebSocket streams for each cryptocurrency.
- Parsing of incoming JSON messages and conversion to human-readable formats.
- Conditional logging based on the USD size of the trades.

### `huge_trades.py`

Focused on capturing and aggregating large trades, this script logs trades over a specified size threshold and outputs the aggregated data periodically. It also saves this data to a CSV file. Key functionalities include:
- Aggregation of trade data into buckets to capture high-value trades.
- Asynchronous writing to a CSV file using `aiofiles` for efficient I/O operations.
- Real-time display of aggregated trades with conditional formatting based on trade characteristics.

### `funding.py`

Tracks and logs funding rates for cryptocurrencies from Binance's WebSocket API. It calculates and logs both the immediate and annualized funding rates. Features include:
- Asynchronous connection to WebSocket streams for fetching funding data.
- Periodic display of funding rates with color-coded output based on the rate's value.
- Efficient error handling and reconnection for continuous data retrieval.

## Additional Files

### `binance_trades.csv`

Contains logged data from `recent_trades.py`, formatted as:
- Event Time, Symbol, Aggregate Trade ID, Price, Quantity, First Trade ID, Trade Time, Is Buyer Maker

### `binance_huge_trades.csv`

Contains aggregated trade data from `huge_trades.py`, formatted as:
- Event Time, Symbol, Trade Value in USD, Trade Type

### `binance_funding.csv`

Contains funding rate data from `funding.py`, formatted as:
- Event Time, Symbol, Funding Rate, Yearly Funding Rate

## Usage

To run any of the scripts, ensure Python 3.7 or higher is installed along with the necessary libraries: `asyncio`, `json`, `os`, `datetime`, `pytz`, `websockets`, `termcolor`, `aiofiles`, and `csv`. Start the script using:
```bash
python <script_name>.py
```

## Dependencies

- Python 3.7+
- `asyncio`, `json`, `os`, `datetime`, `pytz`, `websockets`, `termcolor`, `aiofiles`, `csv`

Ensure all dependencies are installed using:
```bash
pip install asyncio json os datetime pytz websockets termcolor aiofiles csv
```

Note: Some dependencies might already be part of your Python installation.
