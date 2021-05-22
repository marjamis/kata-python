import templating
import requests

from templating import TemplateEngine
import test_data as td

def main():
    te = TemplateEngine()

    try:
        string_template = te.generate_output_from_string_template(
            template_string = 'Hello {{ name }}!',
            context = {
                'name': 'John Doe',
            },
        )
        print(f'From string: {string_template}\n---\n')

        test_items = [
            {
              'template': 'BASE',
              'context': td.GENERAL_TEST_CONTEXT,
            },
            {
              'template': 'TABLE_BASIC',
              'context': td.GENERAL_TEST_CONTEXT,
            },
            {
              'template': 'TABLE_CUSTOM_FUNCTION',
              'context': td.GENERAL_TEST_CONTEXT,
            },
        ]

        for i in test_items:
            rendered_template = te.generate_output_from_file_template(
                template_mapping_name = i['template'],
                context = i['context'],
            )
            print(rendered_template)
            print("\n---\n")

    except templating.InvalidContext as e:
        print(e.message)
    except templating.TemplateNotFound as e:
        print(e.message)
    except Exception as e:
        print(f'{e}')

if __name__ == '__main__':
    main()
