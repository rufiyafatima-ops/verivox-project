from transformers import pipeline

detector = pipeline("audio-classification", model="MelodyMachine/Deepfake-audio-detection-V2")

def detect_deepfake(audio_path):
    result = detector(audio_path)
    fake_score = next((r["score"] for r in result if r["label"] == "fake"), 0)
    real_score = next((r["score"] for r in result if r["label"] == "real"), 0)
    return {
        "fake_score": round(fake_score * 100, 2),
        "real_score": round(real_score * 100, 2),
        "raw_result": result
    }

# Only runs when you test this file directly — won't run when your friend imports it
if __name__ == "__main__":
    output = detect_deepfake("test_audio_fixed.wav")
    print("Result:", output)