# Import all models to register them with SQLAlchemy
from at_common_models.system.cache import CacheModel
from at_common_models.system.prompt import PromptModel
from at_common_models.system.workflow import WorkflowModel
from at_common_models.user.account import UserAccount
from at_common_models.user.oauth import UserOAuth
from at_common_models.user.subscription import UserSubscription
from at_common_models.base import BaseModel

# These imports will register all models with the Base.metadata
__all__ = [
    'BaseModel',
    'CacheModel',
    'PromptModel',
    'WorkflowModel',
    'UserAccount',
    'UserOAuth',
    'UserSubscription'
]
