import datetime

"""
Inspiration from: https://www.freecodecamp.org/news/python-decorators-explained-with-examples/
"""


class CallCount:
    """This is a sample decorator class.
    It creates a generally used class for the deorator, i.e. shared variables,
    and explicitly runs __call__ for the decorator action."""

    def __init__(self, func, limit=1):
        self.func = func
        self.count = 0
        self.limit = limit

    def __call__(self, *args, **kwargs):
        """The function that will be used when the decorator is called on a function execution."""

        # Checks if the current count is smaller than the class defined limit.
        # If it is it will execute the wrapped function
        if self.count < self.limit:
            self.count += 1
            return self.func(*args, **kwargs)
        # If the limit is reached the function being wrapped isn't called and instead this custom code is executed
        else:
            print(f'No queries left. All {self.count} queries used.')
            return False


def my_decorator_func(content=None):
    """This is a sample decorator function.
    This can wrap any function as desired for the below test functionality.
    In this case it's a couple of levels of functions being executed and returned creating an execution chain."""

    def decorator(func):
        """This is the decorator function that will execute the inputed function."""

        def wrapper_func(*args, **kwargs):
            """This is the wrapper function which performs custom steps as well as executed the decorated function."""

            print("Before executing the decorated function")
            start = datetime.datetime.now()
            kwargs['content'] = content

            print("Executing the decorating function")
            func(*args, **kwargs)

            delta = datetime.datetime.now() - start
            print(f"After executing the decorated function. The time delta is: {delta}")

        return wrapper_func

    return decorator


@my_decorator_func(content="hello")
def test_function_decorator(content=None):
    """A basic function that will use the function decorator."""
    print("I'm the actual function running...")

    # If content is available, which currently due to the decorator it will be, prints out this content
    if content:
        print(f"The updated contents is: {content}")


@CallCount
def test_class_decorator() -> bool:
    """A basic function that will use the CallCount decorator class."""
    # Logic of this function
    print("Basic print test")

    # Returns true for the loop of continue or not
    return True


if __name__ == '__main__':
    # Test the function decorator method and configuration
    print("## Test Function Decorator\n")
    test_function_decorator()

    # Cycles until the limit is hit using the class decorator method
    print("\n\n## Test Class Decorator\n")
    success = True
    while success:
        success = test_class_decorator()
