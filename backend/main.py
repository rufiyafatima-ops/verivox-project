import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine, Base, SessionLocal
import models
from api import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="VeriVox API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_seed_data(db):
    if not db.query(models.Account).first():
        db.add(models.Account())
        db.add(models.SystemControl())
        
        models_data = [
            models.AIModel(id="aasist", name="AASIST attention", sub="Temporal + spectral", score=0.18),
            models.AIModel(id="ssl", name="SSL fusion", sub="WavLM · HuBERT", score=0.24),
            models.AIModel(id="bispectrum", name="Bispectrum", sub="Phase coupling", score=0.31),
            models.AIModel(id="acoustic", name="Acoustic baseline", sub="Cosine similarity", score=0.09)
        ]
        db.add_all(models_data)
        
        alerts = [
            models.Alert(id="a1", title="Elevated spoof score", desc="Call from +1 (628) 555-0110 scored 0.71", time="9m ago"),
            models.Alert(id="a2", title="New baseline verified", desc="Priya Nair baseline finished processing", time="1h ago"),
            models.Alert(id="a3", title="SOAR rule triggered", desc="Auto-create case fired for session #4471", time="3h ago")
        ]
        db.add_all(alerts)
        
        rules = [
            models.SOARRule(id="r1", name="Elevated risk notification", trigger=0.55, action="notify", enabled=True),
            models.SOARRule(id="r2", name="Auto-create investigation case", trigger=0.70, action="case", enabled=True),
            models.SOARRule(id="r3", name="Force connection drop", trigger=0.85, action="drop", enabled=True),
            models.SOARRule(id="r4", name="Slack security channel ping", trigger=0.60, action="slack", enabled=False)
        ]
        db.add_all(rules)
        
        baselines = [
            models.VoiceBaseline(id="b1", name="Jordan Davis", speaker="Internal · Security", samples=12, status="verified", created="Aug 14, 2026"),
            models.VoiceBaseline(id="b2", name="Priya Nair", speaker="Internal · Support", samples=9, status="verified", created="Aug 30, 2026"),
            models.VoiceBaseline(id="b3", name="Marcus Webb", speaker="Internal · Sales", samples=4, status="processing", created="Sep 9, 2026")
        ]
        db.add_all(baselines)
        
        c1 = models.ForensicCase(id="c1", caller="+1 (415) 555-0182", date="Sep 11, 2026 · 10:42", score=0.18, status="open")
        c2 = models.ForensicCase(id="c2", caller="+1 (628) 555-0110", date="Sep 11, 2026 · 09:01", score=0.71, status="open")
        c3 = models.ForensicCase(id="c3", caller="+1 (212) 555-0199", date="Sep 10, 2026 · 16:20", score=0.93, status="resolved")
        db.add_all([c1, c2, c3])
        db.flush()
        
        n1 = models.CaseNote(case_id="c2", text="Escalated to L2 for manual waveform review.", time="09:14")
        n2 = models.CaseNote(case_id="c3", text="Confirmed synthetic voice, blocked caller ID at PBX level.", time="16:40")
        db.add_all([n1, n2])
        
        sessions = [
            models.CallSession(caller="+1 (415) 555-0182", time="10:42 AM", score=0.18, verdict="low"),
            models.CallSession(caller="+1 (628) 555-0110", time="09:01 AM", score=0.71, verdict="high"),
            models.CallSession(caller="+1 (310) 555-0143", time="08:22 AM", score=0.29, verdict="low"),
            models.CallSession(caller="+1 (212) 555-0199", time="Yesterday", score=0.93, verdict="high"),
            models.CallSession(caller="+1 (773) 555-0127", time="Yesterday", score=0.44, verdict="mid"),
            models.CallSession(caller="+1 (206) 555-0166", time="2 days ago", score=0.12, verdict="low")
        ]
        db.add_all(sessions)
        db.commit()

db = SessionLocal()
init_seed_data(db)
db.close()

app.include_router(router)

# Mount static frontend files if directory exists
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)