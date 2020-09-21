# TODO convert tests to this class in the future?
class TestRun():
  """A class used for Tests to define what a test and in the future potentially how they're run."""
  def __init__(title: str, function_name: str, comment: str):
    self.title = title
    self.function_name = function_name
    self.comment = comment


def wrapper(runs):
  """A wrapper function to go through a list of tests to be run and formatted consistently."""
  for i in runs:
    print(f"### {i['Title']}")

    try:
      print(f"Comment: {i['Comment']}")
    except KeyError as e:
      pass
    except Exception as e:
      print(f"Unknown exception as occurred: {e}")

    i['FunctionName']()
    print('\n\n')
