import pytest
from app import app, send_verification_email
from unittest.mock import patch

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Subscribe to Updates' in response.data

@patch('app.send_verification_email')
def test_subscribe_form(mock_send_email, client):
    mock_send_email.return_value = None
    response = client.post('/subscribe', data={'email': 'test@example.com'})
    assert response.status_code == 200
    assert b'Subscription successful, verification email sent!' in response.data

def test_send_verification_email(monkeypatch):
    class MockMail:
        def send(self, msg):
            self.msg = msg

    mock_mail = MockMail()
    monkeypatch.setattr('app.mail', mock_mail)

    send_verification_email('test@example.com')
    assert mock_mail.msg.subject == 'Verify your email'
    assert mock_mail.msg.recipients == ['test@example.com']
    assert 'Please verify your email by clicking the link.' in mock_mail.msg.body
