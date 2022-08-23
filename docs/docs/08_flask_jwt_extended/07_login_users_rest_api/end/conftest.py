import pytest
from app import create_app


@pytest.fixture()
def app():
    app = create_app("sqlite://")
    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
