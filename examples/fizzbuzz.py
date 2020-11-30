def response(i):
  v = str(i)
  if i % 15 == 0:
    v = 'fizz buzz'
  elif i % 3 == 0:
    v = 'fizz'
  elif i % 5 == 0:
    v = 'buzz'

  return v

for i in range(1, 101):
  print(f"{response(i)}")
