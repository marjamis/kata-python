import jinja2
import os
import sys

from jinja2 import Environment, FileSystemLoader
import test_data as td


class TemplateNotFound(Exception):
    def __init__(self, message):
        self.message = message


class InvalidContext(Exception):
    def __init__(self, message):
        self.message = message


class TemplateEngine():
    TEMPLATE_MAPING = {
        'BASE': 'base.md.j2',
        'NON_EXISTING': 'base2.md.j2',
        'LINKS': 'links.md.j2',
        'STATS': 'stats.md.j2',
        'UPDATED_BASE': 'updated_base.md.j2',
        'TABLE': 'table_formatting.html.j2',
        'SLACK': 'tickets.slack.j2',
        'TABLE_FROM_DICT': 'tableFromDictionary.txt.j2',
        'TEMP': 'temp.json.j2',
    }

    def __init__(self):
        self.templates_directory = os.getcwd()+"/templates/"
        self.env = Environment(
            loader=FileSystemLoader(searchpath=self.templates_directory),
            autoescape=True
        )
        # Adds a filter for the Jinja environment
        self.env.filters['TrendIconAvsB'] = TrendIconAvsBFilter
        self.env.filters['ComparedString'] = ComparedString
        self.env.filters['SlackTableListGenerator'] = SlackTableListGeneratorFilter
        self.env.filters['SlackTableDictGenerator'] = SlackTableDictGeneratorFilter

        print(f'stderr: Using the template directory: {self.templates_directory}.', file=sys.stderr)

    def _validate_context(self, context):
        return True

    def generate_output_from_template(self, template, context):
        try:
            if self._validate_context(context=context) is False:
                # Better way to do this with exceptions?
                raise InvalidContext(message="The context didn't pass validation.")

            t = self.env.get_template(name=self.TEMPLATE_MAPING[template])
            return t.render(**context)
        except (KeyError, jinja2.exceptions.TemplateNotFound) as e:
            raise TemplateNotFound(message=f'The template {e.message} wasn\'t found in the templates directory location of {self.templates_directory}.')
        except Exception as e:
            raise

def ComparedString(a, b, suffix=''):
    return f'{a}{suffix} ({TrendIconAvsBFilter(a, b)} {b}{suffix})'

def TrendIconAvsBFilter(a, b):
    if a > b:
        icon = '\u2b06'
    elif a < b:
        icon = '\u2b07'
    elif a == b:
        icon = '\u2A75'
    return icon


def SlackTableDictGeneratorFilter(dataDict) -> str:
    """ """
    try:
        headers = list(dataDict[0].keys())

        data = []
        for d in range(len(dataDict)):
            tempd = []
            for header in range(len(headers)):
                tempd.append(dataDict[d][headers[header]])
            data.append(tempd)

        return SlackTableListGeneratorFilter(headers, data)
    except Exception as e:
        print(e)
        raise e


def SlackTableListGeneratorFilter(headers, data) -> str:
    """ """
    try:
        result = ''

        # Determines the max length of each column based on the headers and the data for that header
        lengths = []
        for col in range(len(data[0])):
            maxLength = len(headers[col])
            for row in range(len(data)):
                if len(str(data[row][col])) > maxLength:
                    maxLength = len(str(data[row][col]))
            lengths.append(maxLength)

        # Outputs the headers with required padding
        result += f'| '
        for i in range(len(headers)):
            result += f'{str(headers[i]).ljust(lengths[i])} | '
        result += f'\n'

        # Outputs the delimeter between the headers and data based on the max length of padding
        result += f'| '
        for i in range(len(headers)):
            for j in range(lengths[i]):
                result += f'-'
            result += f' | '
        result += f'\n'

        # Outputs each row of data with required padding
        for row in range(len(data)):
            result += f'| '
            for col in range(len(data[row])):
                result += f'{str(data[row][col]).ljust(lengths[col])} | '
            result += f'\n'

        return result
    except Exception as e:
        print(e)
        raise e


def main():
  # Create examples from here and as required for other projects.
    print('Entering main...')
    te = TemplateEngine()

    print("---\n\n### File based template")
    fbt = te.env.get_template("links.md.j2")
    print(fbt.render(title=td.TEST_CONTEXT['title'], users=td.TEST_CONTEXT['users']))

    print("---\n\n### String based template")
    sbt = te.env.from_string('Hello {{ name }}!')
    print(sbt.render(name='John Doe'))

    print("---\n\n### Class based template - Generate Exceptions")
    try:
        cbte = te.generate_output_from_template(
            template="NON_EXISTING",
            context=td.TEST_CONTEXT)
        print(cbte)
    except InvalidContext as e:
        print(e.message)
    except TemplateNotFound as e:
        print(e.message)
    except Exception as e:
        print(f'There was an unknown exception of type "{type(e).__name__}": "{e}"')

    print("---\n\n### Class based template - Working")
    try:
        cbtw = te.generate_output_from_template(
            template="LINKS",
            context=td.TEST_CONTEXT)
        print(cbtw)
    except InvalidContext as e:
        print(e.message)
    except TemplateNotFound as e:
        print(e.message)
    except Exception as e:
        print("There was an unknown exception of type {e}", type(e).__name__)

    print('---\n\n### Class based template with optional use of a filter')
    try:
        cbtw = te.generate_output_from_template(
            template="TABLE",
            context=td.TABLE_TEST_CONTEXT)
        print(cbtw)
    except InvalidContext as e:
        print(e.message)
    except TemplateNotFound as e:
        print(e.message)
    except Exception as e:
        print("There was an unknown exception of type {e}", type(e).__name__)

    print('---\n\n### Using a custom filter to take data in a dictionary and print it as a table')
    try:
        cbtw = te.generate_output_from_template(
            template="TABLE_FROM_DICT",
            context=td.SLACK_TEST_CONTEXT)
        print(cbtw)
    except InvalidContext as e:
        print(e.message)
    except TemplateNotFound as e:
        print(e.message)
    except Exception as e:
        print("There was an unknown exception of type {e}", type(e).__name__)


if __name__ == '__main__':
    main()
