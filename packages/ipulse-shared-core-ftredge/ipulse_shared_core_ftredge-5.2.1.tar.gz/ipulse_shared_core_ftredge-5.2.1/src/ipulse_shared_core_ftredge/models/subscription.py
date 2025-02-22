from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from typing import Set, Optional, Dict, List, ClassVar
from pydantic import BaseModel, Field, ConfigDict
from ipulse_shared_base_ftredge import Layer, Module, list_as_lower_strings, Sector, SubscriptionPlan
# ORIGINAL AUTHOR ="Russlan Ramdowar;russlan@ftredge.com"
# CLASS_ORGIN_DATE=datetime(2024, 2, 12, 20, 5)


DEFAULT_SUBSCRIPTION_PLAN = SubscriptionPlan.FREE
DEFAULT_SUBSCRIPTION_STATUS = "active"

############################################ !!!!! ALWAYS UPDATE SCHEMA VERSION , IF SCHEMA IS BEING MODIFIED !!! ############################################
class Subscription(BaseModel):
    """
    Represents a single subscription cycle.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    VERSION: ClassVar[float] = 1.1
    DOMAIN: ClassVar[str] = "_".join(list_as_lower_strings(Layer.PULSE_APP, Module.CORE.name, Sector.LOOKUP.name))
    
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

    cycle_start_date: datetime = Field(
        default=datetime.now(timezone.utc),
        description="Subscription Cycle Start Date"
    )
    cycle_end_date: datetime = Field(
        default=lambda: datetime.now(timezone.utc) + relativedelta(years=1),
        description="Subscription Cycle End Date"
    )
    status: str = Field(
        default=DEFAULT_SUBSCRIPTION_STATUS,
        description="Subscription Status (active, inactive, etc.)"
    )