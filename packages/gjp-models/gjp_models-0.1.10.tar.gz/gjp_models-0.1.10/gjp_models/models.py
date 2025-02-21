import numpy as np
from pydantic import BaseModel, constr
from datetime import datetime, timezone

class SystemKwargs(BaseModel):
    class Config:
        extra = "allow"

class SystemConfig(BaseModel):
    ff: str
    box: str
    water: str
    system_kwargs: SystemKwargs

    class Config:
        extra = "allow"

class JobBase(BaseModel):
    pdb_id: constr(min_length=4, max_length=10)
    system_config: SystemConfig
    s3_links: dict[str, str] | None
    priority: int
    hotkeys: list[str]
    is_organic: bool = False
    active: bool = True
    update_interval: int = 2*3600
    max_time_no_improvement: int = 1500
    epsilon: float
    min_updates: int = 1
    updated_at: datetime = datetime.now(timezone.utc)
    best_loss: float = np.inf
    best_loss_at: datetime = datetime.min  # first possible datetime
    best_hotkey: str = ""
    updated_count: int = 0
    created_at: datetime = datetime.now(timezone.utc)
    best_cpt_links: list[str] | None = None
    job_type: str
    event: dict | None = None
    validator_hotkey: str | None = None
    job_id: str | None = None
    computed_rewards: list[float] | None = None # list of rewards for each hotkey. MUST be in order of hotkeys. 


class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    job_id: str
    validator_hotkey: str

    class Config:
        from_attributes = True
