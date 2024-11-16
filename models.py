"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str
import math
import datetime

class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
       
        self.designation = info.get("designation")
        self.name = info.get("name")
        self.diameter = float(info.get("diameter", float("nan")))
        self.hazardous = info.get("hazardous")
        self.approaches = []
       
    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name:
            return f"{self.designation} ({self.name})"
        return f"{self.designation}"


    def __str__(self):
    """Return `str(self)`."""
    
        hazardous_status = "is" if self.hazardous else "is not"
        if not math.isnan(self.diameter):
            return f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km and {hazardous_status} potentially hazardous."
        return f"NEO {self.fullname}, {hazardous_status} potentially hazardous."

        

    def __repr__(self):
    """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
            f"diameter={self.diameter:.3f}, hazardous={self.hazardous})")

    
    def serialize(self) -> dict:
    """Return a dictionary representation of the object's attributes."""
        return {
            "Designation": self.designation,
            "Name": self.name,
            "Diameter_km": self.diameter,
            "Potentially_hazardous": self.hazardous,
        }



class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
   
    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """


        self._designation = info.get("designation")

        # Check validity of time
        self.time = info.get("time")
        if self.time:
            try:
                # Convert 'time' to datetime
                self.time = cd_to_datetime(self.time)
                # Ensure that 'time' is a datetime object
                if not isinstance(self.time, datetime.datetime):
                    raise ValueError(f"Invalid 'time' value: Expected datetime, got {type(self.time)}")
            except Exception as e:
                # Handle any conversion issues
                raise ValueError(f"Failed to convert 'time' to datetime: {e}")

        # assign 'distance' and 'velocity' to default values and validation
        self.distance = info.get("distance", math.nan)
        self.velocity = info.get("velocity", math.nan)

        if not isinstance(self.distance, float):
            raise ValueError(f"Invalid 'distance' value: Expected float, got {type(self.distance)}")
        if not isinstance(self.velocity, float):
            raise ValueError(f"Invalid 'velocity' value: Expected float, got {type(self.velocity)}")

        # Handle 'neo' assignment, ensuring it's set to None if missing
        self.neo = info.get("neo", None)

        
        
        
    @property
    def designation(self):
        """Get designation.
        
        Returns:
            [str]: Returns self._designation
            
        """
        return self._designation

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_string(self.time) if self.time else "Unknown time"


    def __str__(self):
    """Return a user-friendly string representation of the object."""
        return (f"At {self.time_str}, '{self.neo.fullname}' approaches Earth "
            f"at a distance of {self.distance:.2f} au and a velocity of "
            f"{self.velocity:.2f} km/s.")

    def __repr__(self):
    """Return a computer-readable string representation of the object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
            f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def serialize(self):
    """Return a dictionary representation of the object's attributes."""
        return {
            "Datetime_utc": datetime_to_str(self.time),
            "Distance_au": self.distance,
            "Velocity_km_s": self.velocity,
        }

        
