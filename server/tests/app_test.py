from flask.testing import FlaskClient


def test_hello(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'<p>Hello World!</p>'
