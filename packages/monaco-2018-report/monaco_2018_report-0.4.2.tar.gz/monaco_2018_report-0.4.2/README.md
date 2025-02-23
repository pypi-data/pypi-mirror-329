# Report of Monaco 2018 Racing

This project processes racing data to generate a detailed report of racer statistics, including race times, rankings,
and team information. It supports sorting results and filtering by specific drivers.


## Features

- **Command-line Interface:** Configure input folder, sorting order, and driver filtering.
- **Data Parsing:** Reads racer data from structured files (`abbreviations.txt`, `start.log`, `end.log`).
- **Time Calculations:** Computes race durations accurately from start and end timestamps.
- **Flexible Reporting:** Displays full rankings or filtered statistics for a single driver.


## Installation
Create and activate a virtual environment:

`virtualenv venv`

`venv/scripts/activate`


Install the package:

`python -m pip install monaco_2018_report`

Import the package:

` import monaco_2018_report`


## Usage
Run the script from the command line with the following options:

`python script.py --folder_path <path_to_data_folder> [--order <asc|desc>] [--driver <driver_name>]`

Arguments:
- --folder_path (required): Path to the folder containing abbreviations.txt, start.log, and end.log.
- --order (optional): Sorting order of the report.
  - Options:
      - asc (default): Ascending order of race times.
      - desc: Descending order of race times.
- --driver (optional): Filter and show statistics for a specific driver.


## Usage Exemple

`python script.py --folder_path ./data --order desc --driver "Fernando Alonso"`

## Output
- **Ranked Report:** Displays all racers, sorted by race time, with a separator distinguishing the top 15 racers.
- **Driver Statistics:** Shows details of a specific driver's performance if --driver is specified


## File Requirements
The input folder must contain:

- **abbreviations.txt:** Racer abbreviations, names, and team data.
- **start.log:** Start times for each racer.
- **end.log:** End times for each racer.


## Error Handling
- Ensures all required files are present.
- Validates input data formats.
- Provides informative error messages for missing or invalid arguments.

