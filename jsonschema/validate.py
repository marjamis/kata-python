import json
import sys
import os
import glob
import click

from jsonschema import validate, ValidationError, SchemaError, Draft7Validator

stats = {
    'validationFailures': 0,
    'validationSuccesses': 0,
    'skipped': 0,
    'successPush': 0,
    'failedPush': 0,
}

timing_groups = [
    "1xDaily",
    "2xDaily",
    "3xDaily",
    "7xDaily",
    "Mondays",
    "Fridays",
    "Weekdays",
    "FirstofMonth",
]


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


def display_stats_summary():
    click.secho(f'\n\n\n\n### Summary', bold=True)
    click.secho(f'File validation failure count: {stats["validationFailures"]}', fg='red')
    click.secho(f'File validation success count: {stats["validationSuccesses"]}', fg='green')
    click.secho(f'\tSkipped DDB pushes: {stats["skipped"]}', fg='blue')
    click.secho(f'\tSuccessful pushes: {stats["successPush"]}', fg='green')
    click.secho(f'\tFailed pushes: {stats["failedPush"]}', fg='red', bold=True)


def is_sub_in_ddb(id):
    return None


def validated_workflow(fileContents, timing_group):
    for i in range(len(fileContents)):
        ddb = is_sub_in_ddb(fileContents[i]['id'])
        if ddb is not None:
            click.secho(f'\nSubscription exists do you want to update it from:')
            click.secho(f'{json.dumps(ddb, sort_keys=True, indent=4)}', fg='red')
            click.secho(f'to:')
            click.secho(f'{json.dumps(fileContents[i], sort_keys=True, indent=4)}', fg='green')
            check = input(click.style('Do you want to proceed (y/n/exit)? ', bold=True))

            if check == "exit":
                click.secho("Exiting run...", fg='blue')
                stats['aborts'] += (len(fileContents) - i)
                return
            elif check != "y":
                click.secho("Skipping...", fg='blue')
                stats['skipped'] += 1
                continue

        item = {
            "timing_group": {"S": timing_group},
        }

        for key, val in fileContents[i].items():
            item[key] = {"S": val}

        print(f'Pushing to DDB. STUB! {json.dumps(item, indent=4)}')

        # TODO validity check with exceptions if ddb_works(): else stats['failedPush'] += 1
        stats['successPush'] += 1


def validate_file(schema, index, file, timing_group):
    with open(file, 'r') as js:
        fileContents = json.load(js)

    click.secho(f'## Validating file #{index}: {file}', nl=False, bold=True)
    errors = check_json_contents(schema, fileContents)
    if len(errors) == 0:
        click.secho(' - Validated', fg='green', bold=True)
        stats['validationSuccesses'] += 1
        validated_workflow(fileContents, timing_group)
    else:
        click.secho(' - Errors present', fg='red', bold=True)
        stats['validationFailures'] += 1
        for index, error in enumerate(errors, start=1):
            print(f'{index}: {error.message} - {error.relative_path}')
        print('\n------\n')


@click.command()
@click.option('--timing_group', '-g', prompt='How often do you wish this file to run?', help='Select the applicable timing for this file/folder.', type=click.Choice(timing_groups, case_sensitive=True))
@click.option('--schema', '-s', default='./schema.json', help='Specifies which schema to validate the inputs against.')
@click.option('--json_file_folder', '-j', default='./test_json_files/', help='Specifies the folder or JSON file to be validated.')
def main(schema, json_file_folder, timing_group):
    with open(schema, 'r') as s:
        schema_json = json.load(s)
        schema = load_schema(schema_json)

    if os.path.isfile(json_file_folder):
        validate_file(schema, 1, json_file_folder, timing_group)
    else:
        for index, file in enumerate(sorted(glob.glob(json_file_folder + "/**/*.json", recursive=True)), start=1):
            # Only processes it if it's a file, rather than a folder.
            if os.path.isfile(file):
                validate_file(schema, index, file, timing_group)

    display_stats_summary()


if __name__ == '__main__':
    main()
