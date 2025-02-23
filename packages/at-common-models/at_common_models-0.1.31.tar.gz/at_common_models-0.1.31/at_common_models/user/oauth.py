from sqlalchemy import Column, String, DateTime
import uuid, sqlalchemy
from at_common_models.base import BaseModel

class UserOAuth(BaseModel):
    __tablename__ = "user_oauths"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), index=True)
    email = Column(String(255), index=True)
    provider = Column(String(50), nullable=False, index=True)
    provider_user_id = Column(String(255), nullable=False, index=True)
    access_token = Column(String(1024), nullable=True)
    refresh_token = Column(String(1024), nullable=True)
    expires_at = Column(DateTime, nullable=True)

    __table_args__ = (
        sqlalchemy.UniqueConstraint('provider', 'provider_user_id', name='uq_provider_user_id'),
        sqlalchemy.Index('idx_provider_provider_user_id', 'provider', 'provider_user_id'),
    )

    def __str__(self):
        return f"<UserOAuth(id={self.id}, user_id={self.user_id}, email={self.email}"

    def __repr__(self):
        return f"<UserOAuth(id={self.id}, user_id={self.user_id}, email={self.email}"