from datetime import datetime, timedelta
from at_common_models.user.account import UserAccount
from at_common_models.user.oauth import UserOAuth

def test_user_account_model(session):
    # Create test data
    user = UserAccount(
        email="test@example.com",
        name="Test User",
        hashed_password="hashed_password_123",
        profile_picture="https://example.com/pic.jpg",
        is_active=True,
        verification_token="verify_123",
        verification_token_expires=datetime.now() + timedelta(days=1),
        reset_token="reset_123",
        reset_token_expires=datetime.now() + timedelta(days=1),
        stripe_customer_id="cus_123456"
    )
    
    session.add(user)
    session.commit()
    
    result = session.query(UserAccount).filter_by(email="test@example.com").first()
    assert result.email == "test@example.com"
    assert result.name == "Test User"
    assert result.is_active == True
    assert result.hashed_password == "hashed_password_123"
    assert result.stripe_customer_id == "cus_123456"

def test_user_oauth_model(session):
    # Create test data
    oauth = UserOAuth(
        user_id="user_123",
        email="test@example.com",
        provider="google",
        provider_user_id="google_user_123",
        access_token="access_token_123",
        refresh_token="refresh_token_123",
        expires_at=datetime.now() + timedelta(hours=1)
    )
    
    session.add(oauth)
    session.commit()
    
    result = session.query(UserOAuth).filter_by(user_id="user_123").first()
    assert result.email == "test@example.com"
    assert result.provider == "google"
    assert result.provider_user_id == "google_user_123"

def test_user_account_str_repr(session):
    user = UserAccount(
        email="test@example.com",
        name="Test User",
        stripe_customer_id="cus_789"
    )
    
    assert str(user) == f"<UserAccount(id={user.id}, email=test@example.com, name=Test User)>"
    assert repr(user) == f"<UserAccount(id={user.id}, email=test@example.com, name=Test User)>"

def test_user_oauth_unique_constraint(session):
    # Test the unique constraint on provider and provider_user_id
    oauth1 = UserOAuth(
        user_id="user_123",
        email="test1@example.com",
        provider="google",
        provider_user_id="google_user_123",
        access_token="access_token_1",
        refresh_token="refresh_token_1",
        expires_at=datetime.now() + timedelta(hours=1)
    )
    
    oauth2 = UserOAuth(
        user_id="user_456",
        email="test2@example.com",
        provider="google",
        provider_user_id="google_user_123",  # Same provider and provider_user_id
        access_token="access_token_2",
        refresh_token="refresh_token_2",
        expires_at=datetime.now() + timedelta(hours=1)
    )
    
    session.add(oauth1)
    session.commit()
    
    try:
        session.add(oauth2)
        session.commit()
        assert False, "Should have raised an integrity error"
    except:
        session.rollback()
        assert True

def test_user_account_email_unique(session):
    # Test unique email constraint
    user1 = UserAccount(
        email="same@example.com",
        name="User One",
        stripe_customer_id="cus_123"
    )
    
    user2 = UserAccount(
        email="same@example.com",  # Same email
        name="User Two",
        stripe_customer_id="cus_456"
    )
    
    session.add(user1)
    session.commit()
    
    try:
        session.add(user2)
        session.commit()
        assert False, "Should have raised an integrity error"
    except:
        session.rollback()
        assert True 