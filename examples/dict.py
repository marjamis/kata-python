import helpers.formatting as formatting

DICT_DATA = {
  'key1': 'testing',
  'key3': 'abilities',
  'key4': 'of',
  'key2': 'the',
  'key5': 'dictionary',
  'key6': 'testing',
}

def loop():
  print('Loop through key/value pairs.')
  for k, v in DICT_DATA.items():
    print(f'Key is: {k} with the value of: {v}')

  print('Loop through the keys')
  for k in DICT_DATA.keys(): # Could also be: for k in DICT_DATA:
    print(k.title())

  print('Loop through the sorted keys')
  for k in sorted(DICT_DATA.keys()): # Could also be: for k in DICT_DATA:
    print(k.title())

  print('Loop through the values')
  for v in DICT_DATA.values():
    print(v.upper())

  print('Using set() to only display unique values') # Manual create a set with {'v1', 'v2', 'v3'}
  for v in set(DICT_DATA.values()):
    print(v.upper())

def check_key():
  if 'key1' in DICT_DATA: # Could also be: if 'key1' in DICT_DATA.keys():
    print('Key has been found.')

def get():
  print(DICT_DATA.get('key3', 'No key.'))
  print(DICT_DATA.get('no_such_key', 'No key.'))

  print(DICT_DATA['key3'])
  try:
    print(DICT_DATA['no_such_key'])
  except KeyError as e:
    print(f'There is was an error in getting this key. Hence the try/except with this method of getting a key. The KeyError exception was for the key: {e}')
  except Exception as e:
    pass

def main():
  runs = [
    {
      'Title': 'Loop',
      'FunctionName': loop,
    },
    {
      'Title': 'Get',
      'FunctionName': get,
    },
    {
      'Title': 'Check if key exists',
      'FunctionName': check_key,
    },
  ]

  formatting.wrapper(runs)

if __name__ == '__main__':
  main()
