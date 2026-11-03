import asyncio
import json
import os
import edge_tts

SCENES = [
    {
        "id": "s01",
        "chip": "DENTIST ALERT ⚠️",
        "line1": "Dentist हैं?",
        "line2": "₹2 लाख का नुकसान हर महीने!",
        "accent": "#FF2E63",
        "visual": "alert-loss",
        "mascot": "surprise",
        "voice_text": "अगर आप एक डेंटिस्ट हैं, तो सच सुनिए! हर महीने आपके एरिया के चालीस से पचास मरीज़ आपकी क्लिनिक के बजाय दूसरे डेंटिस्ट के पास जा रहे हैं, जिससे आपका सीधा दो से तीन लाख रुपए का नुकसान हो रहा है!",
        "subtitle": "Agar aap Dentist hain toh har mahine 40-50 patients dusre clinics ja rahe hain aur seedha 2-3 lakh ka loss ho raha hai!",
        "highlights": ["Dentist", "40-50 patients", "2-3 lakh", "loss"]
    },
    {
        "id": "s02",
        "chip": "GOOGLE SEARCH 🔍",
        "line1": "सड़क पर बोर्ड नहीं,",
        "line2": "Google पर सर्च करते हैं!",
        "accent": "#0891B2",
        "visual": "google-search",
        "mascot": "point",
        "voice_text": "आज का सच यह है कि जब किसी के दाँत में दर्द होता है, तो वो सड़क पर होर्डिंग नहीं देखता। वो सीधे अपने फ़ोन पर Google करता है: Best Dentist near me! और अगर वहाँ आपकी वेबसाइट नहीं दिखी, तो मरीज़ तुरंत अगले डेंटिस्ट के पास चला जाता है!",
        "subtitle": "Daant me dard hone par log board nahi, Google par 'Best Dentist near me' search karte hain! Website na milne par agle doctor ke paas chale jaate hain!",
        "highlights": ["Google", "Best Dentist", "website", "agle doctor"]
    },
    {
        "id": "s03",
        "chip": "JUSTDIAL TRAP 🚫",
        "line1": "Justdial & Practo?",
        "line2": "वो कॉम्पिटिटर को दिखाते हैं!",
        "accent": "#EF4444",
        "visual": "competitor-trap",
        "mascot": "think",
        "voice_text": "कई डॉक्टर्स सोचते हैं कि Practo या Justdial काफी है। लेकिन कड़वी सच्चाई यह है कि आप उन्हें हज़ारों रुपए देते हैं, और वो आपके ही नाम के नीचे दस और डेंटिस्ट्स के नंबर दिखा देते हैं! आपकी अपनी वेबसाइट आपकी प्राइवेट डिजिटल क्लिनिक होती है!",
        "subtitle": "Practo aur Justdial par aap paise dete ho aur wo aapke neeche 10 aur competitors dikhate hain! Lekin aapki apni website aapka private digital clinic hai!",
        "highlights": ["Practo", "Justdial", "competitors", "private digital clinic"]
    },
    {
        "id": "s04",
        "chip": "5 SUPER FEATURES 💎",
        "line1": "आपकी वेबसाइट में,",
        "line2": "ये 3 जादुई फीचर्स होंगे!",
        "accent": "#10B981",
        "visual": "three-features",
        "mascot": "explain",
        "voice_text": "हम जो वेबसाइट आपके क्लिनिक के लिए बनाते हैं, उसमें होते हैं तीन सबसे असरदार फीचर्स: पहला, वन क्लिक डायरेक्ट WhatsApp अपॉइंटमेंट बटन! दूसरा, बिफोर और आफ्टर स्माइल मेकओवर गैलरी! और तीसरा, लाइव Google Maps नेविगेशन ताकि मरीज़ सीधे आपकी क्लिनिक पहुंचे!",
        "subtitle": "Hamari website me hote hain: 1-Click WhatsApp booking, Before-After Smile makeover gallery, aur live Google Maps navigation!",
        "highlights": ["WhatsApp booking", "Before-After", "Smile makeover", "Google Maps"]
    },
    {
        "id": "s05",
        "chip": "24/7 AUTOPILOT ⏰",
        "line1": "क्लिनिक बंद,",
        "line2": "फिर भी बुकिंग 24 घंटे!",
        "accent": "#7C3AED",
        "visual": "night-booking",
        "mascot": "explain",
        "voice_text": "सोचिए, रात के ग्यारह बजे जब आपकी क्लिनिक बंद होती है और रिसेप्शनिस्ट घर पर सो रहा होता है, तब भी इमरजेंसी में परेशान मरीज़ आपकी वेबसाइट खोलकर अगली सुबह दस बजे का अपॉइंटमेंट बुक कर लेता है! आपकी वेबसाइट एक ऐसा डिजिटल कर्मचारी है जो कभी छुट्टी नहीं लेता!",
        "subtitle": "Raat ke 11 baje jab clinic band hoti hai tab bhi patients subah ka appointment book kar lete hain! Website ek aisi receptionist hai jo kabhi chhutti nahi leti!",
        "highlights": ["clinic band", "appointment book", "digital receptionist", "kabhi chhutti nahi"]
    },
    {
        "id": "s06",
        "chip": "10X ROI MATHS 💰",
        "line1": "पहले ही महीने में,",
        "line2": "पूरा खर्चा 100% वसूल!",
        "accent": "#F59E0B",
        "visual": "roi-calc",
        "mascot": "point",
        "voice_text": "अब ज़रा सीधा गणित समझिए! वेबसाइट बनवाने का खर्च सिर्फ एक बार का होता है। अगर वेबसाइट की वजह से पूरे महीने में सिर्फ दो नए रूट-कैनाल या केवल एक डेंटल इंप्लांट का केस भी आ गया, तो पच्चीस से तीस हज़ार रुपए का मुनाफ़ा सीधे आपकी जेब में! यानी पहले ही महीने में वेबसाइट बिल्कुल फ़्री!",
        "subtitle": "Seedha maths samjhiye: pure mahine me bas 2 Root Canals ya 1 Dental Implant ka case aaya, toh website ka pura kharcha pehle hi mahine me 100% vasool!",
        "highlights": ["Seedha maths", "Root Canals", "Dental Implant", "100% vasool"]
    },
    {
        "id": "s07",
        "chip": "TRUST & SPEED ⚡",
        "line1": "Mohit Jain ही क्यों?",
        "line2": "Super Fast, SEO & Security!",
        "accent": "#0891B2",
        "visual": "tech-specs",
        "mascot": "explain",
        "voice_text": "और हम आपको सिर्फ वेबसाइट नहीं, एक पूरा ब्रांड सॉल्यूशन देते हैं! सुपर-फास्ट एक सेकंड लोडिंग, हंड्रेड परसेंट मोबाइल रेस्पॉन्सिव डिज़ाइन, Google SEO सेटअप और पूरे एक साल का फ्री टेक्निकल सपोर्ट, ताकि आपको कोई सिरदर्द न हो!",
        "subtitle": "Hum dete hain: Super-fast loading, 100% mobile responsive design, Google SEO setup aur pure 1 saal ka free maintenance support!",
        "highlights": ["Super-fast loading", "mobile responsive", "Google SEO", "free maintenance"]
    },
    {
        "id": "s08",
        "chip": "DOCTOR OFFER 📞",
        "line1": "अपनी क्लिनिक को ब्रांड बनाएं,",
        "line2": "Mohit Jain: 6263879076",
        "accent": "#10B981",
        "visual": "cta-card",
        "mascot": "point",
        "voice_text": "तो डॉक्टर साहब, अपने शहर में नंबर वन क्लिनिक बनिए और आज ही अपने क्लिनिक का फ्री लाइव डेमो देखने के लिए कॉल या WhatsApp करें: मोहित जैन - छह दो छह तीन आठ सात नौ शून्य सात छह! अभी कॉल करें, ऑफर सीमित समय के लिए है!",
        "subtitle": "Apne shehar me No.1 Clinic baniye! Free live demo dekhne ke liye abhi call ya WhatsApp karein: Mohit Jain 6263879076!",
        "highlights": ["No.1 Clinic", "Free live demo", "Mohit Jain", "6263879076"]
    }
]

async def generate_scene_audio(scene, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    audio_file = os.path.join(out_dir, f"{scene['id']}.mp3")
    captions_file = os.path.join(out_dir, f"{scene['id']}_captions.json")
    
    communicate = edge_tts.Communicate(scene['voice_text'], voice="hi-IN-MadhurNeural", rate="+6%")
    submaker = edge_tts.SubMaker()
    
    with open(audio_file, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
                
    # Also get duration with ffprobe
    return audio_file

async def main():
    audio_dir = os.path.join("hindi-reel", "public", "audio")
    os.makedirs(audio_dir, exist_ok=True)
    
    print("Generating audio for all scenes...")
    for scene in SCENES:
        print(f"Generating {scene['id']}...")
        await generate_scene_audio(scene, audio_dir)
    print("All audio files generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
