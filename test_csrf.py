from app import app, users

app.config["TESTING"] = True

def test_csrf_protection():
    client = app.test_client()

    # Log in as Alice
    response = client.post(
        "/login",
        data={"username": "alice", "password": "alice123"}
    )
    assert response.status_code == 302

    # Obtain the real CSRF token from Alice's session
    with client.session_transaction() as session:
        token = session["csrf_token"]

    # Test 1: Valid token should be accepted
    response = client.post(
        "/change-email",
        data={
            "email": "alice.valid@example.com",
            "csrf_token": token
        }
    )
    assert response.status_code == 302
    print("PASS: Valid CSRF token accepted")

    # Test 2: Missing token should be rejected
    response = client.post(
        "/change-email",
        data={"email": "alice.missing@example.com"}
    )
    assert response.status_code == 403
    print("PASS: Missing CSRF token rejected")

    # Test 3: Invalid token should be rejected
    response = client.post(
        "/change-email",
        data={
            "email": "alice.invalid@example.com",
            "csrf_token": "wrong-token"
        }
    )
    assert response.status_code == 403
    print("PASS: Invalid CSRF token rejected")

    # Test 4: Unauthenticated request should be rejected
    guest = app.test_client()
    response = guest.post(
        "/change-email",
        data={
            "email": "guest@example.com",
            "csrf_token": "anything"
        }
    )
    assert response.status_code == 401
    print("PASS: Unauthenticated request rejected")

    print("\\nAll 4 CSRF security tests passed!")

if __name__ == "__main__":
    test_csrf_protection()