import subprocess
import json
from transformers import pipeline
import whisper

# --- Setup (runs once when the module is imported) ---
deepfake_detector = pipeline("audio-classification", model="MelodyMachine/Deepfake-audio-detection-V2")
whisper_model = whisper.load_model("base")

PHONEINFOGA_PATH = "phoneinfoga/phoneinfoga.exe"  # adjust path as needed

# --- Feature 1: Deepfake detection ---
def detect_deepfake(audio_path):
    result = deepfake_detector(audio_path)
    fake_score = next((r["score"] for r in result if r["label"] == "fake"), 0)
    real_score = next((r["score"] for r in result if r["label"] == "real"), 0)
    return {"fake_score": round(fake_score * 100, 2), "real_score": round(real_score * 100, 2)}

# --- Feature 2: Transcription ---
def transcribe_audio(audio_path):
    result = whisper_model.transcribe(audio_path)
    return {"text": result["text"], "language": result["language"]}

# --- Feature 3: Scam phrase detection ---
def check_scam_content(transcript_text):
    scam_keywords = ["send money", "gift card", "wire transfer", "don't tell anyone",
                      "urgent", "verify your account", "bank details", "otp"]
    text_lower = transcript_text.lower()
    matches = [kw for kw in scam_keywords if kw in text_lower]
    return {"scam_detected": len(matches) > 0, "matched_phrases": matches}

# --- Feature 4: Phone number OSINT check ---
def check_phone_number(phone_number):
    result = subprocess.run(
        [PHONEINFOGA_PATH, "scan", "-n", phone_number, "-o", "json"],
        capture_output=True, text=True
    )
    try:
        return json.loads(result.stdout)
    except:
        return {"raw_output": result.stdout}

# --- Combined analysis (the "main" function she'd call) ---
def analyze_call(audio_path, phone_number=None):
    deepfake_result = detect_deepfake(audio_path)
    transcript_result = transcribe_audio(audio_path)
    scam_result = check_scam_content(transcript_result["text"])
    phone_result = check_phone_number(phone_number) if phone_number else None

    return {
        "deepfake": deepfake_result,
        "transcript": transcript_result,
        "scam_check": scam_result,
        "phone_check": phone_result
    }

# --- Test it standalone ---
if __name__ == "__main__":
    result = analyze_call("test_audio_fixed.wav")
    print(json.dumps(result, indent=2))