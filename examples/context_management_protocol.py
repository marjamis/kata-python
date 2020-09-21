from contextlib import contextmanager

class RequiredValueMissing(Exception):
  """Basic custom exception for when my Context Manager misses required data."""
  def __init__(self, message):
    self.message = message

class CustomContextManager:
  """Example of using the Context Management Protocol for code that requires openning and closing actions, such as files. They are intended to be used as more succinct mechanism for resource management than try ... finally constructs. It ensure to run the __enter__() on startup and __exit__() when the with code block is exited for any reason, including failures. Hence it's good for automatic clean up of details, such as closing files."""
  def __init__(self, name=None, custom_string=''):
    self.default_string = 'Default String'
    self.new_string = custom_string
    self.name = name

  def __enter__(self):
    """Automatically called when executing via the with directive. Often use to lock or open files."""
    print(f'Entering for {self.name}...')
    if self.name is None:
      raise RequiredValueMissing('There is a missing piece of data')
      return

    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    """Automatically called when the with directive code block ends even if there is an exception in the code. Often use to close files."""
    print(f'Exiting for {self.name}...')

  def readStrings(self):
    """Custom method within the context manager that can be called from an alias within the with code block."""
    if self.new_string != '':
      print(self.new_string)
      return

    print(self.default_string)

@contextmanager
def SimplifiedCustomContextManager(*args, **kwds):
  """A more basic implementation and setup of a context manager"""
  name = kwds['name']
  try:
    print(f"The __enter__() code for {name}.")
    simplified_read_strings(*args, **kwds)
    yield
  finally:
    print(f"The __exit__() code for {name}.")

def simplified_read_strings(*args, **kwds):
  """My custom function that my SimplifiedCustomContextManager calls as part of it's __enter__() code."""
  if 'custom_string' in kwds:
    if kwds['custom_string'] != '':
      print(kwds['custom_string'])
      return

  print("default_string")

def main():
  with CustomContextManager(name='new', custom_string='here I am') as t:
    t.readStrings()

  print()
  with CustomContextManager(name='new') as t:
    t.readStrings()

  print()
  with SimplifiedCustomContextManager(name='new2', custom_string='here I am again'):
    print("I'm here")

  print()
  with SimplifiedCustomContextManager(name='new2'):
    print("I'm here")

  print()
  # Using multiple ContextManagers in the same with statement. This will allow usage of both at the same time, possible useful to interact with each other.
  with CustomContextManager(name='new1', custom_string='here I am') as t, SimplifiedCustomContextManager(name='new2', custom_string='here I am again'):
      t.readStrings()

  print('This with cause an exception.')
  with CustomContextManager() as t:
    t.readStrings()

if __name__ == '__main__':
  main()
