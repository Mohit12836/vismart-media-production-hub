import asyncio
import json
import math
import os
import re
import subprocess
import edge_tts

BEATS_SCRIPT = [
    {
        "id": "b01",
        "voice": "क्या आपके क्लिनिक में आज भी खाली स्लॉट हैं?",
        "emotion": {
            "primary": "concern",
            "secondary": "curiosity",
            "intensity": 0.55,
            "confidence": "human-verified"
        },
        "viewer_goal": "समस्या पहचानें",
        "visual": "खाली dental clinic chair और शांत reception का original vector scene",
        "shot": "wide to medium push-in",
        "motion": "slow-push",
        "caption": "खाली स्लॉट?",
        "audio_cue": "soft room tone and brief pause",
        "asset_strategy": "original-svg",
        "evidence": "illustrative, not real clinic footage"
    },
    {
        "id": "b02",
        "voice": "शायद मरीज ऑनलाइन खोज रहे हैं, लेकिन आपकी जानकारी अधूरी है।",
        "emotion": {
            "primary": "curiosity",
            "secondary": "concern",
            "intensity": 0.5,
            "confidence": "human-verified"
        },
        "viewer_goal": "समस्या का कारण समझें",
        "visual": "मोबाइल search UI पर missing information mockup; no false Google branding",
        "shot": "screen close-up",
        "motion": "ui-reveal",
        "caption": "जानकारी अधूरी है",
        "audio_cue": "subtle tap then lower music",
        "asset_strategy": "react-svg",
        "evidence": "illustrative interface"
    },
    {
        "id": "b03",
        "voice": "जब मरीज आसानी से आपकी सेवाएँ और समय देख पाते हैं, बुकिंग करना सरल हो जाता है।",
        "emotion": {
            "primary": "relief",
            "secondary": "clarity",
            "intensity": 0.65,
            "confidence": "human-verified"
        },
        "viewer_goal": "solution समझें",
        "visual": "services + available slots visual sequence with confirmed fictional content",
        "shot": "interface walkthrough",
        "motion": "guided-reveal",
        "caption": "आसान बुकिंग",
        "audio_cue": "soft resolution accent",
        "asset_strategy": "react-svg",
        "evidence": "conceptual demo"
    },
    {
        "id": "b04",
        "voice": "एक साफ वेबसाइट और आसान WhatsApp संपर्क इस अनुभव को बेहतर बना सकते हैं।",
        "emotion": {
            "primary": "confidence",
            "secondary": "hope",
            "intensity": 0.68,
            "confidence": "human-verified"
        },
        "viewer_goal": "अगला कदम समझें",
        "visual": "एक साफ website mockup और contact CTA; no fabricated outcomes",
        "shot": "hero with split focal region",
        "motion": "parallax",
        "caption": "वेबसाइट + WhatsApp",
        "audio_cue": "gentle upbeat bed",
        "asset_strategy": "react-svg",
        "evidence": "proposed solution, not guaranteed ROI"
    },
    {
        "id": "b05",
        "voice": "अपने क्लिनिक की प्रीमियम वेबसाइट बनवाने के लिए संपर्क करें: मोहित जैन - 6263879076!",
        "emotion": {
            "primary": "confidence",
            "secondary": "enthusiasm",
            "intensity": 0.85,
            "confidence": "human-verified"
        },
        "viewer_goal": "मोहित जैन से संपर्क करें",
        "visual": "MOHIT JAIN calling card, 6263879076, direct call & WhatsApp",
        "shot": "center VIP card pop",
        "motion": "spring-reveal",
        "caption": "Mohit Jain: 6263879076",
        "audio_cue": "triumphant resolve chime",
        "asset_strategy": "react-svg",
        "evidence": "direct creator contact"
    }
]

def get_audio_duration(file_path):
    cmd = ["ffmpeg", "-i", file_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", result.stderr)
    if match:
        hours, minutes, seconds = map(float, match.groups())
        return hours * 3600 + minutes * 60 + seconds
    return 4.0

async def main():
    base_dir = os.path.abspath("vismart-unified-creative-director")
    public_audio = os.path.join(base_dir, "remotion", "public", "audio")
    # Also in hindi-reel public audio so remotion dev server can access it
    hindi_reel_audio = os.path.join("hindi-reel", "public", "audio")
    os.makedirs(public_audio, exist_ok=True)
    os.makedirs(hindi_reel_audio, exist_ok=True)

    beats_output = []
    current_time = 0.0

    for item in BEATS_SCRIPT:
        beat_id = item["id"]
        filename = f"vismart_{beat_id}.mp3"
        dest1 = os.path.join(public_audio, filename)
        dest2 = os.path.join(hindi_reel_audio, filename)

        # Generate audio with edge-tts in professional warm Hindi tone
        com = edge_tts.Communicate(item["voice"], voice="hi-IN-MadhurNeural", rate="+6%")
        await com.save(dest1)
        # copy to dest2
        with open(dest1, "rb") as fsrc, open(dest2, "wb") as fdst:
            fdst.write(fsrc.read())

        duration = get_audio_duration(dest1)
        # add 0.5s breathing padding per beat
        beat_dur = round(duration + 0.45, 2)
        end_time = round(current_time + beat_dur, 2)

        beat_entry = {
            "id": beat_id,
            "start": current_time,
            "end": end_time,
            "voice": item["voice"],
            "emotion": item["emotion"],
            "viewer_goal": item["viewer_goal"],
            "visual": item["visual"],
            "shot": item["shot"],
            "motion": item["motion"],
            "caption": item["caption"],
            "audio": f"audio/{filename}",
            "asset_strategy": item["asset_strategy"],
            "evidence": item["evidence"]
        }
        beats_output.append(beat_entry)
        print(f"Beat {beat_id}: {current_time}s -> {end_time}s (dur: {duration:.2f}s)")
        current_time = end_time

    plan_data = {
        "meta": {
            "title": "Dentist Clinic — Vismart Creative Director",
            "fps": 30,
            "width": 720,
            "height": 1280,
            "language": "hi",
            "duration": current_time,
            "audio_file": "audio/bg.mp3",
            "visual_cost_policy": "zero-paid",
            "word_alignment": "verified",
            "genre": "local-business-ad"
        },
        "beats": beats_output
    }

    plan_path = os.path.join(base_dir, "examples", "dentist-scene-plan.json")
    with open(plan_path, "w", encoding="utf-8") as f:
        json.dump(plan_data, f, indent=2, ensure_ascii=False)

    print(f"\nUpdated {plan_path} with {len(beats_output)} beats. Total duration: {current_time}s")

if __name__ == "__main__":
    asyncio.run(main())
