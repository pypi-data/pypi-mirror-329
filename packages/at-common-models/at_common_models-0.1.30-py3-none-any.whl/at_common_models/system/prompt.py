from sqlalchemy import Column, String, Text, JSON
from at_common_models.base import BaseModel

class PromptModel(BaseModel):
    """Model for storing system prompts and their associated parameters.
    
    Attributes:
        name: Unique identifier for the prompt
        description: Description of the prompt
        tags: List of tags
        model: Model name
        sys_tpl: System template text
        usr_tpl: User template text
    """
    __tablename__ = "system_prompts"

    name = Column(String(255), primary_key=True, index=True)
    description = Column(String(1000), nullable=True)
    tags = Column(JSON, nullable=False, default=list)
    model = Column(String(64), nullable=False)
    sys_tpl = Column(Text, nullable=False)
    usr_tpl = Column(Text, nullable=False)