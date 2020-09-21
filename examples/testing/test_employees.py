import unittest
import employee

class EmployeeTestCase(unittest.TestCase):
  """A testing suite for the Employee class."""
  def setUp(self):
    """Generic setup to be used with each test."""
    self.employee = employee.Employee(first_name='John', last_name='Doe', salary=70_000)

  def test_give_default_raise(self):
    """This tests the default pay rise of $5,000 being added to a salary."""
    self.assertEqual((70_000 + 5_000), self.employee.give_raise())

  def test_give_custom_raise(self):
    """This tests adding a custom amount to the pay rise and ensures the correct end result."""
    custom_increase = 17_500
    self.assertEqual((70_000 + custom_increase), self.employee.give_raise(custom_increase))

if __name__ == '__main__':
  unittest.main()
