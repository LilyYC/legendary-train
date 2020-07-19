"""A1 - Simulation

This file contains the Simulation class, which is the main class for your
bike-share simulation.

At the bottom of the file, there is a sample_simulation function that you
can use to try running the simulation at any time.
"""
import csv
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple

from bikeshare import Ride, Station
from container import PriorityQueue
from visualizer import Visualizer

# Datetime format to parse the ride data
DATETIME_FORMAT = '%Y-%m-%d %H:%M'


class Simulation:
    """Runs the core of the simulation through time.

    === Attributes ===
    all_rides:
        A list of all the rides in this simulation.
        Note that not all rides might be used, depending on the timeframe
        when the simulation is run.
    all_stations:
        A dictionary containing all the stations in this simulation.
    visualizer:
        A helper class for visualizing the simulation.
    active_rides:
        Keep track of the list of all rides that are in progress at the
        current time in the simulation.
    events_queue:
        Keep track of the event of specific rides in a priority queue.
    """
    all_stations: Dict[str, Station]
    all_rides: List[Ride]
    visualizer: Visualizer
    active_rides: List[Ride]
    events_queue: PriorityQueue['Event']

    def __init__(self, station_file: str, ride_file: str) -> None:
        """Initialize this simulation with the given configuration settings.
        """
        self.visualizer = Visualizer()
        self.all_stations = create_stations(station_file)
        self.all_rides = create_rides(ride_file, self.all_stations)
        self.active_rides = []
        self.events_queue = PriorityQueue()

    def run(self, start: datetime, end: datetime) -> None:
        """Run the simulation from <start> to <end>.
        """
        step = timedelta(minutes=1)  # Each iteration spans one minute of time
        current_time = start
        self._update_events_queue(current_time, end)
        while current_time <= end:
            l1 = list(self.all_stations.values())
            self._update_active_rides_fast(current_time)
            self._update_station(current_time)
            for stations in self.all_stations.values():
                stations.update_timer(current_time)
            l2 = self.active_rides
            l1.extend(l2)
            self.visualizer.render_drawables(l1, current_time)
            current_time += step
        # Leave this code at the very bottom of this method.
        # It will keep the visualization window open until you close
        # it by pressing the 'X'.
        while True:
            if self.visualizer.handle_window_events():
                return  # Stop the simulation

    def _update_events_queue(self, time: datetime, end: datetime) -> None:
        """ update events_queue by comparing ride start_time and end_time to
        simulation time period.
        """
        for ride in self.all_rides:
            if time <= ride.start_time <= end:
                ride_event = RideStartEvent(ride, ride.start_time, self)
                self.events_queue.add(ride_event)
            elif time <= ride.end_time <= end:
                self.events_queue.add(RideEndEvent(ride, ride.end_time, self))
                # add this ride to active_rides
                self.active_rides.append(ride)

    def _update_station(self, time: datetime) -> None:
        """ update stations information at current time. """
        for ride in self.active_rides:
            # if the ride start at current time during simulation
            if ride.start.num_bikes > 0 and ride.start_time == time:
                # update the start information at it's start station
                ride.start.update_start(time)
            if ride.end.capacity - ride.end.num_bikes > 0 \
                    and ride.end_time == time:
                ride.end.update_end(time)

    def _update_active_rides(self, time: datetime) -> None:
        """Update this simulation's list of active rides for the given time.

        REQUIRED IMPLEMENTATION NOTES:
        -   Loop through `self.all_rides` and compare each Ride's start and
            end times with <time>.

            If <time> is between the ride's start and end times (inclusive),
            then add the ride to self.active_rides if it isn't already in
            that list.

            Otherwise, remove the ride from self.active_rides if it is in
            that list.

        -   This means that if a ride started before the simulation's time
            period but ends during or after the simulation's time period,
            it should still be added to self.active_rides.

        """
        # need to remove it from active ride
        # when it endstation doesn't have enough bike upon its end time
        for ride in self.all_rides:
            if ride.start_time <= time <= ride.end_time:
                if ride not in self.active_rides:
                    self.active_rides.append(ride)
            else:
                if ride in self.active_rides:
                    self.active_rides.remove(ride)

    def _update_active_rides_fast(self, time: datetime) -> None:
        """Update this simulation's list of active rides for the given time.

        - Remove an event from the priority queue.

        - If the event’s time is after the current time, put the event back into
          the priority queue and return.

        - Otherwise,

        - process the event
        - add any new events generated into the priority queue.

        - Repeat by removing the next item from the priority queue.
        """
        while not self.events_queue.is_empty():
            event = self.events_queue.remove()
            if event.time > time:
                self.events_queue.add(event)
                return None
            else:
                next_events = event.process()
                for next_event in next_events:
                    self.events_queue.add(next_event)

    def calculate_statistics(self) -> Dict[str, Tuple[str, float]]:
        """Return a dictionary containing statistics for this simulation.

        The returned dictionary has exactly four keys, corresponding
        to the four statistics tracked for each station:
          - 'max_start'
          - 'max_end'
          - 'max_time_low_availability'
          - 'max_time_low_unoccupied'

        The corresponding value of each key is a tuple of two elements,
        where the first element is the name (NOT id) of the station that has
        the maximum value of the quantity specified by that key,
        and the second element is the value of that quantity.

        For example, the value corresponding to key 'max_start' should be the
        name of the station with the most number of rides started at that
        station, and the number of rides that started at that station.
        """
        max_start = 0
        potential_start = ''
        max_end = 0
        potential_end = ''
        time_low_avail = 0
        low_availability = ''
        time_low_unoccupied = 0
        low_unoccupied = ''
        for stations in list(self.all_stations.values()):
            if stations.num_start > max_start:
                max_start = stations.num_start
                potential_start = stations.name
            elif stations.num_start == max_start:
                if potential_start == '':
                    potential_start = stations.name
                elif stations.name < potential_start:
                    potential_start = stations.name

            if stations.num_end > max_end:
                max_end = stations.num_end
                potential_end = stations.name
            elif stations.num_end == max_end:
                if potential_end == '':
                    potential_end = stations.name
                elif stations.name < potential_end:
                    potential_end = stations.name

            if stations.low_bikes_total > time_low_avail:
                low_availability = stations.name
                time_low_avail = stations.low_bikes_total
            elif stations.low_bikes_total == time_low_avail:
                if low_availability == '':
                    low_availability = stations.name
                elif stations.name < low_availability:
                    low_availability = stations.name

            if stations.low_spots_total == time_low_unoccupied:
                if low_unoccupied == '':
                    low_unoccupied = stations.name
                elif stations.name < low_unoccupied:
                    low_unoccupied = stations.name
            elif stations.low_spots_total > time_low_unoccupied:
                low_unoccupied = stations.name
                time_low_unoccupied = stations.low_spots_total

        return {
            'max_start': (potential_start, max_start),
            'max_end': (potential_end, max_end),
            'max_time_low_availability': (low_availability,
                                          time_low_avail),
            'max_time_low_unoccupied': (low_unoccupied,
                                        time_low_unoccupied)
        }


