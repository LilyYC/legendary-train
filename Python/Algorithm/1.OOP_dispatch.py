"""Exercise 1: Basic Object-Oriented Programming

- SuperDuperManager, which manages all the cars in the system
- Car, a class which represents a single car in the system

Your task is to design and implement the Car class, and then modify the
SuperDuperManager methods so that they make proper use of the Car class.

"""
from typing import Dict, Optional, Tuple


class SuperDuperManager:
    """A class that keeps track of all cars in the Super Duper system.
    """
    # === Private Attributes ===
    # _cars:
    #   A map of unique string identifiers to the corresponding Car.
    #   For example, _cars['car1'] would be a Car object corresponding to
    #   the id 'car1'.
    _cars: Dict[str, 'Car']

    def __init__(self) -> None:
        """Initialize a new SuperDuperManager.

        There are no cars in the system when first created.
        """
        self._cars = {}

    def add_car(self, id_: str, fuel: int) -> None:
        """Add a new car to the system.

        The new car is identified by the string <id_>, and has initial amount
        of fuel <fuel>.

        Do nothing if there is already a car with the given id.

        >>> m = SuperDuperManager()
        >>> m.add_car('Benz2', 5)
        >>> 'Benz2' in m._cars
        True
        """
        # Check to make sure the identifier isn't already used.
        if id_ not in self._cars:
            self._cars[id_] = Car(fuel)

    def move_car(self, id_: str, new_x: int, new_y: int) -> None:
        """Move the car with the given id.

        The car called <id_> should be moved to position (<new_x>, <new_y>).
        Do nothing if there is no car with the given id,
        or if the corresponding car does not have enough fuel.

        >>> m = SuperDuperManager()
        >>> m.add_car('Benz2', 5)
        >>> m.move_car('Benz2', 1, 3)
        >>> m._cars['Benz2'].x
        1
        >>> m._cars['Benz2'].y
        3
        >>> m._cars['Benz2'].fuel
        1
        """
        if id_ in self._cars:
            x_0, y_0 = self._cars[id_].x, self._cars[id_].y
            if abs(new_x - x_0) + abs(new_y - y_0) <= self._cars[id_].fuel:
                self._cars[id_].x = new_x
                self._cars[id_].y = new_y
                self._cars[id_].fuel -= abs(new_x - x_0) + abs(new_y - y_0)

    def get_car_position(self, id_: str) -> Optional[Tuple[int, int]]:
        """Return the position of the car with the given id.

        Return a tuple of the (x, y) position of the car with id <id_>.

        >>> m = SuperDuperManager()
        >>> m.add_car('Benz1', 10)
        >>> m.get_car_position('Benz1')
        (0, 0)
        >>> m.move_car('Benz1', 2, 5)
        >>> m.get_car_position('Benz1')
        (2, 5)
        """
        if id_ in self._cars:
            return (self._cars[id_].x, self._cars[id_].y)
        else:
            return None

    def get_car_fuel(self, id_: str) -> Optional[int]:
        """Return the amount of fuel of the car with the given id.

        Return None if there is no car with the given id.

        >>> m = SuperDuperManager()
        >>> m.add_car('Bmw2', 10)
        >>> m.get_car_fuel('Bmw1')

        >>> m.get_car_fuel('Bmw2')
        10
        """
        if id_ in self._cars:
            return self._cars[id_].fuel
        return None

    def dispatch(self, x: int, y: int) -> None:
        """Move a car to the given location.

        >>> m = SuperDuperManager()
        >>> m.add_car('a2', 7)
        >>> m.add_car('0s', 6)
        >>> m.add_car('b3', 13)
        >>> m.add_car('c1', 6)
        >>> m.move_car('b3', 1, 5)
        >>> m.move_car('0s', 3, 0)
        >>> m.move_car('c1', 0, 2)
        >>> m.dispatch(5, 2)
        >>> m.get_car_position('a2')
        (5, 2)
        >>> m.get_car_fuel('a2')
        0
        >>> m.get_car_position('b3')
        (1, 5)
        >>> m.get_car_position('c1')
        (0, 2)
        """

        distance = float('inf')
        id1 = []
        for car_id in self._cars:
            temp = abs(x - self._cars[car_id].x) + abs(y - self._cars[car_id].y)
            if temp < distance:
                distance = temp
                # Check if the fuel is enough
                if self._cars[car_id].fuel >= distance:
                    id1 = [car_id]
            elif temp == distance:
                id1.append(car_id)
        min_id = min(id1)
        self.move_car(min_id, x, y)


class Car:
    """A car in the Super system.

    === Public attributes ===
    x: the x-coordinate of this car's position
    y: the y-coordinate of this car's position
    fuel: the amount of fuel remaining this car has remaining

    === Representation invariants ===
    fuel >= 0
    """
    x: int
    y: int
    fuel: int

    def __init__(self, how_far_to_go: int) -> None:
        """Initialize a new Car.

        >>> c = Car(10)
        >>> c.fuel
        10
        >>> c.x
        0
        >>> c.y
        0
        """
        self.x = 0
        self.y = 0
        self.fuel = how_far_to_go

if __name__ == '__main__':
    # Run python_ta to ensure this module passes all checks for
    # code inconsistencies and forbidden Python features.
    # Useful for debugging!
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all()
