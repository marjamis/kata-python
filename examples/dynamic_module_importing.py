import itertools
import importlib

# Dynamically imports the specified module, initialises the provided class in this module with the initial_test_value and executes the provided entry_method. This allows for dynamic import and execution when you dont want/need to import all at time of execution.
routes = {
    'sample_import': {
        'module': 'example_package.test',
        'class': 'TestingClass',
        'entry_method': 'get_test_value_times_by_three',
        'initial_test_value': 3,
    },
    'sample_import_1': {
        'module': 'example_package.test',
        'class': 'TestingClass',
        'entry_method': 'get_test_value_times_by_three',
        'initial_test_value': 6,
    },
}

# For illustration purposes loops through the routes keys and provides a count if needed in the future
for count, key in enumerate(routes.keys()):
    # Set the dictionary for this specific key to the feature. Note: There are more efficient ways to this but this is set this way for illustration purposes
    feature = routes[key]

    # Loops though the components of the module key for the feature to be individually imported and available for dynamic use later in the code
    for module in itertools.accumulate([module] for module in feature['module'].split('.')):
        m = '.'.join(module)
        globals()[m] = importlib.import_module(m)

    # Dynamically gets the class from the module, and initialises it with with the initial_test_value
    cls = getattr(globals()[feature['module']], feature['class'])(feature['initial_test_value'])
    # Using the initialised class execute the entry_method
    method = getattr(cls, feature['entry_method'])

    print(method())
