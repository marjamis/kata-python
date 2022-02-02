number_of_loops = 3

stop_iteration_exception_string = f'There is a finite number of yields produced by the generator, in this case {number_of_loops} and will generate a StopIteration exception when exhausted.'
general_exception_string = "Unknown exception. Raising..."


def create_generator(value=number_of_loops):
    """
    Creates an example generator.

    A generator allows the execution of the function to be paused and continued to get the
    next value, such as in a loop, rather than the execution starting again.

    This is accomplished via yeild and the next() function.
    """
    for i in range(value):
        try:
            # Instead of using a return, which stops the execution of this function call, yield
            # will instead return the value but pause the function call to be continued with the
            # next() function
            yield i
        except Exception as e:
            print(f'Exception: {e}')
            raise e


def generator():
    """
    Example execution through a genertor using the next() function to get the next value in the create_generator loop
    """
    print('\n# Example using basic looping to get all generator values')

    gen = create_generator()

    print(f'There are other inbuilt method calls for a generator that aren\'t covered, as seen here:\n# {dir(gen)}\n\n')

    try:
        # Executes a loop of next() for one more than the number returnable values in
        # the generator to generate the StopIteration exception
        for i in range(number_of_loops + 1):
            # next() gets the next value from the generator
            print(next(gen))
    except StopIteration:
        print(stop_iteration_exception_string)
    except Exception as e:
        print(general_exception_string)
        raise e


def generator_with_throw():
    """
    Example excecution which tells the generator to generate an exception on usage. This is exception
    is caught by this functions exception handling when using the generator.
    """
    print('\n# Example using throw()')

    gen = create_generator()
    try:
        for i in range(number_of_loops):
            print(next(gen))
            # Tells the generator to throw this exception which will execute this functions own exception capturing
            gen.throw(TypeError, "non-standard")
    except StopIteration:
        print(stop_iteration_exception_string)
    except Exception:
        # This gets called as the generator throws an exception from the gen.throw() above
        print(general_exception_string)
        # Note: removed the raise to ensure continued execution of these examples


def generator_with_close():
    """
    Example execution which preemptively closes the generator after the first next()
    which results in the generator returning the StopIteration exception.
    """
    print('\n# Example using close()')

    gen = create_generator()
    try:
        for i in range(number_of_loops):
            print(next(gen))
            gen.close()
    except StopIteration:
        print(stop_iteration_exception_string)
    except Exception as e:
        print(general_exception_string)
        raise e


def echo(value=None):
    print("Execution starts when 'next()' is called for the first time.")
    try:
        while True:
            try:
                value = (yield value)
            except Exception as e:
                value = e
    finally:
        print("Don't forget to clean up when 'close()' is called.")


def example_from_documentation():
    """
    Taken from: https://docs.python.org/3.8/reference/expressions.html#generator.send
    """
    print('\n# Example from documentation')

    generator = echo(1)
    print(next(generator))
    print(next(generator))
    print(generator.send(2))
    generator.throw(TypeError, "spam")
    generator.close()


def main():
    generator()
    generator_with_throw()
    generator_with_close()
    example_from_documentation()


if __name__ == '__main__':
    main()
