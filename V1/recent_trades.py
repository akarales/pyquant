# Import necessary libraries
import asyncio  # Asynchronous I/O operations
import json  # Parsing JSON data
import os  # Operating system interfaces
from datetime import datetime, timezone  # Handling dates and time zones
import zoneinfo  # Time zone data
from websockets import connect, WebSocketException  # WebSocket client and exception handling
from termcolor import cprint  # Colored terminal output
import csv  # CSV file manipulation

# List of cryptocurrency symbols to monitor
symbols = ['btcusdt', 'ethusdt', 'solusdt', 'bnbusdt', 'dogeusdt', 'wifusdt']
# Base URL for connecting to the WebSocket server
websocket_url_base = 'wss://fstream.binance.com/ws/'
# Filename for saving trade data
trades_filename = 'binance_trades.csv'

# Check if the CSV file already exists, create and write headers if it doesn't
if not os.path.isfile(trades_filename):
    with open(trades_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Event Time', 'Symbol', 'Aggregate Trade ID', 'Price', 'Quantity', 'First Trade ID', 'Trade Time', 'Is Buyer Maker'])

# Asynchronous function to connect to the WebSocket and process trades
async def binance_trade_stream(uri, symbol, filename):
    async with connect(uri) as websocket:  # Establish a WebSocket connection
        while True:  # Continuously receive messages
            try:
                message = await websocket.recv()  # Receive a message
                data = json.loads(message)  # Parse the JSON message
                # Convert trade timestamp to a specific timezone
                trade_time = datetime.fromtimestamp(data['T'] / 1000, zoneinfo.ZoneInfo('America/New_York'))
                readable_trade_time = trade_time.strftime('%H:%M:%S')  # Format the trade time
                usd_size = float(data['p']) * float(data['q'])  # Calculate the USD size of the trade

                # Log trades above $14999
                if usd_size > 14999:
                    trade_type = 'SELL' if data['m'] else "BUY"  # Determine trade type
                    color = 'red' if trade_type == 'SELL' else 'green'  # Color for output
                    attrs = ['bold'] if usd_size >= 50000 else []  # Bold attribute for large trades
                    cprint(f"{trade_type} {symbol.upper().replace('USDT', '')} {readable_trade_time} ${usd_size:,.0f}", 'white', f'on_{color}', attrs=attrs)
                    # Append trade data to the CSV file
                    with open(filename, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([datetime.now(timezone.utc).isoformat(), symbol.upper(), data['a'], data['p'], data['q'], data['T'], data['m']])

            except WebSocketException as e:  # Handle WebSocket exceptions
                print(f"WebSocket error for {symbol}: {str(e)} - retrying in 5 seconds.")
                await asyncio.sleep(5)  # Retry after a pause
            except json.JSONDecodeError as e:  # Handle JSON parsing errors
                print(f"JSON error for {symbol}: {str(e)} - continuing.")
                continue  # Continue to the next message

# Asynchronous main function to start all tasks
async def main():
    # Create a list of tasks for each symbol
    tasks = [binance_trade_stream(f"{websocket_url_base}{symbol}@aggTrade", symbol, trades_filename) for symbol in symbols]
    await asyncio.gather(*tasks)  # Execute all tasks concurrently

# Run the main function using asyncio
asyncio.run(main())
