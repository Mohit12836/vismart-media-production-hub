# 🌐 Vismart Production Hub — VPS Setup Guide (हिंदी गाइड)

यह गाइड आपके **Linux VPS (Ubuntu 22.04 / 24.04)** पर पूरे वीडियो और ऑडियो ऑटोमेशन सिस्टम को 1-क्लिक में लाइव करने के लिए है।

---

## ⚡ 1. VPS से कनेक्ट कैसे करें (Connect via SSH)
अपने टर्मिनल या PowerShell में यह कमांड चलाएं:
```bash
ssh root@YOUR_VPS_IP
```

---

## 🚀 2. ऑटोमेशन सेटअप रन करें (1-Command Install)
VPS में कनेक्ट होने के बाद सिर्फ यह एक कमांड पेस्ट करें:
```bash
bash /opt/media_hub/production_hub/vps/deploy_vps.sh
```

यह स्क्रिप्ट अपने आप:
- **FFmpeg 9+** और **Chromium** इंस्टॉल करेगी।
- **Node.js 22 LTS** और **Remotion** रेंडर इंजन सेट करेगी।
- **Python Edge-TTS** (100% Free Unlimited Hindi/English Voices) तैयार करेगी।
- **Google Devanagari Fonts** लोड करेगी।
- **Daily Cron Job** सेट कर देगी जो रोज़ तय समय पर अपने आप वीडियो रेंडर करेगा।

---

## 🎬 3. वेब डैशबोर्ड से 100+ वीडियो बल्क फैक्ट्री चलाना (Recommended):
ब्राउज़र में खोलें:
```
http://YOUR_VPS_IP:5000
```
- **Studio Tab:** 1-क्लिक में सिंगल कस्टम वीडियो, वॉयस प्रीव्यू, पिच/टोन स्लाइडर्स।
- **Bulk Factory Tab:** 10, 50, या 100 टॉपिक्स एक साथ डालें, `9:16 Reels` + `16:9 Long Videos` + `Stories` चेक करें, और "Launch 100+ Batch Factory" दबा दें!
- बैकग्राउंड वर्कर बिना रुके लगातार रेंडर करता रहेगा और लाइव प्रोग्रेस ओडोमीटर पर दिखाता रहेगा।

---

## 💻 4. CLI से नई वीडियो कैसे बनाएं?

### तरीका 1: 14s Silent Kinetic रील बनाना:
```bash
python3 /opt/media_hub/production_hub/master_generator.py --style silent_kinetic --mode silent
```

### तरीका 2: 16:9 Long Landscape यूट्यूब वीडियो बनाना:
```bash
python3 /opt/media_hub/production_hub/master_generator.py --style long_explainer --format long
```

### तरीका 3: अपनी खुद की ऑडियो फ़ाइल देकर वीडियो बनाना:
```bash
python3 /opt/media_hub/production_hub/master_generator.py --audio /path/to/my_recording.mp3 --style vismart
```

---

## 📂 5. आउटपुट कहाँ मिलेगा?
सभी तैयार वीडियो और कवर्स ऑटो-कैटलॉग होकर इन फ़ोल्डर्स में सुरक्षित सेव होते हैं:
```bash
/opt/media_hub/production_hub/outputs/reels/    # 📱 9:16 Vertical Reels / Shorts
/opt/media_hub/production_hub/outputs/long/     # 📺 16:9 Landscape YouTube Videos
/opt/media_hub/production_hub/outputs/stories/  # ⚡ 9:16 Micro Stories / Status
```
वहाँ से आप इन्हें सीधे YouTube Shorts, Instagram Reels, या WhatsApp पर पब्लिश कर सकते हैं!
