import asyncio
import json
import math
import os
import re
import subprocess
import edge_tts

# 45-second high-impact, fast-cut, authoritative B2B pitch
SCENES = [
    {
        "id": "s01",
        "chip": "🚨 DENTIST ALERT",
        "line1": "Dentist हैं?",
        "line2": "हर महीने ₹2 लाख का नुकसान!",
        "accent": "#FF2E63",
        "voice_text": "अगर आप एक डेंटिस्ट हैं, तो सच सुनिए! हर महीने आपके एरिया के 50 मरीज़ सिर्फ एक गलती की वजह से दूसरे क्लिनिक्स चले जाते हैं!",
        "subtitle": "Agar aap Dentist hain toh har mahine 50 patients dusre clinics ja rahe hain!",
        "highlights": ["Dentist", "50 patients", "dusre clinics"]
    },
    {
        "id": "s02",
        "chip": "🔍 GOOGLE SEARCH",
        "line1": "सड़क पर बोर्ड नहीं,",
        "line2": "Google पर सर्च करते हैं!",
        "accent": "#00F2FE",
        "voice_text": "दाँत में दर्द होने पर कोई बोर्ड नहीं देखता, सीधे Google करता है: Best Dentist Near Me! और अगर आपकी वेबसाइट नहीं है, तो मरीज़ तुरंत छूट जाता है!",
        "subtitle": "Dard hone par log seedhe Google karte hain Best Dentist Near Me! Website nahi toh patient gaya!",
        "highlights": ["Google", "Best Dentist", "Website nahi"]
    },
    {
        "id": "s03",
        "chip": "⚡ 1-CLICK BOOKING",
        "line1": "आपकी वेबसाइट पर,",
        "line2": "WhatsApp 1-Click बुकिंग!",
        "accent": "#10B981",
        "voice_text": "आपकी प्रीमियम वेबसाइट पर होता है 1-Click डायरेक्ट WhatsApp अपॉइंटमेंट बटन और बिफोर-आफ्टर स्माइल मेकओवर गैलरी, जो 100% ट्रस्ट बनाती है!",
        "subtitle": "Aapki website par 1-Click direct WhatsApp appointment aur Before-After Smile gallery!",
        "highlights": ["1-Click", "WhatsApp", "Before-After", "Smile"]
    },
    {
        "id": "s04",
        "chip": "💰 10X PROFIT MATHS",
        "line1": "महीने में सिर्फ 2 मरीज़,",
        "line2": "और पूरा खर्चा 100% वसूल!",
        "accent": "#F59E0B",
        "voice_text": "सीधा गणित: महीने में सिर्फ 2 नए रूट-कैनाल या 1 इंप्लांट का मरीज़ आया, तो ₹30,000 का मुनाफ़ा! यानी वेबसाइट पहले ही महीने में बिल्कुल फ्री!",
        "subtitle": "Seedha maths: mahine me bas 2 Root Canals ya 1 Implant aaya toh 30,000 profit! Website 100% free!",
        "highlights": ["Seedha maths", "Root Canals", "Implant", "30,000 profit", "100% free"]
    },
    {
        "id": "s05",
        "chip": "📞 DOCTOR SPECIAL OFFER",
        "line1": "अपनी क्लिनिक को ब्रांड बनाएं,",
        "line2": "Mohit Jain: 6263879076",
        "accent": "#10B981",
        "voice_text": "तो डॉक्टर साहब, अपने शहर में नंबर-1 क्लिनिक बनिए! अपनी क्लिनिक का फ्री लाइव डेमो देखने के लिए अभी कॉल या WhatsApp करें: मोहित जैन - 6263879076!",
        "subtitle": "Apne shehar me No.1 Clinic baniye! Free demo ke liye abhi call ya WhatsApp karein: Mohit Jain 6263879076!",
        "highlights": ["No.1 Clinic", "Free demo", "Mohit Jain", "6263879076"]
    }
]

def get_audio_duration(file_path):
    cmd = ["ffmpeg", "-i", file_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", result.stderr)
    if match:
        hours, minutes, seconds = map(float, match.groups())
        return hours * 3600 + minutes * 60 + seconds
    return 8.0

async def generate_fast():
    base_dir = os.path.abspath("hindi-reel")
    audio_dir = os.path.join(base_dir, "public", "audio")
    data_dir = os.path.join(base_dir, "src", "data")
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    
    script_data = []
    total_frames = 0
    
    for scene in SCENES:
        scene_id = scene["id"]
        audio_path = os.path.join(audio_dir, f"{scene_id}.mp3")
        # Energetic, punchy, fast sales rate +18%
        communicate = edge_tts.Communicate(scene["voice_text"], voice="hi-IN-MadhurNeural", rate="+18%", pitch="+2Hz")
        await communicate.save(audio_path)
        
        duration = get_audio_duration(audio_path)
        frames = math.ceil(duration * 30) + 6
        total_frames += frames
        
        scene_entry = {
            "id": scene_id,
            "chip": scene["chip"],
            "line1": scene["line1"],
            "line2": scene["line2"],
            "accent": scene["accent"],
            "subtitle": scene["subtitle"],
            "highlights": scene["highlights"],
            "audio": f"audio/{scene_id}.mp3",
            "durationSec": duration,
            "frames": frames
        }
        script_data.append(scene_entry)
        print(f"{scene_id}: {duration:.2f}s -> {frames} frames")
        
    script_json_path = os.path.join(data_dir, "script.json")
    with open(script_json_path, "w", encoding="utf-8") as f:
        json.dump(script_data, f, indent=2, ensure_ascii=False)
        
    print(f"\nTotal 45s Reel Duration: {total_frames / 30:.1f}s ({total_frames} frames @ 30fps)")

if __name__ == "__main__":
    asyncio.run(generate_fast())
