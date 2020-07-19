“””Bike-share objects

This file contains the Station and Ride classes, which store the data for the
objects in this simulation.

There is also an abstract Drawable class that is the superclass for both
Station and Ride. It enables the simulation to visualize these objects in
a graphical window.
"""

from datetime import datetime
from typing import Tuple, Optional

# Sprite files
STATION_SPRITE = 'stationsprite.png'
RIDE_SPRITE = 'bikesprite.png'


class Drawable:
    """A base class for objects that the graphical renderer can be drawn.

    === Public Attributes ===
    sprite:
        The filename of the image to be drawn for this object.
    """
    sprite: str

    def __init__(self, sprite_file: str) -> None:
        """Initialize this drawable object with the given sprite file.
        """
        self.sprite = sprite_file

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (long, lat) position of this object at the given time.
        """
        raise NotImplementedError


class Station(Drawable):
    """A Bixi station.

    === Public Attributes ===
    capacity:
        the total number of bikes the station can store
    location:
        the location of the station in long/lat coordinates
        **UPDATED**: make sure the first coordinate is the longitude,
        and the second coordinate is the latitude.
    name:
        name of the station
    num_bikes:
        current number of bikes at the station
    num_start:
        current total number of bikes starting from the station
    num_end:
        current total number of bikes ending at the station
    timer_bike:
        A timer to record the time when low_availability situation appears
    timer_spot:
        A time to record the time when low_unoccupied situation appears
    low_spots_total:
        current total amount in seconds that the station spent with
        at most five unoccupied spots
    low_bikes_total:
        count the total amount of time in seconds that the station
        spent with at most five availabile bikes

    === Representation Invariants ===
    - 0 <= num_bikes <= capacity
    - 0 <= num_start
    - 0 <= num_end
    - 0 <= low_spots_total
    - 0 <= low_bikes_total
    """
    name: str
    location: Tuple[float, float]
    capacity: int
    num_bikes: int
    num_start: int
    num_end: int
    timer_bike: Optional[datetime]
    timer_spot: Optional[datetime]
    low_spots_total: int
    low_bikes_total: int

    def __init__(self, pos: Tuple[float, float], cap: int,
                 num_bikes: int, name: str) -> None:
        """Initialize a new station.

        Precondition: 0 <= num_bikes <= cap
        """
        Drawable.__init__(self, STATION_SPRITE)
        self.location = pos
        self.capacity = cap
        self.num_bikes = num_bikes
        self.name = name
        self.num_end = 0
        self.num_start = 0
        self.timer_bike = None
        self.timer_spot = None
        self.low_spots_total = 0
        self.low_bikes_total = 0

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (long, lat) position of this station for the given time.

        Note that the station's location does *not* change over time.
        The <time> parameter is included only because we should not change
        the header of an overridden method.
        """
        longitude = self.location[0]
        latitude = self.location[1]
        return (float(longitude), float(latitude))

    def update_timer(self, time: datetime) -> None:
        """ Update the timer_bike"""
        if self.num_bikes <= 5:
            if self.timer_bike is None:
                self.timer_bike = time
            else:
                self.low_bikes_total += (time - self.timer_bike).total_seconds()
                self.timer_bike = time
        if self.capacity - self.num_bikes <= 5:
            if self.timer_spot is None:
                self.timer_spot = time
            else:
                self.low_spots_total += (time - self.timer_spot).total_seconds()
                self.timer_spot = time

    def update_start(self, time: datetime) -> None:
        """ Update the start of a ride from the station at simulation time.

            Start timer for low_availability
            Record time when station has at most five bikes or
            at most five unoccupied spots
        """
        self.num_bikes -= 1
        self.num_start += 1

        # when the station has at most 5 bikes, and the timer is off
        if self.num_bikes <= 5 and self.timer_bike is None:
            # Record the time when low_availability situation appears
            self.timer_bike = time
        # if the station has more than 5 bikes
        if self.capacity - self.num_bikes > 5 and self.timer_spot is \
                not None:
            # record the time spent with this low_availability situation
            self.low_bikes_total += \
                (self.timer_spot - time).total_seconds()
            # Reset the timer
            self.timer_spot = None

    def update_end(self, time: datetime) -> None:
        """ Update the end of a ride at the station at simulation time.
            Increase the num_end by 1, and increase the num_bikes  by 1

            Start timer for low_unoccupied station, record time
            when station no longer have at most 5 unoccupied stpots or
            when number of bikes exceeds 5
        """
        self.num_end += 1
        self.num_bikes += 1

        # when the number of unoccupied spots is at most 5, and timer is off
        if self.capacity - self.num_bikes <= 5 and self.timer_spot is None:
            # record the time when the low_unoccupied situation appears
            self.timer_spot = time
        # when the number of bikes is more than 5 and the timer is on
        if self.num_bikes > 5 and self.timer_bike is not None:
            # record the time spent with this low_unoccupied situation
            self.low_spots_total += \
                (self.timer_bike - time).total_seconds()
            self.timer_bike = None


class Ride(Drawable):
    """A ride using a Bixi bike.

    === Attributes ===
    start:
        the station where this ride starts
    end:
        the station where this ride ends
    start_time:
        the time this ride starts
    end_time:
        the time this ride ends

    === Representation Invariants ===
    - start_time < end_time
    """
    start: Station
    end: Station
    start_time: datetime
    end_time: datetime

    def __init__(self, start: Station, end: Station,
                 times: Tuple[datetime, datetime]) -> None:
        """Initialize a ride object with the given start and end information.
        """
        Drawable.__init__(self, RIDE_SPRITE)
        self.start, self.end = start, end
        self.start_time, self.end_time = times[0], times[1]

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (long, lat) position of this ride for the given time.

        A ride travels in a straight line between its start and end stations
        at a constant speed.
        """
        x0, y0 = self.start.location[0], self.start.location[1]
        x1, y1 = self.end.location[0], self.end.location[1]
        t0, t1 = self.start_time, self.end_time
        if t0 <= time <= t1:
            total, travelled = t1 - t0, time - t0
            proportion = travelled.total_seconds() / total.total_seconds()
            longitude = x0 + (x1 - x0) * proportion
            latitude = y0 + (y1 - y0) * proportion
            return (float(longitude), float(latitude))
        elif t0 > time:
            return (x0, y0)
        elif t1 < time:
            return (x1, y1)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'datetime'
        ],
        'max-attributes': 15
    })
