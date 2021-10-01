#!/bin/bash python3.7

import random
from datetime import datetime, timedelta
from dataclasses import FrozenInstanceError, dataclass, field, replace


def random_date():
    """Generate a random date in the past with random days, minutes, and seconds."""
    return datetime.now() - timedelta(days=random.randint(0, 21), minutes=random.randint(0, 59), seconds=random.randint(0, 60))


@dataclass(order=True, frozen=True)
class Ticket:
    """Basic example of a dataclass trying to use some if it's inbuild abilities.

    More information can be found here: https://docs.python.org/3/library/dataclasses.html"""
    id: str = field(compare=False, repr=False)
    creation_date: datetime = field(compare=False, repr=False)
    age: int = 0
    plus_1_count: int = 0
    mylist: list = field(default_factory=list, compare=False, repr=False)

    def __post_init__(self):
        """Showing an example of how to modify attributes even in a frozen dataclass"""
        object.__setattr__(self, 'age', self._age(self.creation_date))

        # Randomly selects if the object should have a mylist value or not
        if random.randint(0, 1) == 1:
            object.__setattr__(
                self, 'mylist', [random.randint(1, 100) for _ in range(0, 5)])

    def __repr__(self):
        """Custom print string"""
        return f'Ticket: {self.id} - {self.age} days old with {self.plus_1_count} +1\'s. Is there a list? {self.mylist}'

    def _age(self, creation_date):
        """Calculates the age based on the creation date"""
        return (datetime.now() - creation_date).days


# Generate random data for sorting and the like
tickets = [Ticket(id=random.randint(1, 100), creation_date=random_date(), plus_1_count=random.randint(1, 40))
           for _ in range(10)]

print("\n## Using the dataclass' inbuilt ability to sort based on the object attributes that can be compared")
for ticket in sorted(tickets, reverse=True):
    print(ticket)

print("\n### Sorted by my custom search, as you can normally do, on plus_1_count")
for ticket in sorted(tickets, key=lambda ticket: (ticket.plus_1_count), reverse=True):
    print(ticket)

print("\n## Trying to modifying a frozen ticket object")
try:
    print(tickets[0].plus_1_count)
    tickets[0].plus_1_count += 1
    print(tickets[0].plus_1_count)
except FrozenInstanceError as e:
    print(f"Can't easily modify a frozen object from a dataclass: {e}")

print("\n## \"Modifying\" a frozen ticket object with the replace function")
try:
    print(tickets[0].plus_1_count)
    tickets[0] = replace(tickets[0], plus_1_count=tickets[0].plus_1_count+1)
    print(tickets[0].plus_1_count)
except FrozenInstanceError as e:
    print(
        f"This won't execute as when using frozen I'm creating a new copy and assigning it back tothe array with the modification: {e}")
