GENERAL_TEST_CONTEXT = {
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
    'stats_as_list': [
        {
            'name': 'A',
            'size': 2000,
        },
        {
            'name': 'B',
            'size': 202,
        }
    ],
    'stats_as_dict': {
        'A': {
            'size': 3000,
        },
        'B': {
            'size': 4,
        }
    },
    'summaries': [
        {
            'group': 'Total',
            'number': 3,
            'oldest': 8,
            'average_age': 10.32,
            'percent': 1,
        },
        {
            'group': 'New',
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
