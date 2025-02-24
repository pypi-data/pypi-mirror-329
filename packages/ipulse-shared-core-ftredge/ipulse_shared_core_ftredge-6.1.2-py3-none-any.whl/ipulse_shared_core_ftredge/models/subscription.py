from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from typing import Set, Optional, ClassVar
from pydantic import Field, ConfigDict
from ipulse_shared_base_ftredge import Layer, Module, list_as_lower_strings, Subject, SubscriptionPlan
from .base_data_model import BaseDataModel
# ORIGINAL AUTHOR ="Russlan Ramdowar;russlan@ftredge.com"
# CLASS_ORGIN_DATE=datetime(2024, 2, 12, 20, 5)


DEFAULT_SUBSCRIPTION_PLAN = SubscriptionPlan.FREE
DEFAULT_SUBSCRIPTION_STATUS = "active"

############################################ !!!!! ALWAYS UPDATE SCHEMA VERSION , IF SCHEMA IS BEING MODIFIED !!! ############################################
class Subscription(BaseDataModel):
    """
    Represents a single subscription cycle.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    VERSION: ClassVar[float] = 1.1
    DOMAIN: ClassVar[str] = "_".join(list_as_lower_strings(Layer.PULSE_APP, Module.CORE.name, Subject.SUBSCRIPTION_PLAN.name))
    OBJ_REF: ClassVar[str] = "subscription"
    
    # System-managed fields (read-only)
    schema_version: float = Field(
        default=VERSION,
        description="Version of this Class == version of DB Schema",
        frozen=True
    )

    plan_name: SubscriptionPlan = Field(
        default=DEFAULT_SUBSCRIPTION_PLAN,
        description="Subscription Plan Name"
    )

    plan_version: float = Field(
        default=1.0,
        description="Version of the subscription plan"
    )

    cycle_start_date: datetime = Field(
        default=datetime.now(timezone.utc),
        description="Subscription Cycle Start Date"
    )
    cycle_end_date: datetime = Field(
        default=lambda: datetime.now(timezone.utc) + relativedelta(years=1),
        description="Subscription Cycle End Date"
    )
    auto_renew: bool = Field(
        default=True,
        description="Auto-renewal status"
    )
    status: str = Field(
        default=DEFAULT_SUBSCRIPTION_STATUS,
        description="Subscription Status (active, trial, inactive, etc.)"
    )

    # Remove audit fields as they're inherited from BaseDataModel