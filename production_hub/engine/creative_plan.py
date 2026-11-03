"""Validated scene direction and actual TTS timing for the installed creative skills."""
import asyncio
import json
import math
import wave
import struct
from pathlib import Path

VISUALS = {"inbox", "message", "steps", "choices", "answer", "shop", "handoff", "cta"}
DIRECTED_RECIPES = {"directed_motion", "chat_story", "choice_quiz"}

def validate_plan(plan, lines):
    if not isinstance(plan, dict):
        raise ValueError("Directed recipes need a creative_plan object; use the supplied examples")
    for key in ("audience", "first_frame", "payoff"):
        if not isinstance(plan.get(key), str) or not 1 <= len(plan[key]) <= 500:
            raise ValueError(f"creative_plan.{key} is required (max 500 characters)")
    scenes = plan.get("scenes")
    if not isinstance(scenes, list) or len(scenes) != len(lines):
        raise ValueError("creative_plan.scenes must match the spoken scenes exactly")
    clean = {key: plan[key] for key in ("audience", "first_frame", "payoff")}
    clean["fictional"] = plan.get("fictional") is True
    clean["scenes"] = []
    for scene in scenes:
        if not isinstance(scene, dict) or scene.get("visual") not in VISUALS:
            raise ValueError("Choose a supported scene visual: " + ", ".join(sorted(VISUALS)))
        headline = scene.get("headline", "")
        if not isinstance(headline, str) or not headline or len(headline) > 90 or len(headline.split()) > 12:
            raise ValueError("Each headline needs 1–12 words, max 90 characters")
        result = {"visual": scene["visual"], "headline": headline}
        for key in ("label", "message", "reply", "option_a", "option_b"):
            value = scene.get(key, "")
            if not isinstance(value, str) or len(value) > 120:
                raise ValueError(f"Scene {key} must be text, max 120 characters")
            result[key] = value
        if result["visual"] in ("choices", "answer") and not (result["option_a"] and result["option_b"]):
            raise ValueError("Choice scenes need option_a and option_b")
        if result["visual"] == "answer":
            if scene.get("correct") not in ("A", "B"):
                raise ValueError("Answer scenes require correct=A or correct=B")
            result["correct"] = scene["correct"]
        clean["scenes"].append(result)
    return clean

async def timed_speech(text, target, voice):
    import edge_tts
    from .voice_engine import get_audio_duration
    target.parent.mkdir(parents=True, exist_ok=True)
    import hashlib
    cache = target.with_suffix('.json')
    key = hashlib.sha256((voice+'\n'+text).encode()).hexdigest()
    if target.exists() and cache.exists():
        saved = json.loads(cache.read_text(encoding='utf8'))
        if saved.get('key') == key and saved.get('words'):
            return get_audio_duration(str(target)), saved['words']
    communicator = edge_tts.Communicate(text, voice=voice, rate="+0%", boundary="WordBoundary", connect_timeout=15, receive_timeout=40)
    words = []
    with open(target, "wb") as audio:
        async for chunk in communicator.stream():
            if chunk["type"] == "audio":
                audio.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                words.append({"text": chunk["text"], "start": chunk["offset"] / 10_000_000,
                              "end": (chunk["offset"] + chunk["duration"]) / 10_000_000})
    duration = get_audio_duration(str(target))
    if not words:
        raise ValueError("Voice provider returned no word timestamps; refusing guessed captions")
    if any(word["end"] > duration + 0.3 for word in words):
        raise ValueError("Voice timing exceeds the generated audio")
    cache.write_text(json.dumps({'key': key, 'words': words}, ensure_ascii=False), encoding='utf8')
    return duration, words

def arrange_timeline(durations, words, audio_paths, total_seconds, fps=30):
    # Keep first spoken word early; preserve every audio tail and a readable hold.
    minimum = [max(3.0, duration + 0.4) for duration in durations]
    if sum(minimum) > total_seconds:
        raise ValueError(f"Narration needs at least {math.ceil(sum(minimum))}s; shorten copy or increase duration")
    spare = (total_seconds - sum(minimum)) / len(minimum)
    cursor = 0
    timeline = []
    for index, seconds in enumerate(minimum):
        end = round((sum(minimum[:index + 1]) + spare * (index + 1)) * fps)
        timeline.append({"from": cursor, "duration": end - cursor, "audio": audio_paths[index], "words": words[index]})
        cursor = end
    timeline[-1]["duration"] = round(total_seconds * fps) - timeline[-1]["from"]
    return timeline

