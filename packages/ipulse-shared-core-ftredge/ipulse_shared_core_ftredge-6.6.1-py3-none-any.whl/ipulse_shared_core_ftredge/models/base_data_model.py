from datetime import datetime
from typing import ClassVar
from pydantic import BaseModel, Field, ConfigDict, field_validator
import dateutil.parser

class BaseDataModel(BaseModel):
    """Base model with common fields and configuration"""
    model_config = ConfigDict(frozen=True, extra="forbid")

    # Required class variables that must be defined in subclasses
    VERSION: ClassVar[float]
    DOMAIN: ClassVar[str]
    OBJ_REF: ClassVar[str]

    # Schema versioning
    schema_version: float = Field(
        ...,  # Make this required
        description="Version of this Class == version of DB Schema",
        frozen=True
    )

    # Audit fields
    creat_date: datetime = Field(default_factory=datetime.utcnow, frozen=True)
    creat_by_user: str = Field(..., frozen=True)
    updt_date: datetime = Field(default_factory=datetime.utcnow)
    updt_by_user: str = Field(...)

    @classmethod
    def get_collection_name(cls) -> str:
        """Generate standard collection name"""
        return f"{cls.DOMAIN}_{cls.OBJ_REF}s"

    @field_validator('creat_date', 'updt_date', mode='before')
    @classmethod
    def parse_datetime(cls, v: any) -> datetime:
        if isinstance(v, datetime):
            return v
        try:
            return dateutil.parser.isoparse(v)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid datetime format: {e}")
