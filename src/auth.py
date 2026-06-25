# src/auth.py
# Handles user registration, login, and password hashing

import bcrypt
from database import create_user, get_user_by_username, get_user_by_email


def hash_password(password):
    """
    Hash a password using bcrypt.
    bcrypt automatically adds a random salt — making every hash unique
    even if two users have the same password.
    """
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password, hashed_password):
    """
    Check if a plain password matches the stored hash.
    Returns True if correct, False if wrong.
    """
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def register_user(username, email, password):
    """
    Register a new user.
    Returns: (success: bool, message: str, user_id: int or None)
    """
    # Validate inputs
    if len(username.strip()) < 3:
        return False, "Username must be at least 3 characters.", None

    if len(password) < 6:
        return False, "Password must be at least 6 characters.", None

    if "@" not in email or "." not in email:
        return False, "Please enter a valid email address.", None

    # Check if username already taken
    if get_user_by_username(username):
        return False, "Username already taken. Please choose another.", None

    # Check if email already registered
    if get_user_by_email(email):
        return False, "Email already registered. Please login instead.", None

    # Hash password and save user
    password_hash = hash_password(password)
    user_id = create_user(username, email, password_hash)

    if user_id:
        return True, f"Account created! Welcome, {username}!", user_id
    else:
        return False, "Registration failed. Please try again.", None


def login_user(username, password):
    """
    Login an existing user.
    Returns: (success: bool, message: str, user: dict or None)
    """
    if not username or not password:
        return False, "Please enter both username and password.", None

    user = get_user_by_username(username)

    if not user:
        return False, "Username not found. Please check or register.", None

    if not verify_password(password, user["password_hash"]):
        return False, "Incorrect password. Please try again.", None

    return True, f"Welcome back, {user['username']}!", user


if __name__ == "__main__":
    from database import init_database
    init_database()

    print("Testing auth system...")

    # Register a user
    success, msg, user_id = register_user("mahal", "mahal@test.com", "password123")
    print(f"Register: {msg} (ID: {user_id})")

    # Try duplicate username
    success, msg, user_id = register_user("mahal", "other@test.com", "pass456")
    print(f"Duplicate: {msg}")

    # Login correctly
    success, msg, user = login_user("mahal", "password123")
    print(f"Login: {msg}")

    # Wrong password
    success, msg, user = login_user("mahal", "wrongpass")
    print(f"Wrong pass: {msg}")

    print("\n✅ Auth test complete!")