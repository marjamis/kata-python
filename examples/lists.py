import helpers.formatting as formatting

LIST_DATA = [
  'testing',
  'the',
  'abilities',
  'of',
  'lists',
  'testing',
]

def loops():
  print('Loop through a list')
  for i in LIST_DATA:
    print(i)

def access_elements():
  print('Get first and second element of the list')
  print(f'first_element {LIST_DATA[0]} and second_element {LIST_DATA[1]}')

  print('Get second_last and last element of the list')
  print(f'second_last {LIST_DATA[-2]} and last {LIST_DATA[-1]}')

def alter_elements():
  # Note: the copy() is used to ensure a complete copy rather than a reference to the same underlying data that would happen from a: new_list_data = LIST_DATA. Python does a copy by reference for lists.
  new_list_data = LIST_DATA.copy()

  print('Printing the list')
  print(new_list_data)

  pos=2
  print(f"Insert element into position: {pos}")
  new_list_data.insert(pos, "ADDED")
  print(new_list_data)

  print(f"Deleting the element in position: {pos}")
  del(new_list_data[pos])
  print(new_list_data)

  print(f"Popping the last element")
  popped_element = new_list_data.pop()
  print(f"The element that was poped was {popped_element} and the list is now {new_list_data}")

  print(f"Popping the element in position: {pos}")
  popped_element = new_list_data.pop(pos)
  print(f"The element that was poped was {popped_element} and the list is now {new_list_data}")

  value='testing'
  print(f"Removing the first element with the value of: {value}")
  new_list_data.remove(value)
  print(f"The element that was poped was {value} and the list is now {new_list_data}")

  print(LIST_DATA)

def sorting():
  new_list_data = LIST_DATA.copy()

  new_list_data.sort()
  reverse_new_list_data = new_list_data.copy()
  reverse_new_list_data.reverse() # Or with: reverse_new_list_data.sort(reverse=True)
  print(f"list.sort() will change the lists ordering permanently in memory. Here is the new_list_data sorted: {new_list_data} and in reverse order: {reverse_new_list_data}")

  print(f"sorted() doesn't change the a lists ordering. Here is the existing LIST_DATA temporarily sorted for this run: {sorted(LIST_DATA)} and in reverse order: {sorted(LIST_DATA, reverse=True)}")

def ranges():
  print(f"Uses ranges to create a list of numbers, such as: {list(range(0, 10))}")
  print(f"The range function can also be provided a step-size, such as: {list(range(0, 10, 2))}")

def list_comprehensions():
  print(f'You can also make lists from functions easily with list comprehensions. Such as: {[i for i in range(1, 100, 8)]}')
  print(f'You can also have additional logic to make them more usable. Such as generating a list and then only adding items based off of a condition: {[i for i in range(1, 100, 8) if i % 10 == 7]}')

def slices():
  slice = LIST_DATA[1:-2]
  print(f'You can create slices of existing lists for references to sub-sections of a larger list. Such as: {slice}')

  slice[0] = 'new_something'
  print(f'When creating a slice of a list it does make a copy so the references will point to different values after a slice has been made. This is different to when assigning a list to a new variable, as that operation won\'t make a copy. Here is the slice after the change: {slice} and here is the LIST_DATA after the same change: {LIST_DATA}. Note: LIST_DATA hasn\'t been modified due to the implicit copy of values on the slices creation. A.k.a. A shallow copy.')

  print('You can also loop through a newly created slice.')
  for i in LIST_DATA[1:-2]:
    print(i)

def tuples():
  print(f'Like lists but the data can\'t be modified only overwritten with new values.')
  t = (7, 19, 20)
  for i in t:
    print(i)

  try:
    t[0] = 3 # Will fail
  except Exception as e:
    print(f'Can\'t modify an element of a tuple and instead get the exception: {e}.')

  t = (7, 19, 30, 12)
  for i in t:
    print(i)

def remove_keys():
  new_list_data = LIST_DATA.copy()
  remove_key='testing'

  print(f'Remove all keys with the value \'{remove_key}\' from the list. Note remove() only removes the first found, hence the loop. Initial list is: {new_list_data}.')
  while remove_key in new_list_data:
    new_list_data.remove(remove_key)
  print(f'Updated list is: {new_list_data}.')

def main():
  print(f"The test data named 'LIST_DATA' has a length of {len(LIST_DATA)}\n\n")

  runs = [
    {
      'Title': 'Loops',
      'FunctionName': loops,
    },
    {
      'Title': 'Accessing elements',
      'FunctionName': access_elements,
    },
    {
      'Title': 'Altering elements',
      'FunctionName': alter_elements,
    },
    {
      'Title': 'Sorting elements',
      'FunctionName': sorting,
    },
    {
      'Title': 'Ranges',
      'FunctionName': ranges,
    },
    {
      'Title': 'List Comprehensions',
      'FunctionName': list_comprehensions,
    },
    {
      'Title': 'Slices',
      'FunctionName': slices,
    },
    {
      'Title': 'Tuples',
      'FunctionName': tuples,
    },
    {
      'Title': 'Remove keys',
      'FunctionName': remove_keys,
    },
  ]

  formatting.wrapper(runs)

if __name__ == '__main__':
  main()
