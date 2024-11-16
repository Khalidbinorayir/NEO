"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json
from pathlib import Path
from typing import List
from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path: Path) -> List[NearEarthObject]:
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos = []
    
     with open(neo_csv_path, mode='r', newline='') as csvfile:
         reader = csv.DictReader(csvfile)  # Read the CSV as a dictionary for each row
        
         for row in reader:
            # Extract relevant fields and create NearEarthObject instances
            designation = row['pdes']
            name = row['name']
            diameter = float(row['diameter']) if row['diameter'] else float('nan')  # Handle missing diameter
            hazardous = row['hazardous'] == 'Y'  # Assuming 'Y' means hazardous, 'N' means not hazardous
            
            # Create a NearEarthObject instance
            neo = NearEarthObject(designation, name, diameter, hazardous)
            neos.append(neo)
    return neos
   


def load_approaches(cad_json_path: Path) -> List[CloseApproach]:
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    
    approaches = []
    
    with open(cad_json_path, mode='r') as jsonfile:
        data = json.load(jsonfile)  # Parse the JSON file
        
        for approach_data in data:
            # Extract relevant fields and create CloseApproach instances
            designation = approach_data['designation']
            time = approach_data['time']  # Assuming time is already in a usable format (e.g., ISO string)
            distance = float(approach_data['distance'])  # Convert to float
            velocity = float(approach_data['velocity'])  # Convert to float
            
            # Create a CloseApproach instance
            approach = CloseApproach(designation, time, distance, velocity)
            approaches.append(approach)
    
    return approaches




