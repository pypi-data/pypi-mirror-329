""" User Profile model representing user information. """
from datetime import date
from typing import Set, Optional, ClassVar
from pydantic import EmailStr, Field, ConfigDict, field_validator
from ipulse_shared_base_ftredge import Layer, Module, list_as_lower_strings, Subject
from .base_data_model import BaseDataModel

# # Revision history (as model metadata)
# CLASS_ORIGIN_AUTHOR: ClassVar[str] = "Russlan Ramdowar;russlan@ftredge.com"
# CLASS_ORGIN_DATE: ClassVar[datetime] = datetime(2024, 1, 16, 20, 5)
class UserProfile(BaseDataModel):
    """
    User Profile model representing user information and metadata.
    Contains both system-managed and user-editable fields.
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    # Metadata as class variables
    VERSION: ClassVar[float] = 4.1
    DOMAIN: ClassVar[str] = "_".join(list_as_lower_strings(Layer.PULSE_APP, Module.CORE.name, Subject.USER.name))
    OBJ_REF: ClassVar[str] = "userprofile"
    
    # System-managed fields (read-only)
    schema_version: float = Field(
        default=VERSION,
        description="Version of this Class == version of DB Schema",
        frozen=True
    )
    
    id : str = Field(
        ...,
        description="User ID, propagated from Firebase Auth"
    )

    user_uid: str = Field(
        ...,
        description="User UID, propagated from Firebase Auth"
    )


    email: EmailStr = Field(
        ...,
        description="Propagated from Firebase Auth",
        frozen=True
    )
    organizations_uids: Set[str] = Field(
        default_factory=set,
        description="Depends on Subscription Plan, Regularly Updated"
    )
    
    # System identification (read-only)
    provider_id: str = Field(frozen=True)
    aliases: Optional[Set[str]] = Field(
        default=None
    )
    
    # User-editable fields
    username: Optional[str] = Field(
        default=None,
        max_length=50,
        pattern="^[a-zA-Z0-9_-]+$"
    )
    dob: Optional[date] = Field(
        default=None,
        description="Date of Birth"
    )
    first_name: Optional[str] = Field(
        default=None,
        max_length=100
    )
    last_name: Optional[str] = Field(
        default=None,
        max_length=100
    )
    mobile: Optional[str] = Field(
        default=None,
        pattern=r"^\+?[1-9]\d{1,14}$",  # Added 'r' prefix for raw string
        description="E.164 format phone number"
    )

    # Remove audit fields as they're inherited from BaseDataModel

    @field_validator('id', mode='before')
    @classmethod
    def validate_or_generate_id(cls, v: Optional[str], info) -> str:
        """Validate or generate user ID based on user_uid."""
        # If id is already provided (Firebase Auth case), return it
        if v:
            return v
            
        # Fallback: generate from user_uid if needed
        values = info.data
        user_uid = values.get('user_uid')
        if not user_uid:
            raise ValueError("Either id or user_uid must be provided")
        return f"{cls.OBJ_REF}_{user_uid}"