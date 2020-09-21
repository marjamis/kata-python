import helpers.formatting as formatting

test_data='Here is some test data'
numeric_data=3.091

def fstrings():
  print(f"This is an fstring, it will replace the braced values for the relevant variable. For example: {test_data.upper()}. Numeric data: {numeric_data:.1f}")

def format_function_string():
  print('This is a formatted string similar to the fstring approach but a bit less easy to read. For example: {data}'.format(data=test_data.lower()))
  print('A different way to populate the string, purely based on {}. For example: {} and some numeric data: {:.1f}'.format("position", test_data.lower(), numeric_data))
  print('Yet another way to display data based on positon. For example: {1} and some numeric data: {0:.2f}'.format(numeric_data, test_data.upper()))

def numbers():
  print(f'To make numbers easier to read _\'s can be used in numbers in the code but wont be displayed, such as: {1_000_000}')

  numbers = list(range(3, 30, 4))
  print(f'Inbuilt functionality to find the min and/or max of a list of numbers, for example the list is {numbers} with a min of {min(numbers)} and a max of {max(numbers)}. They also all add up to: {sum(numbers)}. There are lots of these helper functions, so it\'s always worth checking the documentation first.')

def main():
  print('There are many formatting options for text, such as seen with the formatting of numeric_data above. Check documentation for more details.')
  print('\nMy preffered way for larger text formatting is the use of something like jinja2. Check my examples under: ../markdown_templates_j2.\n')

  runs = [
    {
      'Title': 'f strings',
      'FunctionName': fstrings,
      'Comment': 'Easier to read that .format() examples but only available in python 3.6 and above.',
    },
    {
      'Title': 'format() strings',
      'FunctionName': format_function_string,
      'Comment': 'Another way to format strings',
    },
    {
      'Title': 'Numbers',
      'FunctionName': numbers,
    }
  ]

  formatting.wrapper(runs)

if __name__ == '__main__':
  main()
