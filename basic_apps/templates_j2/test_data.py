TEST_CONTEXT = {
    "title": "Title",
    "users": [
        {
            'username': 'google',
            'url': 'https://google.com',
        },
        {
            'username': 'amazon',
            'url': 'https://amazon.com',
        },
    ],
    'stats': [
        {
            'name': 'A',
            'value1': 20,
            'value2': 30,
        },
        {
            'name': 'B',
            'value1': 202,
            'value2': 310,
        }
    ]}

TABLE_TEST_CONTEXT = {
    'summaries': [
        {
            'resolver_group': 'Total',
            'previous': {
                'number': 2,
                'oldest': 11,
                'average_age': 10,
                'percent': 1,
            },
            'number': 3,
            'oldest': 8,
            'average_age': 10.32,
            'percent': 1,
        },
        {
            'resolver_group': 'New',
            'number': 5,
            'oldest': 6,
            'average_age': 7,
            'percent': 8,
        }
    ]
}

SLACK_TEST_CONTEXT = {
    'tickets': [
        {
            'id': 1,
            'description': 'test',
            'dgd': 'testing',
        },
        {
            'id': 2,
            'description': 'again',
            'dgd': 'testinjgdgdkg',
        }
    ],
    'stats': {
        'total': 100000,
        'new': 4,
        'old': 7,
    }
}
