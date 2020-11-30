import jinja2
import os
import sys

from jinja2 import Environment, FileSystemLoader
from test_data import TEST_CONTEXT

class TemplateNotFound(Exception):
  def __init__(self, message):
    self.message = message

class InvalidContext(Exception):
  def __init__(self, message):
    self.message = message

class TemplateEngine():
  TEMPLATE_MAPING = {
    "BASE": "base.md.j2",
    "NON_EXISTING": "base2.md.j2",
    "LINKS": "links.md.j2",
    "STATS": "stats.md.j2",
    'UPDATED_BASE': 'updated_base.md.j2',
    'TableFormatting': 'table_formatting.html.j2',
    'SLACK': 'tickets.slack.j2',
  }

  def __init__(self):
    self.templates_directory=os.getcwd()+"/templates/"
    self.env = Environment(
      loader=FileSystemLoader(searchpath=self.templates_directory),
      autoescape=True
    )

    print(f'stderr: Using the template directory: {self.templates_directory}.', file=sys.stderr)

  def _validate_context(self, context):
    return True

  def generate_output_from_template(self, template, context):
    try:
      if self._validate_context(context=context) is False:
        raise InvalidContext(message="The context didn't pass validation.") # Better way to do this with exceptions?

      t = self.env.get_template(name=self.TEMPLATE_MAPING[template])
      return t.render(**context)
    except (KeyError, jinja2.exceptions.TemplateNotFound) as e:
      raise TemplateNotFound(message=f'The template {e.message} wasn\'t found in the templates directory location of {self.templates_directory}.')
    except Exception as e:
      raise

## Create examples from here and as required for other projects.
def main():
  print('Entering main...')
  te = TemplateEngine()

  print("---\n\n### File based template")
  fbt = te.env.get_template("links.md.j2")
  print(fbt.render(title=TEST_CONTEXT['title'], users=TEST_CONTEXT['users']))

  print("---\n\n### String based template")
  sbt = te.env.from_string('Hello {{ name }}!')
  print(sbt.render(name='John Doe'))

  print("---\n\n### Class based template - Generate Exceptions")
  try:
    cbte = te.generate_output_from_template(
      template = "NON_EXISTING",
      context = TEST_CONTEXT)
    print(cbte)
  except InvalidContext as e:
    print(e.message)
  except TemplateNotFound as e:
    print(e.message)
  except Exception as e:
    print("There was an unknown exception of type {e}", type(e).__name__)

  print("---\n\n### Class based template - Working")
  try:
    cbtw = te.generate_output_from_template(
      template = "LINKS",
      context = TEST_CONTEXT)
    print(cbtw)
  except InvalidContext as e:
    print(e.message)
  except TemplateNotFound as e:
    print(e.message)
  except Exception as e:
    print("There was an unknown exception of type {e}", type(e).__name__)


if __name__ == '__main__':
    main()
