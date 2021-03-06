"""Inheritance
"""
from math import sqrt, ceil
import random          # used to generate random numbers
from typing import Dict, Optional, Tuple

##############################################################################
# Task 1: Cars and other vehicles
##############################################################################
class SuperDuperManager:
    """A class responsible for keeping track of all cars in the system.

    NOTE: Unlike last week, you should NO CHANGE FOR THIS CLASS
    Instead, look at how it's using the Vehicle interface and the initializers
    for the three required subclasses.
    """
    # === Private Attributes ===
    # _vehicles:
    #     A map of unique string identifiers to the corresponding vehicles.
    #     For example, _vehicles['car1'] would be a vehicle corresponding to
    #     the id_ 'car1'.
    _vehicles: Dict[str, 'Vehicle']

    def __init__(self) -> None:
        """Initialize a new SuperDuperManager.

        There are no vehicles in the system when first created.
        """
        self._vehicles = {}

    def add_vehicle(self, vehicle_type: str, id_: str, fuel: int) -> None:
        """Add a new vehicle to the system of the given type.

        The new vehicle is identified by the string <id_>,
        and has initial amount of fuel <fuel>.

        Do nothing if there is already a vehicle with the given id.

        Preconditions:
          - <vehicle_type> is one of 'Car', 'Helicopter', or
            'UnreliableMagicCarpet'.
          - fuel >= 0

        NOTE: you'll need to override the initializer for each of the three
        Vehicle subclasses in order to make them compatible with this method.
        That should be your first step (otherwise you won't be able to add
        any cars to this system).

        >>> m = SuperDuperManager()
        >>> m.add_vehicle('Car', 'myBmw', 5)
        >>> m.add_vehicle('UnreliableMagicCarpet', 'Carpet1', 0)
        >>> m.add_vehicle('Helicopter', 'h1', 10)
        >>> m.get_vehicle_fuel('h1')
        10
        >>> m.get_vehicle_fuel('Carpet1')
        0
        >>> m.get_vehicle_fuel('myBmw')
        5
        """
        # Check to make sure the identifier isn't already used.
        if id_ not in self._vehicles:
            if vehicle_type == 'Car':
                self._vehicles[id_] = Car(fuel)
            elif vehicle_type == 'Helicopter':
                self._vehicles[id_] = Helicopter(fuel)
            elif vehicle_type == 'UnreliableMagicCarpet':
                self._vehicles[id_] = UnreliableMagicCarpet(fuel)

    def move_vehicle(self, id_: str, new_x: int, new_y: int) -> None:
        """Move a vehicle with the given id.

        The vehicle called <id_> should be moved to position (<new_x>, <new_y>).
        Do nothing if there is no vehicle with the given id,
        or if the corresponding vehicle does not have enough fuel to move.

        >>> m = SuperDuperManager()
        >>> m.add_vehicle('Car', 'c1', 7)
        >>> m.add_vehicle('UnreliableMagicCarpet', 'Carpet1', 0)
        >>> m.add_vehicle('Helicopter', 'h1', 10)
        >>> m.move_vehicle('h1', 0, 1)
        >>> m.get_vehicle_fuel('h1')
        5
        >>> m.get_vehicle_position('h1')
        (0, 1)
        >>> m.move_vehicle('c1', 1, 4)
        >>> m.get_vehicle_fuel('c1')
        2
        >>> m.get_vehicle_position('c1')
        (1, 4)
        >>> m.move_vehicle('c1', 1, 1)
        >>> m.get_vehicle_fuel('c1')
        2
        >>> m.get_vehicle_position('c1')
        (1, 4)
        >>> m.move_vehicle('Carpet1', 2, 8)

        """
        if id_ in self._vehicles:
            self._vehicles[id_].move(new_x, new_y)

    def get_vehicle_position(self, id_: int) -> Optional[Tuple[int, int]]:
        """Return the position of the vehicle with the given id.

        Return a tuple of the (x, y) position of the vehicle.
        Return None if there is no vehicle with the given id.
        """
        if id_ in self._vehicles:
            return self._vehicles[id_].position

    def get_vehicle_fuel(self, id_: str) -> Optional[int]:
        """Return the amount of fuel of the vehicle with the given id.

        Return None if there is no vehicle with the given id.
        """
        if id_ in self._vehicles:
            return self._vehicles[id_].fuel


