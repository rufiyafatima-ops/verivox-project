from pydantic import BaseModel
from typing import List, Optional

class AccountSchema(BaseModel):
    name: str
    email: str
    role: str
    org: str
    theme: str
    notifEmail: bool
    notifSms: bool
    notifDigest: bool

    class Config:
        from_attributes = True

class ControlsSchema(BaseModel):
    elevatedAlerts: bool
    autoCases: bool
    forceDrop: bool

class AIModelSchema(BaseModel):
    id: str
    name: str
    sub: str
    score: float

class AlertSchema(BaseModel):
    id: str
    title: str
    desc: str
    time: str

class SOARRuleCreate(BaseModel):
    name: str
    trigger: float
    action: str

class SOARRuleSchema(SOARRuleCreate):
    id: str
    enabled: bool

class VoiceBaselineCreate(BaseModel):
    name: str
    speaker: str

class VoiceBaselineSchema(VoiceBaselineCreate):
    id: str
    samples: int
    status: str
    created: str

class CaseNoteSchema(BaseModel):
    text: str
    time: str

class ForensicCaseCreate(BaseModel):
    id: Optional[str] = None
    caller: str
    date: Optional[str] = None
    score: float
    status: Optional[str] = "open"
    notes: List[CaseNoteSchema] = []

class ForensicCaseSchema(BaseModel):
    id: str
    caller: str
    date: str
    score: float
    status: str
    notes: List[CaseNoteSchema] = []

class CallSessionSchema(BaseModel):
    caller: str
    time: str
    score: float
    verdict: str

class MonitoringSchema(BaseModel):
    monitoring: bool

class FullStateResponse(BaseModel):
    monitoring: bool
    alertDismissed: bool
    account: AccountSchema
    session: dict
    models: List[AIModelSchema]
    controls: ControlsSchema
    alerts: List[AlertSchema]
    soarRules: List[SOARRuleSchema]
    baselines: List[VoiceBaselineSchema]
    forensics: List[ForensicCaseSchema]
    sessions: List[CallSessionSchema]