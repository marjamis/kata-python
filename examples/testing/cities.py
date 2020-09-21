def city_country_to_string(city, country, population=None):
  str = f'{city.title()}, {country.title()}'
  if population is not None:
    str += f' - population {population}'
  return str
