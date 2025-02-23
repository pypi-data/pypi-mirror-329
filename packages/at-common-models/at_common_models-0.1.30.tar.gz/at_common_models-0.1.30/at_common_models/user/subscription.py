from sqlalchemy import Index, Column, String, BigInteger, DateTime, Boolean, Enum as SQLEnum
from at_common_models.base import BaseModel
from sqlalchemy.sql import func
from enum import Enum

class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    INCOMPLETE = "incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired"
    TRIALING = "trialing"
    UNPAID = "unpaid"

    @classmethod
    def from_stripe_status(cls, stripe_status: str) -> 'SubscriptionStatus':
        """Convert Stripe subscription status to internal status"""
        try:
            return cls(stripe_status)
        except ValueError:
            return cls.INCOMPLETE

class UserSubscription(BaseModel):
    __tablename__ = "user_subscriptions"

    stripe_subscription_id = Column(String(255), primary_key=True, default='')
    stripe_customer_id = Column(String(255), nullable=False)
    user_id = Column(String(36), nullable=False)
    price_id = Column(String(255), nullable=False)
    status = Column(SQLEnum(SubscriptionStatus), nullable=False)

    # Billing cycle
    current_period_start = Column(DateTime, nullable=False)
    current_period_end = Column(DateTime, nullable=False)
    cancel_at_period_end = Column(Boolean, default=False)
    canceled_at = Column(DateTime, nullable=True)

    # Metadata and timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Strip event timestamps
    last_event_timestamp = Column(BigInteger, nullable=False, default=0)

      # Indexes
    __table_args__ = (
        Index('idx_sub_user_status', user_id, status),
        Index('idx_sub_period_end', current_period_end),
    )

    def __str__(self):
        return f"<UserSubscription(stripe_subscription_id={self.stripe_subscription_id}, stripe_customer_id={self.stripe_customer_id}, user_id={self.user_id}"

    def __repr__(self):
        return f"<UserSubscription(stripe_subscription_id={self.stripe_subscription_id}, stripe_customer_id={self.stripe_customer_id}, user_id={self.user_id}"