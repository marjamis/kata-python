import templating
import requests

from templating import TemplateEngine
from test_data import TEST_CONTEXT, TABLE_TEST_CONTEXT, SLACK_TEST_CONTEXT

def main():
  te = TemplateEngine()

  try:
    cbtw = te.generate_output_from_template(
      template = 'SLACK',
      context = SLACK_TEST_CONTEXT,
    )
    print(cbtw)

  except templating.InvalidContext as e:
    print(e.message)
  except templating.TemplateNotFound as e:
    print(e.message)
  except Exception as e:
    print("There was an unknown exception of type {e}", type(e).__name__)

if __name__ == '__main__':
    main()