def create_stations(stations_file: str) -> Dict[str, 'Station']:
    """Return the stations described in the given JSON data file.

    Each key in the returned dictionary is a station id,
    and each value is the corresponding Station object.
    Note that you need to call Station(...) to create these objects!

    Precondition: stations_file matches the format specified in the
                  assignment handout.

    This function should be called *before* _read_rides because the
    rides CSV file refers to station ids.
    """
    # Read in raw data using the json library.
    with open(stations_file) as file:
        raw_stations = json.load(file)
    stations = {}
    for s in raw_stations['stations']:
        stations[s['n']] = Station((float(s['lo']), float(s['la'])),
                                   int(s['ba']) + int(s['da']),
                                   int(s['da']), s['s'])
        # Extract the relevant fields from the raw station JSON.
        # s is a dictionary with the keys 'n', 's', 'la', 'lo', 'da', and 'ba'
        # as described in the assignment handout.
        # NOTE: all of the corresponding values are strings, and so you need
        # to convert some of them to numbers explicitly using int() or float().
    return stations


def create_rides(rides_file: str, stations: Dict[str, 'Station']) \
        -> List['Ride']:
    """Return the rides described in the given CSV file.

    Lookup the station ids contained in the rides file in <stations>
    to access the corresponding Station objects.

    Ignore any ride whose start or end station is not present in <stations>.

    Precondition: rides_file matches the format specified in the
                  assignment handout.
    """
    rides = []
    with open(rides_file) as file:
        # line is a list of strings
        for line in csv.reader(file):
            if line[1] and line[3] in stations:
                start = stations[line[1]]
                end = stations[line[3]]
                time = (datetime.strptime(line[0], DATETIME_FORMAT),
                        datetime.strptime(line[2], DATETIME_FORMAT))
                rides.append(Ride(start, end, time))
    return rides


