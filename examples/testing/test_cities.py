import unittest
import cities

class CitiesTestCase(unittest.TestCase):
  """Tests for the functions of cities"""
  def test_city_country_to_string(self):
    """Tests to ensure the accuracy of the city_country_to_string function with different types of data."""
    tests = [
      {
        'city': 'Santiago',
        'country': 'Chile',
        'expected': 'Santiago, Chile',
      },
      {
        'city': 'melbourne',
        'country': 'australia',
        'expected': 'Melbourne, Australia',
      },
      {
        'city': 'sydnEy',
        'country': 'australia',
        'population': 3_000_000,
        'expected': 'Sydney, Australia - population 3000000',
      }
    ]

    # Loops through each of the above tests
    for test in tests:
      # Assigns the required data to the context
      context={
        'city': test['city'],
        'country': test['country'],
      }
      # Only assigns the population to the context if provided
      if 'population' in test:
        context['population'] = test['population']

      # Using subTest() as they're so similar tests to be in the same method. Added benefit all of these tests will be run indepedent of failures meaning better failure data.
      with self.subTest(context=context):
        # **context will end up sending the multiple components to the city_country_to_string function and is useful for somethings that may not be available, such as the population.
        self.assertEqual(cities.city_country_to_string(**context), test['expected'])

if __name__ == '__main__':
  unittest.main()
