import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="Jordan Davis")
    email = Column(String, default="jordan.davis@acme.com")
    role = Column(String, default="Security lead")
    org = Column(String, default="Acme Corp")
    theme = Column(String, default="light")
    notif_email = Column(Boolean, default=True)
    notif_sms = Column(Boolean, default=False)
    notif_digest = Column(Boolean, default=True)

class SystemControl(Base):
    __tablename__ = "system_controls"

    id = Column(Integer, primary_key=True, index=True)
    elevated_alerts = Column(Boolean, default=True)
    auto_cases = Column(Boolean, default=True)
    force_drop = Column(Boolean, default=True)
    monitoring = Column(Boolean, default=True)
    alert_dismissed = Column(Boolean, default=False)

class AIModel(Base):
    __tablename__ = "ai_models"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sub = Column(String, nullable=False)
    score = Column(Float, default=0.0)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    desc = Column(Text, nullable=False)
    time = Column(String, nullable=False)

class SOARRule(Base):
    __tablename__ = "soar_rules"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    trigger = Column(Float, nullable=False)
    action = Column(String, nullable=False)
    enabled = Column(Boolean, default=True)

class VoiceBaseline(Base):
    __tablename__ = "voice_baselines"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    speaker = Column(String, nullable=False)
    samples = Column(Integer, default=1)
    status = Column(String, default="processing")
    created = Column(String, nullable=False)

class ForensicCase(Base):
    __tablename__ = "forensic_cases"

    id = Column(String, primary_key=True, index=True)
    caller = Column(String, nullable=False)
    date = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    status = Column(String, default="open")

    notes = relationship("CaseNote", back_populates="case", cascade="all, delete-orphan")

class CaseNote(Base):
    __tablename__ = "case_notes"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String, ForeignKey("forensic_cases.id"))
    text = Column(Text, nullable=False)
    time = Column(String, nullable=False)

    case = relationship("ForensicCase", back_populates="notes")

class CallSession(Base):
    __tablename__ = "call_sessions"

    id = Column(Integer, primary_key=True, index=True)
    caller = Column(String, nullable=False)
    time = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    verdict = Column(String, nullable=False)