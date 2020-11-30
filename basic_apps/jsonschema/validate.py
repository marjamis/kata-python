import json
import sys
import os
import glob

from jsonschema import validate, ValidationError, SchemaError, Draft7Validator

DEFAULT_JSON_FILES_DIR='./test_json_files/'
DEFAULT_SCHEMA_FILE='./schema.json'

def load_schema(schema_json) -> 'jsonschema.validators.create.<locals>.Validator':
    return Draft7Validator(schema_json)

def check_json_contents(schema, json_contents) -> []:
    try:
        return sorted(schema.iter_errors(json_contents), key=str)
    except SchemaError as e:
        print("There is an error with the schema")
        raise
    except Exception as e:
        print(f'Exception: {e}')
        raise

def main():
    with open(DEFAULT_SCHEMA_FILE, 'r') as s:
        schema_json = json.load(s)
        schema = load_schema(schema_json)

    JSON_FILES_DIR = DEFAULT_JSON_FILES_DIR
    if len(sys.argv) > 1:
      JSON_FILES_DIR = sys.argv[1]

    for index, file in enumerate(sorted(glob.glob(JSON_FILES_DIR + "/**/*", recursive=True)), start=1):
        if not os.path.isfile(file):
          continue

        with open(file, 'r') as js:
            invalidJson = json.load(js)

        print(f'## Validating file #{index}: {file}', end='')
        errors = check_json_contents(schema, invalidJson)
        if len(errors) == 0:
            print(' - Validated')
        else:
            print(' - Errors present')
            for index, error in enumerate(errors, start=1):
                print(f'{index}: {error.message} - {error.relative_path}')
            print('------\n')

if __name__ == '__main__':
    main()
