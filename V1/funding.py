import asyncio
import json
import os
import aiofiles
import logging
from datetime import datetime
from websockets import connect
from termcolor import cprint

# Configure logging for error reporting only
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the list of trading symbols to monitor
symbols = ['btcusdt', 'ethusdt', 'solusdt', 'bnbusdt', 'dogeusdt', 'wifusdt']
websocket_url_base = 'wss://fstream.binance.com/ws/'  # Base URL for Binance websocket API
funding_filename = 'binance_funding.csv'  # File to store funding rate data

results = {}  # Dictionary to store the latest results for each symbol

async def setup_funding_file():
    # Check if the funding file exists, if not, create it and write the header
    if not os.path.isfile(funding_filename):
        async with aiofiles.open(funding_filename, 'w') as f:
            await f.write('Event Time, Symbol, Funding Rate, Yearly Funding Rate\n')

async def binance_funding_stream(uri, symbol):
    # Connect to Binance websocket and stream funding data
    async with connect(uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                funding_rate = float(data['r'])
                yearly_funding_rate = funding_rate * 3 * 365 * 100  # Convert to yearly percentage
                event_time = datetime.utcfromtimestamp(data['E'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
                symbol_display = symbol.upper().replace('USDT', '')
                results[symbol] = (event_time, symbol_display, funding_rate, yearly_funding_rate)
                
                # Append data to CSV file
                async with aiofiles.open(funding_filename, 'a') as f:
                    await f.write(f"{event_time}, {symbol_display}, {funding_rate:.4f}, {yearly_funding_rate:.2f}\n")

            except Exception as e:
                logging.error(f"Error in websocket stream for {symbol}: {e}")
                await asyncio.sleep(5)

async def display_results():
    while True:
        if results:  # Check if there are any results to display
            header_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            cprint(f"Yearly Fund - {header_time}", 'white', 'on_blue')
            for symbol, (time, symbol_display, rate, yearly_rate) in results.items():
                color, back_color = determine_color(yearly_rate)
                cprint(f"{symbol_display} funding: {yearly_rate:.2f}%", color, back_color)
        await asyncio.sleep(5)  # Update display every 10 seconds

def determine_color(yearly_rate):
    if yearly_rate > 50:
        return 'white', 'on_red'
    elif yearly_rate > 30:
        return 'white', 'on_yellow'
    elif yearly_rate > 5:
        return 'white', 'on_cyan'
    elif yearly_rate < -10:
        return 'white', 'on_green'
    else:
        return 'white', 'on_light_green'

async def main():
    await setup_funding_file()
    funding_stream_tasks = [binance_funding_stream(f"{websocket_url_base}{symbol}@markPrice", symbol) for symbol in symbols]
    display_task = display_results()  # Create a task for displaying results
    await asyncio.gather(*funding_stream_tasks, display_task)

if __name__ == "__main__":
    asyncio.run(main())
