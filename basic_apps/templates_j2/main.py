import templating
import requests

from templating import TemplateEngine
import test_data as td

def main():
  te = TemplateEngine()

  try:
    cbtw = te.generate_output_from_template(
      template = 'TEMP',
      context = td.TEMP,
    )
    print(cbtw)

  except templating.InvalidContext as e:
    print(e.message)
  except templating.TemplateNotFound as e:
    print(e.message)
  except Exception as e:
    print(f'{e}')

if __name__ == '__main__':
    main()
