import io
import os
import pathlib
import sys
from datetime import datetime
import argparse

from jinja2.ext import loopcontrols


def parse_arguments():
    """
    Parses command-line arguments for the racing report program.

    This function sets up and returns an argument parser with the following options:

    Arguments:
        --files (pathlib.Path):
            Specifies the path to the folder containing data files required for processing.
        --order (str):
            Specifies the sorting order for the report.
            Choices:
                - "asc": Sorts in ascending order (default).
                - "desc": Sorts in descending order.
        --driver (str):
            Filters the report to show statistics for a specific driver by name.

    Returns:
        argparse.ArgumentParser: The configured argument parser ready to parse input arguments.

    Example Usage:
        Command: python script.py --files ./data --order desc --driver "Fernando Alonso"
        Arguments parsed:
            files = './data'
            order = 'desc'
            driver = 'Fernando Alonso'

    Notes:
        - The `--files` argument is required to specify the folder containing the necessary files.
        - If `--order` is not provided, the report defaults to ascending order ("asc").
        - If `--driver` is not specified, no driver-specific filtering is applied.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_path", required=True, type=pathlib.Path, help="Path to the folder containing files.")
    parser.add_argument("--order", choices=["asc", "desc"], default="asc", help="Sorting order of drivers:"
                        " 'asc' for ascending, 'desc' for descending (default: asc)")
    parser.add_argument("--driver", type=str, help="Shows statistic about given driver.")

    return parser


def get_data(folder_path):
    """
    Reads all files in a specified folder and extracts their content.

    This function iterates through each file in the given folder, reads the content of each file,
    and stores the content as a list of stripped lines in a dictionary, where the keys are
    filenames and the values are lists of lines from the respective files.

    Parameters:
        folder_path (str): The path to the folder containing the files to be read.

    Returns:
        dict: A dictionary where keys are filenames and values are lists of stripped lines from the files.
    """
    files = {}

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        os.chmod(file_path, 0o444)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.readlines()
        except PermissionError:
            raise PermissionError(f"Permission denied: Please check file permission.")
        except FileNotFoundError:
            raise FileNotFoundError("Error: File not found")
        except IsADirectoryError:
            raise IsADirectoryError("Error: The provided path is a directory, not a file.")
        except io.UnsupportedOperation:
            raise io.UnsupportedOperation("Unsupported operation: File might be opened in the wrong mode.")
        except OSError as error:
            raise OSError (f"Error: {error}")
        else:
            content = [line.rstrip() for line in file_content]
            files[filename] = content

    return files


def get_files():
    """
    Parses command-line arguments to retrieve a folder path and returns the list of files
    within the specified folder.

    This function utilizes the `parse_arguments` function to define and parse
    command-line arguments. It expects the arguments to include a `folder_path`
    parameter that specifies the directory to retrieve files from. The files
    in the folder are fetched using the `get_data` function.

    Returns:
        dict: A dictionary where keys are filenames and values are lists of files content.
    """
    parser = parse_arguments()
    parser_arguments = parser.parse_args()
    folder_path = parser_arguments.folder_path
    files = get_data(folder_path)

    return files


def get_racer_time_info(file):
    """
    Parses race information from a list of race data strings and extracts racer abbreviations and times.

    This function processes each line in the provided object, extracting the first three
    characters as the racer's abbreviation and the subsequent characters (starting from the 14th index)
    as the racer's time.
    Each string in the input list is expected to have a fixed length of 26 characters.
    The extracted data is stored as a list of dictionaries.

    Args:
        file (list): A list os string containing the race participants information, where each item includes the
                        racer's abbreviation and time.
                        The list should not be empty, and each string must have a length of exactly 26 characters

    Returns:
        list[dict]: A list of dictionaries, where each dictionary has the following structure:
            - "abbrev" (str): The racer's abbreviation (first three characters of the item).
            - "time" (str): The racer's time (characters from the 14th index onward).
    """
    time_info = []
    required_data_len = 26

    if type(file) is not list or file == []:
        raise TypeError("This data should be a list and/or should not be empty.")
    else:
        for race_info in file:
            if len(race_info) != required_data_len:
                raise Exception(f"{race_info} does not have sufficient characters to extract the required data.")
            else:
                racer_initial = race_info[:3]
                time = race_info[14:]
                time_info.append({"abbrev":racer_initial, "time":time})

    return time_info


def get_racer_time_by_racer(racer_abbrev, file):
    """
    Retrieves the race time for a specific racer based on their abbreviation.

    This function iterates through race time information obtained from the `get_racer_time_info`
    function, searching for the entry that matches the given racer's abbreviation. When a match is
    found, it extracts and returns the racer's time.

    Args:
        racer_abbrev (str): The abbreviation of the racer whose time is to be retrieved.
        file (list): The file-like object list containing the racers information of abbreviation and its race time.

    Returns:
        str: The race time of the specified racer.

    Dependencies:
        - `get_racer_time_info(file)`: A function that parses the provided file and returns a list
          of dictionaries containing race time information, where each dictionary includes:
            - "abbrev": The racer's abbreviation.
            - "time": The corresponding race time.
    """
    for item in get_racer_time_info(file):
        if racer_abbrev in item["abbrev"]:
            racer_time = item["time"]
            return racer_time


def get_racers_profile(race_files):
    """
    Generates detailed profiles for racers by combining their abbreviations, names, teams,
    start times, and end times from multiple data sources.

    This function retrieves race files using `get_files()`, parses racer abbreviation data
    from the "abbreviations.txt" file, and enriches the profiles with additional information
    such as start and end times extracted from the "start.log" and "end.log" files.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a racer's profile
        with the following structure:
            - "abbrev" (str): The racer's abbreviation.
            - "profile" (list): A list containing:
                - Name (str): The racer's full name.
                - Team (str): The racer's team name.
                - Start time (str): The racer's start time from "start.log".
                - End time (str): The racer's end time from "end.log".

    Dependencies:
        - `get_files()`: Retrieves the race files required for processing.
        - `get_racer_time_by_racer()`: Extracts start and end times for racer by name abbreviation.

    """
    # race_files = get_files()
    profiles = []
    racers_abbrev_split = []

    if not "abbreviations.txt" or not "start.log" or not "end.log" in race_files.keys():
        raise KeyError("Files are missing.")
    else:
        for r_profile in race_files["abbreviations.txt"]:
            racers_abbrev_split.append(r_profile.split("_"))

        for racer in racers_abbrev_split:
            initial_abbrev = racer[0]
            name = racer[1]
            team = racer[-1]
            s_time = get_racer_time_by_racer(initial_abbrev, race_files["start.log"])
            e_time = get_racer_time_by_racer(initial_abbrev, race_files["end.log"])
            profile_info = {"abbrev":initial_abbrev, "profile":[name, team, s_time, e_time]}
            profiles.append(profile_info)

    return profiles


def calculate_race_time(start_time, end_time, time_format="%H:%M:%S.%f"):
    """
    Calculates the race time duration between a start time and an end time.

    This function computes the time difference between the given start and end times using
    the specified format. The result is returned as a string formatted as "MM:SS.mmm",
    where "mmm" represents the first three digits of microseconds.

    Args:
        start_time (str): The starting time of the race in the specified format.
        end_time (str): The ending time of the race in the specified format.
        time_format (str, optional): The format of the input times. Defaults to "%H:%M:%S.%f".

    Returns:
        str: The calculated race time as a formatted string "HH:MM:SS.mmm".
    """
    s_time = datetime.strptime(start_time, time_format)
    e_time = datetime.strptime(end_time, time_format)

    race_time = e_time - s_time

    total_seconds = race_time.total_seconds()
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    microseconds = race_time.microseconds
    sliced_microseconds = str(microseconds)[:3]
    result_race_time = f"{minutes:01}:{seconds:02}.{sliced_microseconds}"

    return result_race_time


def compute_racers_time(profile_list):
    """
    Computes the race times for a list of racer profiles and returns the results.

    This function processes a list of racer profiles, extracts relevant details (abbreviation,
    name, team, start time, and end time), and calculates the race time using the
    `calculate_race_time()` function. The results are returned as a list of dictionaries.

    Args:
        profile_list (list[dict]): A list of dictionaries where each dictionary represents
                                   a racer's profile with the following keys:
            - "abbrev" (str): The racer's abbreviation.
            - "profile" (list): A list containing:
                - Name (str): The racer's name.
                - Team (str): The racer's team.
                - Start time (str): The start time of the race.
                - End time (str): The end time of the race.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a racer's race result
        with the following structure:
            - "abbrev" (str): The racer's abbreviation.
            - "name" (str): The racer's name.
            - "team" (str): The racer's team.
            - "time" (str): The calculated race time in "HH:MM:SS.mmm" format.

    Dependencies:
        - `calculate_race_time()`: Computes the time difference between the start and end times.
    """
    list_of_race_result = []

    for dict_item in profile_list:
        if not "abbrev" or not "profile" in dict_item.keys():
            raise KeyError("Missing required data key 'abbreviation' or 'profile' from profile list.")
        else:
            racer_abbrev = dict_item["abbrev"]
            racer_name = dict_item["profile"][0]
            racer_team = dict_item["profile"][1]
            start_time = dict_item["profile"][2]
            end_time = dict_item["profile"][3]
            loop_time = calculate_race_time(start_time, end_time)
            racer_statistic = {"abbrev": racer_abbrev, "name": racer_name, "team": racer_team, "start_time":start_time,
                               "end_time": end_time, "loop_time": loop_time}
            list_of_race_result.append(racer_statistic)

    return list_of_race_result


def build_report(racers_data):
    """
    Builds a race report by sorting racer data based on their race times and formatting the results.

    This function sorts the provided racer data in ascending order of race times and formats
    the information into a ranked list. The report includes racer rank, name, team, and time.
    A separator line is added before the racer ranked 16th to distinguish the top 15 racers
    from the rest.

    Args:
        racers_data (list[dict]): A list of dictionaries where each dictionary contains the
                                  following keys:
            - "name" (str): The racer's name.
            - "team" (str): The racer's team name.
            - "time" (str): The racer's race time in "HH:MM:SS.mmm" format.

    Returns:
        list[str]: A formatted list of strings representing the race report. Each entry includes
                   the rank, racer's name, team, and race time, with a separator before the 16th rank.
    """
    report = []
    sorted_race_time = sorted(racers_data, key=lambda time: time["time"])
    underline_rank = 16

    for rank, racer in enumerate(sorted_race_time, start=1):
        if rank == underline_rank:
            report.append("---------------------------------------------------------------------------")
            report.append(f"{rank}. {racer['name']} | {racer['team']} | {racer['time']}")
        else:
            report.append(f"{rank}. {racer['name']} | {racer['team']} | {racer['time']}")

    return report


def build_statistic_report(racers_data):

    statistics_report = []
    sorted_race_time = sorted(racers_data, key=lambda time: time["loop_time"])
    underline_rank = 16

    for rank, racer in enumerate(sorted_race_time, start=1):
        if rank == underline_rank:
            statistics_report.append("---------------------------------------------------------------------------")
            statistics_report.append([rank, racer['name'], racer['abbrev'], racer['team'], racer['start_time'],
                                      racer['end_time'], racer['loop_time']])
            # statistics_report.append(f"{rank}. {racer['name']} | {racer['abbrev']} | {racer['team']} | {racer['start_time']} | "
            #                          f"{racer['end_time']} | {racer['loop_time']}")
        else:
            statistics_report.append([rank, racer['name'], racer['abbrev'], racer['team'], racer['start_time'],
                                      racer['end_time'], racer['loop_time']])
            # statistics_report.append(f"{rank}. {racer['name']} | {racer['team']} | {racer['abbrev']} | {racer['start_time']} | "
            #                          f"{racer['end_time']} | {racer['loop_time']}")
    return statistics_report


def generate_statistic_report(folder_path, order):
    """
    Generates a statistical report of racers based on data from the specified folder.

    This function retrieves input data from the given folder, processes racer profiles,
    computes statistical data related to their performance, and builds a report.
    The final report can be returned in ascending or descending order.

    Args:
        folder_path (str): The path to the folder containing input data files.
        order (str): The sorting order of the report. Accepts "asc" for ascending
                     order or any other value for descending order.

    Returns:
        list: A list containing statistical data about racers, sorted in the specified order.
    """
    input_data = get_data(folder_path)
    profiles = get_racers_profile(input_data)
    racers_statistic_data = compute_racers_time(profiles)
    statistics = build_statistic_report(racers_statistic_data)

    if order == "asc":
        return statistics
    else:
        return reversed(statistics)


def generate_report_data(folder_path, order):
    """
    Generates a report of racer participants based on data from the specified folder.

    This function retrieves input data from the given folder, processes racer profiles,
    computes their times, and builds a report. The final report can be returned in
    ascending or descending order.

    Args:
        folder_path (str): The path to the folder containing input data files.
        order (str): The sorting order of the report. Accepts "asc" for ascending
                     order or any other value for descending order.

    Returns:
        list: A list of racer participants sorted in the specified order.
    """

    input_data = get_data(folder_path)
    profiles = get_racers_profile(input_data)
    racers_data = compute_racers_time(profiles)
    racers_participants = build_report(racers_data)

    if order == "asc":
        return racers_participants
    else:
        return reversed(racers_participants)


def print_report():
    """
    Prints a formatted race report based on user-specified command-line arguments.

    This function generates racer profiles, computes their race times, and builds a
    sorted race report. It supports displaying the report in ascending or descending order
    of race times and allows filtering by a specific driver if specified in the
    command-line arguments.

    Workflow:
        1. Retrieves racer profiles using `get_racers_profile()`.
        2. Computes race times using `compute_racers_time()`.
        3. Builds a sorted race report using `build_report()`.
        4. Parses command-line arguments for order and driver filtering.
        5. Prints the report based on the specified order.
        6. If a driver is specified, prints detailed statistics for that driver.

    Command-line Arguments:
        - `order` (str): Specifies the order of the report. Acceptable values:
            - "asc": Print the report in ascending order of race times.
            - "desc": Print the report in descending order of race times.
        - `driver` (str): The name of a driver to filter and display detailed statistics.

    Dependencies:
        - `get_racers_profile()`: Fetches racer profiles.
        - `compute_racers_time()`: Calculates race times for each racer.
        - `build_report()`: Builds the formatted race report.
        - `parse_arguments()`: Parses command-line arguments.
    """
    race_files = get_files()
    profiles = get_racers_profile(race_files) #move ArgParser out
    racers_data = compute_racers_time(profiles)
    parser = parse_arguments()
    command_line_args = parser.parse_args()
    racers_participants = build_report(racers_data)
    racers_participants_in_desc_order = list(reversed(racers_participants))

    if command_line_args.order == "asc":
        for racer in racers_participants:
            print(racer)
    elif command_line_args.order == "desc":
        for racer in racers_participants_in_desc_order:
            print(racer)
    if command_line_args.driver:
        for profile in racers_participants:
            if command_line_args.driver in profile:
                print(f"\nFollow the Statistics about {command_line_args.driver}: \n\n{profile}\n")


if __name__ == '__main__':
    # print_report()
    # print(generate_report_data(folder_path="../../data", order="asc"))
    print(generate_statistic_report(folder_path="../../data", order = "asc"))
