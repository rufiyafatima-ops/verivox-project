import uuid
import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(prefix="/api")

@router.get("/state")
def get_full_state(db: Session = Depends(get_db)):
    account = db.query(models.Account).first()
    if not account:
        account = models.Account()
        db.add(account)
        db.commit()
        db.refresh(account)
        
    controls = db.query(models.SystemControl).first()
    if not controls:
        controls = models.SystemControl()
        db.add(controls)
        db.commit()
        db.refresh(controls)

    models_list = db.query(models.AIModel).all()
    alerts_list = db.query(models.Alert).all()
    rules_list = db.query(models.SOARRule).all()
    baselines_list = db.query(models.VoiceBaseline).all()
    forensics_list = db.query(models.ForensicCase).all()
    sessions_list = db.query(models.CallSession).all()

    account_data = {
        "name": account.name,
        "email": account.email,
        "role": account.role,
        "org": account.org,
        "theme": account.theme,
        "notifEmail": account.notif_email,
        "notifSms": account.notif_sms,
        "notifDigest": account.notif_digest
    }

    controls_data = {
        "elevatedAlerts": controls.elevated_alerts,
        "autoCases": controls.auto_cases,
        "forceDrop": controls.force_drop
    }

    models_data = [{"id": m.id, "name": m.name, "sub": m.sub, "score": m.score} for m in models_list]
    alerts_data = [{"id": a.id, "title": a.title, "desc": a.desc, "time": a.time} for a in alerts_list]
    rules_data = [{"id": r.id, "name": r.name, "trigger": r.trigger, "action": r.action, "enabled": r.enabled} for r in rules_list]
    baselines_data = [{"id": b.id, "name": b.name, "speaker": b.speaker, "samples": b.samples, "status": b.status, "created": b.created} for b in baselines_list]
    
    forensics_data = []
    for c in forensics_list:
        notes_data = [{"text": n.text, "time": n.time} for n in c.notes]
        forensics_data.append({
            "id": c.id,
            "caller": c.caller,
            "date": c.date,
            "score": c.score,
            "status": c.status,
            "notes": notes_data
        })

    sessions_data = [{"caller": s.caller, "time": s.time, "score": s.score, "verdict": s.verdict} for s in sessions_list]

    return {
        "monitoring": controls.monitoring,
        "alertDismissed": controls.alert_dismissed,
        "account": account_data,
        "session": {"score": 0.18, "confidence": 91.4, "status": "low"},
        "models": models_data,
        "controls": controls_data,
        "alerts": alerts_data,
        "soarRules": rules_data,
        "baselines": baselines_data,
        "forensics": forensics_data,
        "sessions": sessions_data
    }

@router.put("/account")
def update_account(payload: schemas.AccountSchema, db: Session = Depends(get_db)):
    account = db.query(models.Account).first()
    if not account:
        account = models.Account()
        db.add(account)
    
    account.name = payload.name
    account.email = payload.email
    account.role = payload.role
    account.org = payload.org
    account.theme = payload.theme
    account.notif_email = payload.notifEmail
    account.notif_sms = payload.notifSms
    account.notif_digest = payload.notifDigest

    db.commit()
    return {"status": "ok"}

@router.put("/controls")
def update_controls(payload: schemas.ControlsSchema, db: Session = Depends(get_db)):
    controls = db.query(models.SystemControl).first()
    if not controls:
        controls = models.SystemControl()
        db.add(controls)

    controls.elevated_alerts = payload.elevatedAlerts
    controls.auto_cases = payload.autoCases
    controls.force_drop = payload.forceDrop

    db.commit()
    return {"status": "ok"}

@router.post("/monitoring/toggle")
def toggle_monitoring(payload: Optional[dict] = None, db: Session = Depends(get_db)):
    controls = db.query(models.SystemControl).first()
    if not controls:
        controls = models.SystemControl()
        db.add(controls)
    
    if payload and "monitoring" in payload:
        controls.monitoring = payload["monitoring"]
    else:
        controls.monitoring = not controls.monitoring

    db.commit()
    return {"monitoring": controls.monitoring}

@router.post("/alert/dismiss")
def dismiss_alert(db: Session = Depends(get_db)):
    controls = db.query(models.SystemControl).first()
    if not controls:
        controls = models.SystemControl()
        db.add(controls)
    
    controls.alert_dismissed = True
    db.commit()
    return {"alertDismissed": True}

@router.post("/reset")
def reset_database(db: Session = Depends(get_db)):
    from main import init_seed_data
    db.query(models.CaseNote).delete()
    db.query(models.ForensicCase).delete()
    db.query(models.VoiceBaseline).delete()
    db.query(models.SOARRule).delete()
    db.query(models.Alert).delete()
    db.query(models.AIModel).delete()
    db.query(models.SystemControl).delete()
    db.query(models.Account).delete()
    db.query(models.CallSession).delete()
    db.commit()

    init_seed_data(db)
    return {"status": "reset complete"}

