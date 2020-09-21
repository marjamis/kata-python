class Employee():
  """The Employee class contains details of an employee."""
  def __init__(self, first_name, last_name, salary):
    self.first_name = first_name
    self.last_name = last_name
    self.salary = salary

  def give_raise(self, raise_in_dollars=5000) -> int:
    """Adds a raise to this instance of Employee. Either default $5000 or a custom amount."""
    self.salary += raise_in_dollars
    return self.salary
