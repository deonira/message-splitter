# Message Splitter

Message Splitter is a Python-based script that splits long HTML messages into smaller fragments based on a specified maximum length. This project helps in handling large HTML content and splitting it for further processing or communication.

## Features

- Split long HTML messages into smaller fragments based on a maximum length.
- Supports both command-line usage and unit testing.
- Easy to configure and extend.

## Installation

To get started with the project, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/deonira/message-splitter.git
2. Navigate to the project directory:
   ```
   cd message-splitter
3. Install the project dependencies using Poetry:
   ```
   poetry install
## Usage
Once the dependencies are installed, you can run the script to split HTML messages.
To use the script, run the following command:
```
poetry run python script_split_msg.py --max-len=4296 .\source.html
```
- ```--max-len=4296:``` The maximum length for each split message (you can adjust this value as needed).
- ```.\source.html:``` Path to the HTML file you want to split.
## Unit Testing
To run the unit tests for the project:
```
poetry run python -m unittest discover tests
```
This will discover and run all ```tests``` in the tests directory.
## Dependencies
- ```beautifulsoup4:```For parsing and handling HTML content.
- ```argparse:```For handling command-line arguments.