class Event:
    """An event in the bike share simulation.

    Events are ordered by their timestamp.

    === Attributes ===
    simulation: 'Simulation'
        the simulation in which this event occurs.
    time: datetime
        the time when this event occurs.
    """
    simulation: 'Simulation'
    time: datetime

    def __init__(self, simulation: 'Simulation', time: datetime) -> None:
        """Initialize a new event."""
        self.simulation = simulation
        self.time = time

    def __lt__(self, other: 'Event') -> bool:
        """Return whether this event is less than <other>.

        Events are ordered by their timestamp.
        """
        return self.time < other.time

    def process(self) -> List['Event']:
        """Process this event by updating the state of the simulation.

        Return a list of new events spawned by this event.
        """
        raise NotImplementedError


class RideStartEvent(Event):
    """An event corresponding to the start of a ride.

    === Attributes ===
    start: 'Station'
        the station where this ride starts
    time: datetime
        the time the event ride start occurs
    num_bikes: int
        the bikes available at the event ride start
    ride: 'Ride'
    """
    def __init__(self, ride: 'Ride', time: datetime, simulation: Simulation):
        Event.__init__(self, simulation, time)
        self.ride = ride

    def process(self) -> List['Event']:
        """ Processing a “ride starting” event by adding a ride to the list of
             active rides and generating a “ride ending” event to happen
             at the appropriate time.
        """
        event_list = []
        self.simulation.active_rides.append(self.ride)
        self.ride.start.num_bikes -= 1
        self.ride.start.num_start += 1
        # generate a 'ride ending' event to happen at the appropriate time
        event_list.append(RideEndEvent(self.ride, self.ride.end_time, self.
                                       simulation))
        return event_list


class RideEndEvent(Event):
    """An event corresponding to the start of a ride.

    === Attributes ===
    end: 'Station'
        the station where this ride starts
    time: datetime
        the time the event ride start occurs
    ride: Ride
    """
    def __init__(self, ride: 'Ride', time: datetime, simulation: Simulation):
        Event.__init__(self, simulation, time)
        self.ride = ride
        self.time = time

    def process(self) -> List['Event']:
        """Processing a “ride starting” event by adding a ride to the
        list of active rides and generating a “ride ending” event to happen
        at the appropriate time.

        remove a ride from the list of active rides.
        It should not generate any additional events.
        """
        self.simulation.active_rides.remove(self.ride)
        self.ride.end.num_bikes += 1
        self.ride.end.num_end += 1
        return []


def sample_simulation() -> Dict[str, Tuple[str, float]]:
    """Run a sample simulation. For testing purposes only."""
    sim = Simulation('stations.json', 'sample_rides.csv')
    sim.run(datetime(2017, 6, 1, 8, 0, 0),
            datetime(2017, 6, 1, 12, 5, 0))
    return sim.calculate_statistics()

if __name__ == '__main__':
    # Uncomment these lines when you want to check your work using python_ta!
    # import python_ta
    # python_ta.check_all(config={
    #     'allowed-io': ['create_stations', 'create_rides'],
    #     'allowed-import-modules': [
    #         'doctest', 'python_ta', 'typing',
    #         'csv', 'datetime', 'json',
    #         'bikeshare', 'container', 'visualizer'
    #     ]
    # })
    print(sample_simulation())
