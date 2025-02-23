from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class BaseModel(DeclarativeBase):
    def to_dict(self):
        data = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if isinstance(value, datetime):
                data[c.name] = value.isoformat()
            else:
                data[c.name] = value
        return data