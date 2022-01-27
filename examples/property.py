class PropertyFunctionTestClass:
    _my_number: int

    def __init__(self, number):
        self._my_number = number

    def _get_my_number(self):
        """Getter method for my_number. This is private as it shouldn't be called directly."""
        return self._my_number

    def _set_my_number(self, value):
        """Setter method for my_number. This is private as it shouldn't be called directly."""
        self._my_number = value

    def _del_my_number(self):
        """Delete method for my_number. This is private as it shouldn't be called directly."""
        # Currently nothing is required here...
        pass

    @property
    def my_number_doubled(self) -> int:
        """This decorator allows a method to act like an attribute."""
        return self._my_number * 2

    # Creates an "attribute" of number (there is also an _number that is auto added with these details)
    # with these accessing methods for reading,modifying, and deleting the number attribute
    number = property(
        fget=_get_my_number,
        fset=_set_my_number,
        fdel=_del_my_number,
        doc="My number property."
    )


class PropertyDecoratorTestClass:
    _my_number: int

    def __init__(self, number):
        self._my_number = number

    @property
    def number(self):
        """
        This number method is now a property which is used as the getter and is the basis of the
        following setter and deleter methods.
        """
        return self._my_number

    @number.setter
    def number(self, value):
        """
        Setter method for my_number, as defined by the decorator of the property name
        and the type of method it is.
        """
        self._my_number = value

    @number.deleter
    def number(self):
        """
        Deleter method for my_number, as defined by the decorator of the property name
        and the type of method it is.
        """
        # Currently nothing is required here...
        pass

    @property
    def my_number_doubled(self) -> int:
        """This decorator allows a method to act like an attribute."""
        return self._my_number * 2


def main():
    property_function = PropertyFunctionTestClass(8)
    print('Using the older property() function approach to define get and set methods...')
    print(f'Accessing the _my_number attribute directly, even though we shouldn\'t: {property_function._my_number}')
    print(f'Used like an attribute but really via the fget method: {property_function.number}')
    # Get the original number, times it by 11 and then set it
    # This will use both the fget and the fset method on the "number" attribute
    property_function.number *= 11
    print(f'Uses the fget method after using the fset method in the line above: {property_function.number}')
    print(f'Uses the decorator to treat as an attribute to return the number: {property_function.my_number_doubled}')
    print(f'Back to where we started with directly accessing the "private" attribute: {property_function._my_number}')

    print('\n\n')

    property_decorator = PropertyDecoratorTestClass(8)
    print('Using the new property decorator approach to define get and set methods...')
    print(f'Accessing the _my_number attribute directly, even though we shouldn\'t: {property_decorator._my_number}')
    print(f'Used like an attribute but really via the getter method: {property_decorator.number}')
    # Get the original number, times it by 11 and then set it
    # This will use both the getter and setter methods, as set by the decorators, on the "number" attribute
    property_decorator.number *= 11
    print(f'Uses the getter method after using the setter method in the line above: {property_decorator.number}')
    print(f'Uses the decorator to treat as an attribute to return the number: {property_decorator.my_number_doubled}')
    print(f'Back to where we started with directly accessing the "private" attribute: {property_decorator._my_number}')


if __name__ == '__main__':
    main()
