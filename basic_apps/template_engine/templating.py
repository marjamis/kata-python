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
        'TABLE_BASIC': 'table_formatting.html.j2',
        'TABLE_CUSTOM_FUNCTION': 'table_formatting_custom_global_function.md.j2',
    }

    def __init__(self):
        self.templates_directory = os.getcwd()+"/templates/"
        self.env = Environment(
            loader=FileSystemLoader(searchpath=self.templates_directory),
            autoescape=True
        )

        # Adds additional filters for the Jinja environment
        self.env.filters.update(
            {
                'TrendIconAvsB': TrendIconAvsBFilter,
                'ComparedString': ComparedStringFilter,
            }
        )

        # Adds additional global functions for the Jinja environment
        self.env.globals.update(
            {
                'SlackTableListGenerator': SlackTableListGenerator,
                'SlackTableDictGenerator': SlackTableDictGenerator,
            }
        )

        print(f'stderr: Using the template directory: {self.templates_directory}.', file=sys.stderr)

    def _validate_context(self, context):
        return True

    def _generate_output_from_template(self, template, context):
        try:
            if self._validate_context(context=context) is False:
                raise InvalidContext(message="The context didn't pass validation.")

            return template.render(**context)
        except (KeyError, jinja2.exceptions.TemplateNotFound) as e:
            raise TemplateNotFound(message=f'The template {e.message} wasn\'t found in the templates directory location of {self.templates_directory}.')
        except Exception as e:
            raise

    def generate_output_from_file_template(self, template_mapping_name, context):
        t = self.env.get_template(name=self.TEMPLATE_MAPING[template_mapping_name])
        return self._generate_output_from_template(t, context)

    def generate_output_from_string_template(self, template_string, context):
        t = self.env.from_string(template_string)
        return self._generate_output_from_template(t, context)


def ComparedStringFilter(a, b, suffix=''):
    '''Provide two values and a formatted string will be returned based on the value of b relative to a.'''
    return f'{a}{suffix} ({TrendIconAvsBFilter(a, b)} {b}{suffix})'


def TrendIconAvsBFilter(a, b):
    '''Returns a unicode character based on the value of b relative to a.'''
    if a > b:
        icon = '\u2b06'
    elif a < b:
        icon = '\u2b07'
    elif a == b:
        icon = '\u2A75'
    return icon


def SlackTableDictGenerator(dataDict) -> str:
    ''' Provide a consistent, i.e. all keys are the same, dictionary and a table will be generated based off of those keys and their respective values.'''
    try:
        headers = list(dataDict[0].keys())

        data = []
        for d in range(len(dataDict)):
            tempd = []
            for header in range(len(headers)):
                tempd.append(dataDict[d][headers[header]])
            data.append(tempd)

        return SlackTableListGenerator(headers, data)
    except Exception as e:
        print(e)
        raise e


def SlackTableListGenerator(headers, data) -> str:
    ''' Provide a consistent, i.e. all keys are the same, list and a table will be generated based off of those keys and their respective values.'''
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
    print('Not implemented.')


if __name__ == '__main__':
    main()
