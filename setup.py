from setuptools import find_packages, setup

requires = [
    'holidays',
    'waitress',
    'pyramid',
    'uwsgi',
    'pyramid-openapi3',
    'openapi-core<=0.13.8',
]

test_requirements = []

setup_args = {
    'name': 'business_seconds',
    'version': '0.0.1',
    'description': 'Pyramid service to calculate business seconds which would accept start time and end time in ISO format',
    'classifiers': [
        'Programming Language :: Python',
    ],
    'author': 'Anish',
    'author_email': 'anishatabsa@gmail.com',
    'url': 'https://github.com/anishatabsa/business_seconds',
    'keywords': 'web wsgi pyramid swagger',
    'packages': find_packages(),
    'include_package_data': True,
    'zip_safe': False,
    'test_suite': 'tests',
    'install_requires': requires,
    'tests_require': test_requirements,
    'extras_require': {'test': test_requirements},
    'package_data': {
        'business_seconds': [
            'configuration/pyramid/*',
            'configuration/*',
            'api_docs/*',
        ]
    },
    'entry_points': {
        'paste.app_factory': [
            """business_seconds=business_seconds.server:business_seconds_server"""
        ],
        'console_scripts': [
            'initialize=business_seconds.initialize_db:initialize',
        ],
    },
}

setup(**setup_args)
