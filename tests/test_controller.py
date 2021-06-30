"""
Pytest for controller
"""
import logging
import random
import sys

import faker
import pytest
import six

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))
fake = faker.Factory.create()


def test_hello(database, controller):
    """
        Test hello
    """
    name = fake.name()
    result = controller.hello(name)
    assert result == 'Hello there, {}!'.format(name)

def test_hello_friends(database, controller):
    """
        Test hello friends
    """
    name = fake.name()
    friends = [{'name': fake.name(), 'gender': 'male' if random.randint(0,1) else 'female'} for i in six.moves.builtins.range(0,100)]
    result = controller.hello_friends(name, friends)
    assert result

def test_get_thing(database, controller):
    """
        Test hello friends
    """
    name = fake.name()
    while name == 'what':
        name = fake.name()
    with pytest.raises(errors.NotFoundException):
        result = controller.get_thing(name)
    assert controller.get_thing('what')['name'] == 'what'
