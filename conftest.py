import pytest
from core import app

@pytest.fixture
def api():
    client = app.test_client()
    return client

@pytest.fixture
def source():
    source = click_on_page('hello', 'adele')
    return source

@pytest.fixture
def mock_get_sqlalchemy(mocker):
    mock = mocker.patch("flask_sqlalchemy._QueryProperty.__get__").return_value = mocker.Mock()
