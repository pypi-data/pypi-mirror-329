from sqlalchemy import Column, String, LargeBinary, DateTime
from at_common_models.base import BaseModel

class CacheModel(BaseModel):
    """Model for storing system cache entries.
    
    Attributes:
        key: Unique identifier for the cache entry
        value: Binary data stored in the cache
        expires_at: Expiration datetime for the cache entry
    """
    __tablename__ = "system_cache"

    key = Column(String(255), primary_key=True)
    value = Column(LargeBinary(length=(2**24)-1), nullable=False)
    expires_at = Column(DateTime, nullable=False)