# SOAR Rules Endpoints
@router.post("/soar-rules")
def create_soar_rule(payload: schemas.SOARRuleCreate, db: Session = Depends(get_db)):
    rule_id = "r" + uuid.uuid4().hex[:6]
    rule = models.SOARRule(
        id=rule_id,
        name=payload.name,
        trigger=payload.trigger,
        action=payload.action,
        enabled=True
    )
    db.add(rule)
    db.commit()
    return {"id": rule.id, "name": rule.name, "trigger": rule.trigger, "action": rule.action, "enabled": rule.enabled}

@router.put("/soar-rules/{rule_id}")
def update_soar_rule(rule_id: str, payload: dict = Body(...), db: Session = Depends(get_db)):
    rule = db.query(models.SOARRule).filter(models.SOARRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="SOAR rule not found")
    if "enabled" in payload:
        rule.enabled = payload["enabled"]
    if "name" in payload:
        rule.name = payload["name"]
    if "trigger" in payload:
        rule.trigger = payload["trigger"]
    if "action" in payload:
        rule.action = payload["action"]
    db.commit()
    return {"id": rule.id, "name": rule.name, "trigger": rule.trigger, "action": rule.action, "enabled": rule.enabled}

@router.delete("/soar-rules/{rule_id}")
def delete_soar_rule(rule_id: str, db: Session = Depends(get_db)):
    rule = db.query(models.SOARRule).filter(models.SOARRule.id == rule_id).first()
    if rule:
        db.delete(rule)
        db.commit()
    return {"status": "deleted"}

# Voice Baselines Endpoints
@router.post("/baselines")
def create_baseline(payload: schemas.VoiceBaselineCreate, db: Session = Depends(get_db)):
    b_id = "b" + uuid.uuid4().hex[:6]
    created_str = datetime.date.today().strftime("%b %d, %Y")
    baseline = models.VoiceBaseline(
        id=b_id,
        name=payload.name,
        speaker=payload.speaker,
        samples=1,
        status="processing",
        created=created_str
    )
    db.add(baseline)
    db.commit()
    return {"id": baseline.id, "name": baseline.name, "speaker": baseline.speaker, "samples": baseline.samples, "status": baseline.status, "created": baseline.created}

@router.put("/baselines/{baseline_id}")
def update_baseline(baseline_id: str, payload: dict = Body(...), db: Session = Depends(get_db)):
    baseline = db.query(models.VoiceBaseline).filter(models.VoiceBaseline.id == baseline_id).first()
    if not baseline:
        raise HTTPException(status_code=404, detail="Baseline not found")
    if "status" in payload:
        baseline.status = payload["status"]
    if "samples" in payload:
        baseline.samples = payload["samples"]
    db.commit()
    return {"id": baseline.id, "name": baseline.name, "speaker": baseline.speaker, "samples": baseline.samples, "status": baseline.status, "created": baseline.created}

@router.delete("/baselines/{baseline_id}")
def delete_baseline(baseline_id: str, db: Session = Depends(get_db)):
    baseline = db.query(models.VoiceBaseline).filter(models.VoiceBaseline.id == baseline_id).first()
    if baseline:
        db.delete(baseline)
        db.commit()
    return {"status": "deleted"}

# Forensics Cases Endpoints
@router.post("/forensics")
def create_forensic_case(payload: schemas.ForensicCaseCreate, db: Session = Depends(get_db)):
    c_id = payload.id or ("c" + uuid.uuid4().hex[:6])
    date_str = payload.date or datetime.datetime.now().strftime("%b %d, %Y · %H:%M")
    case = models.ForensicCase(
        id=c_id,
        caller=payload.caller,
        date=date_str,
        score=payload.score,
        status=payload.status or "open"
    )
    db.add(case)
    db.flush()

    for note in payload.notes:
        db.add(models.CaseNote(case_id=c_id, text=note.text, time=note.time))
    
    db.commit()
    return {"id": c_id, "status": "created"}

@router.post("/forensics/{case_id}/notes")
def add_case_note(case_id: str, payload: schemas.CaseNoteSchema, db: Session = Depends(get_db)):
    case = db.query(models.ForensicCase).filter(models.ForensicCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    note = models.CaseNote(case_id=case_id, text=payload.text, time=payload.time)
    db.add(note)
    db.commit()
    return {"text": note.text, "time": note.time}

@router.put("/forensics/{case_id}/status")
def toggle_case_status(case_id: str, payload: dict = Body(...), db: Session = Depends(get_db)):
    case = db.query(models.ForensicCase).filter(models.ForensicCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if "status" in payload:
        case.status = payload["status"]
    else:
        case.status = "resolved" if case.status == "open" else "open"
    db.commit()
    return {"id": case.id, "status": case.status}