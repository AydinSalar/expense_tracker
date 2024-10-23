def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Expense Tracker' in response.data

def test_registration(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPass123',
        'confirm_password': 'TestPass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Your account has been created!' in response.data

def test_login_logout(client):
    # Register a user
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPass123',
        'confirm_password': 'TestPass123'
    }, follow_redirects=True)

    # Log in
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'TestPass123'
    }, follow_redirects=True)
    assert b'You have been logged in!' in response.data

    # Log out
    response = client.get('/logout', follow_redirects=True)
    assert b'You have been logged out.' in response.data