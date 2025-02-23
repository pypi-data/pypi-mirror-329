from sqlalchemy import Column, String, JSON
from at_common_models.base import BaseModel

class WorkflowModel(BaseModel):
    """Model for storing system workflows and their associated parameters.
    
    Attributes:
        name: Unique identifier for the workflow
        description: Description of the workflow
        tags: List of tags
        initial_context_schema: Initial context schema
    """
    __tablename__ = "system_workflows"

    name = Column(String(255), primary_key=True, index=True)
    description = Column(String(1000), nullable=True)
    tags = Column(JSON, nullable=False, default=list)
    initial_context_schema = Column(JSON, nullable=False, default=dict)