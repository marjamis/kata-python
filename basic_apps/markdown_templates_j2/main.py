import templating

from templating import TemplateEngine
from test_data import TEST_CONTEXT

def main():
  te = TemplateEngine()

  try:
    cbtw = te.generate_output_from_template(
      template = 'UPDATED_BASE',
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
