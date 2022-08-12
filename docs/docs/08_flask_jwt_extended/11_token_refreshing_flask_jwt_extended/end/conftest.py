import pytest
from flask_jwt_extended import create_access_token
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


@pytest.fixture()
def fresh_jwt(app):
    with app.app_context():
        access_token = create_access_token(identity=1, fresh=True)
        return access_token


@pytest.fixture()
def jwt(app):
    with app.app_context():
        access_token = create_access_token(identity=1)
        return access_token


@pytest.fixture()
def admin_jwt(app):
    with app.app_context():
        access_token = create_access_token(
            identity=1, additional_claims={"is_admin": True}
        )
        return access_token