def create_soundkit(folder):
    """Original deterministic percussion/tones; no stock track or external download."""
    folder.mkdir(parents=True, exist_ok=True)
    rate = 22050
    for name, seconds in (("pop", .18), ("sweep", .28), ("bed", 32.0)):
        target = folder / (name + ".wav")
        if target.exists():
            continue
        with wave.open(str(target), "wb") as audio:
            audio.setnchannels(1)
            audio.setsampwidth(2)
            audio.setframerate(rate)
            data = bytearray()
            for index in range(round(seconds * rate)):
                t = index / rate
                if name == "pop":
                    value = math.sin(2 * math.pi * (620 * t - 900 * t * t)) * math.exp(-t * 28) * .4
                elif name == "sweep":
                    value = math.sin(2 * math.pi * (220 * t + 1800 * t * t)) * math.sin(math.pi * t / seconds) ** 2 * .18
                else:
                    beat = t % .5
                    kick = math.sin(2 * math.pi * 64 * beat) * math.exp(-beat * 38) * .19
                    tick = math.sin(2 * math.pi * 1200 * beat) * math.exp(-beat * 110) * .035
                    pad = (math.sin(2 * math.pi * 220 * t) + math.sin(2 * math.pi * 330 * t)) * .018
                    value = (kick + tick + pad) * min(1, t / .15, (seconds - t) / .3)
                data.extend(struct.pack('<h', round(max(-1, min(1, value)) * 32767)))
            audio.writeframes(data)

def write_subtitles(timeline, folder, fps=30):
    def stamp(seconds):
        value=round(seconds*1000)
        hours,remainder=divmod(value,3_600_000)
        minutes,remainder=divmod(remainder,60_000)
        whole,milliseconds=divmod(remainder,1000)
        return f'{hours:02}:{minutes:02}:{whole:02},{milliseconds:03}'
    captions=[]
    global_words=[]
    for scene in timeline:
        offset=scene['from']/fps
        for word in scene['words']:
            global_words.append({'text':word['text'],'start':offset+word['start'],'end':offset+word['end']})
        for index in range(0,len(scene['words']),4):
            group=scene['words'][index:index+4]
            captions.append(f"{len(captions)+1}\n{stamp(offset+group[0]['start'])} --> {stamp(offset+group[-1]['end'])}\n{' '.join(word['text'] for word in group)}\n")
    (folder/'subtitles.srt').write_text('\n'.join(captions),encoding='utf8')
    (folder/'words.json').write_text(json.dumps(global_words,ensure_ascii=False,indent=2),encoding='utf8')

def build_directed_assets(job, folder, public):
    payload = job['payload']
    plan = validate_plan(payload['creative_plan'], payload['scenes'])
    for font in ('NotoSansDevanagari-Regular.ttf','NotoSansDevanagari-Bold.ttf'):
        if not (public/'factory-fonts'/font).is_file():
            raise ValueError('Local Hindi font assets missing; complete the directed recipe font setup first')
    durations, words, audio_paths = [], [], []
    if payload['mode'] == 'voice':
        async def build():
            for index, text in enumerate(payload['scenes']):
                relative = f"factory-audio/{job['id']}/scene-{index}.mp3"
                target = public / relative
                seconds, tokens = await asyncio.wait_for(timed_speech(text, target, payload['voice']), timeout=75)
                durations.append(seconds)
                words.append(tokens)
                audio_paths.append(relative)
        asyncio.run(build())
    else:
        durations = [max(2.5, len(text.split()) / 2.6) for text in payload['scenes']]
        words = [[] for _ in durations]
        audio_paths = [None for _ in durations]
    timeline = arrange_timeline(durations, words, audio_paths, payload['duration'])
    (folder/'timing.json').write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding='utf8')
    (folder/'creative-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
    write_subtitles(timeline,folder)
    create_soundkit(public/'factory-sfx')
    return {"creative_plan": plan, "directed_timeline": timeline, "soundkit": True, "creative_style": payload['recipe']}
