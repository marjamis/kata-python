class MyClass:
    """
    This is a custom class to showcase custom dunder/magic methods in Python.

    The "work" in these overrides are examples of operations you may want for your own object/classes.

    Note: This doesn't contain all dunder/magic methods, as it depends on the class/object in question,
    but has a good selection as an example.
    """

    custom_string = "This is a sample string"

    def __new__(cls, *args, **kwargs):
        print("Creating a new object of this class...")
        return super(MyClass, cls).__new__(cls)

    def __init__(self, name, lucky_numbers):
        print("Intialising the object that has been created...")
        self.name = name
        self.lucky_numbers = lucky_numbers

    def __del__(self):
        print("Deleting object...")

    def __str__(self):
        return f'Printing details of this class, such as a variable: {self.custom_string} for {self.name}'

    def __int__(self):
        total = 0
        for i in self.lucky_numbers:
            total += i

        return total

    def __bool__(self):
        return len(self.lucky_numbers) > 0

    def __eq__(self, other):
        return self.__int__() == other.__int__()

    def __lt__(self, other):
        return self.__int__() < other.__int__()

    def __gt__(self, other):
        return self.__int__() > other.__int__()

    def __le__(self, other):
        return self.__int__() <= other.__int__()

    def __ge__(self, other):
        return self.__int__() >= other.__int__()

    def __add__(self, other):
        self.lucky_numbers += other.lucky_numbers

        return self

    def __sub__(self, other):
        # Takes the list of lucky_numbers from other and if it's already in the list removes it from self
        for num in other.lucky_numbers:
            if num in self.lucky_numbers:
                self.lucky_numbers.remove(num)

        return self

    def __len__(self):
        return len(self.lucky_numbers)

    def __repr__(self) -> str:
        return f'Default representation: {super(MyClass, self).__repr__()}which is "wrapped"'

    def __contains__(self, value):
        return value in self.lucky_numbers


if __name__ == '__main__':
    my_lucky_number = 5
    bob = MyClass(name='Bob', lucky_numbers=[0, 1, 2, 3, 4])
    alice = MyClass(name='Alice', lucky_numbers=[4, 5, 6, 7, 8])

    print(bob)
    print(repr(bob))

    print()

    print(f'Does bob contain my lucky number? {5 in bob}')
    print(f'Does alice contain my lucky number? {5 in alice}')

    print()

    print(f'What is bobs int value? {bob.__int__()}')
    print(f'What is alices int value? {alice.__int__()}')

    print()

    print(f'Are bob and alice equal? {bob == alice}')
    print(f'Is alice greater than bob? {alice > bob}')

    print()

    print(f'Bobs size is: {len(bob)}')
    print(f'Alices size is: {len(alice)}')

    print()

    print(f'Alices numbers are: {alice.lucky_numbers}')
    alice -= bob
    print(f'Alices numbers after subtracting bobs are: {alice.lucky_numbers}')

    print()

    print(f'Alices numbers are: {alice.lucky_numbers}')
    alice += bob
    print(f'Alices numbers after adding bobs are: {alice.lucky_numbers}')

    # Note: This is last as it clears the array that used above. Remeber this is just for example purposes
    print()

    print(f'Is alice "true"? {alice.__bool__()}')
    alice.lucky_numbers = []
    print(f'How about now? {alice.__bool__()}')

    print()

    # Explicitly calling delete on bob but leaving the garbage collector to "collect" alice
    del bob
