from datetime import datetime
from typing import Set, Optional, Dict, List, ClassVar
from pydantic import BaseModel, Field, ConfigDict, field_validator
from .subscription import Subscription
from ipulse_shared_base_ftredge import Layer, Module, list_as_lower_strings, Subject
import dateutil.parser
from .base_data_model import BaseDataModel
# ORIGINAL AUTHOR ="Russlan Ramdowar;russlan@ftredge.com"
# CLASS_ORGIN_DATE=datetime(2024, 2, 12, 20, 5)

############################################ !!!!! ALWAYS UPDATE SCHEMA VERSION , IF SCHEMA IS BEING MODIFIED !!! ############################################
class UserStatus(BaseDataModel):
    """
    User Status model for tracking user subscription and access rights.
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    # Class constants
    VERSION: ClassVar[float] = 4.1
    DOMAIN: ClassVar[str] = "_".join(list_as_lower_strings(Layer.PULSE_APP, Module.CORE.name, Subject.USER.name))
    OBJ_REF: ClassVar[str] = "userstatus"
    
    # Default values as class variables
    DEFAULT_IAM_GROUPS: ClassVar[Dict[str, List[str]]] = {"pulseroot": ["full_open_read"]}
    DEFAULT_SUBSCRIPTION_PLAN: ClassVar[str] = "subscription_free"
    DEFAULT_SUBSCRIPTION_STATUS: ClassVar[str] = "active"
    DEFAULT_SUBSCRIPTION_INSIGHT_CREDITS: ClassVar[int] = 10
    DEFAULT_VOTING_CREDITS: ClassVar[int] = 0
    DEFAULT_EXTRA_INSIGHT_CREDITS: ClassVar[int] = 0
    

    # System-managed fields
    schema_version: float = Field(
        default=VERSION,
        frozen=True,
        description="Version of this Class == version of DB Schema"
    )
    
    id : str = Field(
        ...,
        description="User ID, format: {OBJ_REF}_{user_uid}"
    )

    user_uid: str = Field(
        ...,
        description="User UID from Firebase Auth"
    )

    # IAM and subscription fields
    iam_groups: Dict[str, List[str]] = Field(
        default_factory=lambda: UserStatus.DEFAULT_IAM_GROUPS,
        description="User's Groups, with a default one for all authenticated Pulse users"
    )
    
    # Subscription Management
    subscriptions: Dict[str, Subscription] = Field(
        default_factory=dict,
        description="Dictionary of user's active and past subscriptions, keyed by plan name"
    )

    # Credits management
    sbscrptn_based_insight_credits: int = Field(
        default_factory=lambda: UserStatus.DEFAULT_SUBSCRIPTION_INSIGHT_CREDITS,
        description="Subscription-based insight credits"
    )
    sbscrptn_based_insight_credits_updtd_on: datetime = Field(
        default_factory=datetime.now,
        description="Last update timestamp for subscription credits"
    )
    extra_insight_credits: int = Field(
        default_factory=lambda: UserStatus.DEFAULT_EXTRA_INSIGHT_CREDITS,
        description="Additional purchased insight credits (non-expiring)"
    )

    extra_insight_credits_updtd_on: datetime = Field(
        default_factory=datetime.now,
        description="Last update timestamp for extra credits"
    )

    voting_credits: int = Field(
        default=lambda : UserStatus.DEFAULT_VOTING_CREDITS,
        description="Voting credits for user"
    )
    
    # Optional fields
    payment_refs_uids: Optional[Set[str]] = None
    
    # Remove audit fields as they're inherited from BaseDataModel

    @field_validator('id', mode='before')
    @classmethod
    def validate_or_generate_id(cls, v: Optional[str], info) -> str:
        # If id is already provided (Firebase Auth case), return it
        if v:
            return v
            
        # Fallback: generate from user_uid if needed
        values = info.data
        user_uid = values.get('user_uid')
        if not user_uid:
            raise ValueError("Either id or user_uid must be provided")
        return f"{cls.OBJ_REF}_{user_uid}"