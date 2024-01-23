# CSE3502 SYSTEM TELEGRAM BOT

This is a Python script for a Telegram bot that provides system information and monitoring capabilities. The bot is designed to run on the Telegram platform and can be queried for various system-related information.

## Features

- Display system information such as uptime, CPU temperature, memory usage, disk space, network information, and CPU details.
- Continuous logging of system information at regular intervals.
- Retrieve information by sending specific commands to the bot.

## Requirements

- Python 3.x
- `telebot` library
- `psutil` library
- `pymongo` library
- A Telegram bot token

## Installation

1. Clone the repository:


2. Install the required Python libraries:

```bash 
pip install telebot psutil pymongo

```

3. Replace the placeholder TOKEN in the script with your actual Telegram bot token.

4. Ensure that MongoDB is installed and running on your machine. Update the MongoDB connection details if necessary.



### Usage

Run the script by executing the following command in your terminal:

```bash

python bot.py

```

## Commands

    /info: Display information about the bot.
    /uptime: Show the system uptime.
    /coretemp: Retrieve CPU core temperatures.
    /mem: Display memory usage information.
    /disk: Show disk space information.
    /ip: Retrieve network information.
    /cpu: Display CPU information.
    /startlog: Start continuous logging of system information.

## Logging

The script continuously logs system information to a MongoDB database. Different collections are used for logging different types of information, such as uptime, CPU temperature, memory info, disk info, IP info, and CPU info.
Dependencies

    Telebot: A Python wrapper for the Telegram Bot API.
    psutil: A cross-platform library for retrieving information on running processes and system utilization.
    pymongo: The official Python driver for MongoDB.

## License

This code is licensed under the MIT License. Feel free to modify and distribute it as needed.
