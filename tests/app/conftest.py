import os

import pytest

from traitlets.config import Config
from voila.app import Voila
from jupyter_server.serverapp import ServerApp

BASE_DIR = os.path.dirname(__file__)


class ServerAppForTesting(ServerApp):
    # pytest-tornado handles ioloop.
    default_url = 'voila'

    def start(self):
        pass


@pytest.fixture
def server_args():
    return []


@pytest.fixture
def serverapp(server_args):
    serverapp = ServerAppForTesting()
    serverapp.initialize(argv=server_args, load_extensions=False)
    return serverapp


@pytest.fixture
def voila_config():
    return {}


@pytest.fixture
def voila_args_extra():
    return []


@pytest.fixture
def voila_config_file_paths_arg():
    # we don't want the tests to use any configuration on the system
    return '--Voila.config_file_paths=[]'


@pytest.fixture
def voila_args(voila_notebook, voila_args_extra, voila_config_file_paths_arg):
    debug_args = ['--Voila.log_level=DEBUG'] if os.environ.get('VOILA_TEST_DEBUG', False) else []
    return [voila_notebook, voila_config_file_paths_arg] + voila_args_extra + debug_args

@pytest.fixture
def voila_app(serverapp, voila_args, voila_config):
    config = Config(voila_config)
    voila_app = Voila(config=config)
    voila_app.initialize(serverapp, argv=voila_args)
    yield voila_app

@pytest.fixture
def app(voila_app):
    return voila_app.serverapp.web_app