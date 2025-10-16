import pytest
from pydgraph.errors import ConnectionError

from meteor import create_app, dgraph


@pytest.fixture
def app():
    app = create_app()

    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app


def test_dgraph_connection(app):
    with app.app_context():
        try:
            client = dgraph.connection
            assert client is not None, "DGraph client should not be None"

            version_info = client.check_version()
            assert version_info is not None, "DGraph version info should not be None"

        except ConnectionError as e:
            pytest.fail(f"Connection to DGraph failed: {e}")
