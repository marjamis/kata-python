print('Importing this module')

class TestingClass:

    def __init__(self, initial_test_value: int):
        self._test_value = initial_test_value

    def get_test_value(self) -> int:
        return self._test_value

    def get_test_value_times_by_three(self) -> int:
        return self._test_value * 3
