class Robot():
  def __init__(self, name, position, intelligence):
    self.name = name
    self.position = position
    self.intelligence = intelligence

  def get_intelligence() -> int:
    return self.intelligence

class T100(Robot):
  def __init__(self, name, position, intelligence, infiltration_mission_count):
    super().__init__(name=name, position=position, intelligence=intelligence)
    self.infiltration_mission_count = infiltration_mission_count

  def get_infiltration_missions_count(self) -> int:
    return self.infiltration_mission_count

class Maintenance(Robot):
  def __init__(self, name, position, intelligence, succesful_repair_count):
    super().__init__(name=name, position=position, intelligence=intelligence)
    self.succesful_repair_count = succesful_repair_count

  def get_succesful_repair_count(self) -> int:
    return self.succesful_repair_count

class Translator(Robot):
  def __init__(self, name, position, intelligence):
    super().__init__(name=name, position=position, intelligence=intelligence)

def main():
  robots = [
    T100('The Terminator', 'Earth', 320, 8),
    Maintenance('Bender', 'Earth', 150, 250),
    Translator('C-3PO', 'Tattooine', 210)
  ]

  for robot in robots:
    str = (f'{robot.name.title()} is located on {robot.position.title()} with the intelligence of {robot.intelligence}.')

    if type(robot) is T100:
      str += f' There were {robot.get_infiltration_missions_count()} infiltration missions.'
    elif type(robot) is Maintenance:
      str += f' There were {robot.get_succesful_repair_count()} succesful repairs.'

    print(str)

if __name__ == '__main__':
  main()
