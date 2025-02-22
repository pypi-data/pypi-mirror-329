from datetime import datetime, date
from typing import Set, Optional, ClassVar
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from ipulse_shared_base_ftredge import Layer, Module, list_as_lower_strings, Sector

# # Revision history (as model metadata)
# CLASS_ORIGIN_AUTHOR: ClassVar[str] = "Russlan Ramdowar;russlan@ftredge.com"
# CLASS_ORGIN_DATE: ClassVar[datetime] = datetime(2024, 1, 16, 20, 5)
class UserProfile(BaseModel):
    """
    User Profile model representing user information and metadata.
    Contains both system-managed and user-editable fields.
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    # Metadata as class variables
    VERSION: ClassVar[float] = 4.1
    DOMAIN: ClassVar[str] = "_".join(list_as_lower_strings(Layer.PULSE_APP, Module.CORE.name, Sector.USERCORE.name))
    
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
    
    # Timestamps and audit fields (read-only)
    creat_date: datetime = Field(frozen=True)
    creat_by_user: str = Field(frozen=True)
    updt_date: datetime = Field(frozen=True)
    updt_by_user: str = Field(frozen=True)
    
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

    # Audit fields
    creat_date: datetime = Field(default_factory=datetime.now)
    creat_by_user: str = Field(frozen=True)
    updt_date: datetime = Field(default_factory=datetime.now)
    updt_by_user: str = Field(frozen=True)