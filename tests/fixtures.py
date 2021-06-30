import pytest
from business_seconds.controllers import business_seconds_controller as c


@pytest.fixture(scope='module')
def controller(request):
    controller = c.Controller()
    yield controller
    pass