class Vehicle:
    """An interface for a vehicle in the Super Duper system.

    Note that this interface specifies *two* public attributes,
    and *two* public methods (the initializer is not considered public).

    Of the public methods, a default implementation is given for move,
    but not fuel_needed.

    It also defines a constructor that should be called by each of its
    subclasses.

    === Attributes ===
    position:
        The position of this vehicle.
    fuel:
        The amount of fuel remaining for this vehicle.

    === Representation invariants ===
    - fuel >= 0
    """
    position: Tuple[int, int]
    fuel: int

    def __init__(self, new_fuel: int, new_position: Tuple[int, int]) -> None:
        """Initialize a new Vehicle with the given fuel and position.

        Precondition: new_fuel >= 0
        """
        self.fuel = new_fuel
        self.position = new_position

    def fuel_needed(self, new_x: int, new_y: int) -> int:
        """Return how much fuel would be used to move to the given position.

        Note: the amount returned may be larger than self.fuel,
        indicating that this vehicle may not move to the given position.
        """
        raise NotImplementedError

    def move(self, new_x: int, new_y: int) -> None:
        """Move this vehicle to a new position.

        Do nothing if this vehicle does not have enough fuel to move
        to the specified position.
        """
        needed = self.fuel_needed(new_x, new_y)
        if needed <= self.fuel:
            self.position = (new_x, new_y)
            self.fuel -= needed


class Car(Vehicle):
    """A car in the Super Duper system.

    A car can only move vertically and horizontally, and uses
    one unit of fuel per unit distance travelled.

    === Public attributes ===
    position: the x, y-coordinate of this car's position
    fuel: the amount of fuel remaining this car has remaining

    === Representation invariants ===
    fuel >= 0
    """
    position: Tuple[int, int]
    fuel: int

    def __init__(self, fuel) -> None:
        """Initialize this car, originally start at (0, 0)

        >>> c = Car(5)
        >>> c.fuel
        5
        >>> c.position
        (0, 0)
        """
        Vehicle.__init__(self, fuel, (0, 0))

    def fuel_needed(self, new_x: int, new_y: int) -> int:
        """Return how much fuel would be used to move to the given position.

        Note: the amount returned may be larger than self.fuel,
        indicating that this vehicle may not move to the given position.

        >>> m = SuperDuperManager()
        >>> m.add_vehicle('Car', 'c1', 7)
        >>> m._vehicles['c1'].fuel_needed(3, 2)
        5
        >>> c = Car(7)
        >>> c.fuel_needed(4, 6)
        10
        """
        return abs(new_x - self.position[0]) + abs(new_y - self.position[1])


class Helicopter(Vehicle):
    """A helicopter. Can travel diagonally between points.

    === Public attributes ===
    position: the x, y-coordinate of this car's position
    fuel: the amount of fuel remaining this car has remaining

    === Representation invariants ===
    fuel >= 0
    """
    position: Tuple[int, int]
    fuel: int

    def __init__(self, fuel) -> None:
        """Initialize this helicopter, originally starts at (3, 5)

        >>> h = Helicopter(10)
        >>> h.fuel
        10
        >>> h.position
        (3, 5)
        """
        Vehicle.__init__(self, fuel, (3, 5))

    def fuel_needed(self, new_x: int, new_y: int) -> int:
        """Return how much fuel would be used to move to the given position.

        Note: the amount returned may be larger than self.fuel,
        indicating that this vehicle may not move to the given position.

        >>> h1 = Helicopter(7)
        >>> h1.fuel_needed(0, 1)
        5
        """
        d1, d2 = new_x - self.position[0], new_y - self.position[1]
        return int(ceil(sqrt(d1**2 + d2**2)))


class UnreliableMagicCarpet(Vehicle):
    """An unreliable magic carpet.

    Does not need to use fuel to travel, but ends up in a random position
    within two horizontal and two vertical units from the target destination.

    === Public attributes ===
    position: the x, y-coordinate of this car's position
    fuel: the amount of fuel remaining this car has remaining

    === Representation invariants ===
    fuel = 0
    """
    def __init__(self, fuel) -> None:
        """Initialize this car, originally start at a random point with x, y
        coordinate within -10 to 10.

        >>> umc = UnreliableMagicCarpet(10)
        >>> umc.fuel
        10
        >>> abs(umc.position[0]) <= 10
        True
        >>> abs(umc.position[1]) <= 10
        True
        """
        Vehicle.__init__(self, fuel, (random.randint(-10, 10),
                                   random.randint(-10, 10)))

    def fuel_needed(self, new_x: int, new_y: int) -> int:
        """Return how much fuel would be used to move to the given position.

        Note: the amount returned may be larger than self.fuel,
        indicating that this vehicle may not move to the given position.

        >>> umc = UnreliableMagicCarpet(10)
        >>> umc.fuel_needed(4, 6)
        0
        """
        return 0

    def move(self, new_x: int, new_y: int)-> None:
        """Move this vehicle to a new position.

        >>> umc = UnreliableMagicCarpet(2)
        >>> umc.move(5, 2)
        >>> umc.position <= (7, 4)
        True
        >>> umc.position >= (3, 0)
        True
        """
        x1 = new_x + random.randint(-2, 2)
        y1 = new_y + random.randint(-2, 2)
        self.position = (x1, y1)



if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Uncomment and run before final submission. This checks for style errors
    # in addition to code inconsistencies and forbidden Python features.
    # import python_ta
    # python_ta.check_all(config={
    #     'allowed-import-modules': [
    #         'doctest', 'python_ta', 'typing',
    #         'math', 'random', 'obfuscated_stack'
    #     ]
    # })
