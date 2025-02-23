from datetime import datetime, timedelta
from uuid import uuid4
from at_common_models.user.subscription import UserSubscription, SubscriptionStatus
from sqlalchemy.exc import IntegrityError

def test_user_subscription_model(session):
    # Create test data
    now = datetime.now()
    user_id = str(uuid4())
    subscription = UserSubscription(
        user_id=user_id,
        stripe_subscription_id="sub_123",
        stripe_customer_id="cus_123",
        price_id="price_123",
        status=SubscriptionStatus.ACTIVE,
        current_period_start=now,
        current_period_end=now + timedelta(days=30),
        cancel_at_period_end=False
    )
    
    session.add(subscription)
    session.commit()
    
    result = session.query(UserSubscription).filter_by(user_id=user_id).first()
    assert result.stripe_subscription_id == "sub_123"
    assert result.stripe_customer_id == "cus_123"
    assert result.price_id == "price_123"
    assert result.status == SubscriptionStatus.ACTIVE
    assert result.current_period_start == now
    assert result.current_period_end == now + timedelta(days=30)
    assert result.cancel_at_period_end == False
    assert result.canceled_at is None

def test_subscription_unique_constraints(session):
    now = datetime.now()
    # Test unique constraint on stripe_subscription_id
    user_id1 = str(uuid4())
    user_id2 = str(uuid4())
    
    sub1 = UserSubscription(
        user_id=user_id1,
        stripe_subscription_id="sub_123",
        stripe_customer_id="cus_123",
        price_id="price_123",
        status=SubscriptionStatus.ACTIVE,
        current_period_start=now,
        current_period_end=now + timedelta(days=30)
    )
    
    sub2 = UserSubscription(
        user_id=user_id2,
        stripe_subscription_id="sub_123",  # Same stripe_subscription_id
        stripe_customer_id="cus_456",
        price_id="price_456",
        status=SubscriptionStatus.ACTIVE,
        current_period_start=now,
        current_period_end=now + timedelta(days=30)
    )
    
    session.add(sub1)
    session.commit()
    
    # Test that we can't add another subscription with the same stripe_subscription_id
    try:
        session.add(sub2)
        session.commit()
        assert False, "Should have raised an IntegrityError"
    except IntegrityError:
        session.rollback()
    except Exception as e:
        session.rollback()
        assert False, f"Wrong exception type raised: {type(e)}"

def test_subscription_status_transitions(session):
    # Test subscription status changes
    now = datetime.now()
    user_id = str(uuid4())
    subscription = UserSubscription(
        user_id=user_id,
        stripe_subscription_id="sub_789",
        stripe_customer_id="cus_789",
        price_id="price_789",
        status=SubscriptionStatus.ACTIVE,
        current_period_start=now,
        current_period_end=now + timedelta(days=30)
    )
    
    session.add(subscription)
    session.commit()
    
    # Update subscription status
    subscription.status = SubscriptionStatus.CANCELED
    subscription.cancel_at_period_end = True
    subscription.canceled_at = now
    session.commit()
    
    result = session.query(UserSubscription).filter_by(user_id=user_id).first()
    assert result.status == SubscriptionStatus.CANCELED
    assert result.cancel_at_period_end == True
    assert result.canceled_at == now