#!/usr/bin/env python3
"""
Master Modular Media Production Engine
Supports:
1. User-Uploaded Voice Audio OR Zero-Cost Edge-TTS Voiceover
2. Free AI Images (Pollinations AI) OR Remotion Coded Vector SVG
3. 1-Click MP4 Render & Thumbnail Generation
4. 100% Linux VPS & Windows Compatible
"""

import argparse
import asyncio
import os
import sys
import json
import shutil

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Import engine modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from engine.voice_engine import get_audio_duration, generate_speech, process_uploaded_audio
from engine.image_engine import generate_ai_image
from engine.remotion_engine import render_remotion_composition, render_cover_thumbnail

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
REMOTION_DIR = os.path.join(PROJECT_ROOT, "hindi-reel")

async def run_pipeline(args):
    print("=======================================================")
    print("🚀 VISMART MODULAR PRODUCTION HUB — STARTING PIPELINE")
    print("=======================================================")

    output_dir = os.path.join(BASE_DIR, "outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    # Categorized output directory
    if args.style == "long_explainer":
        cat_dir = os.path.join(output_dir, "long")
    elif getattr(args, "format", "reel") == "story":
        cat_dir = os.path.join(output_dir, "stories")
    else:
        cat_dir = os.path.join(output_dir, "reels")
    os.makedirs(cat_dir, exist_ok=True)

    out_mp4 = args.output or os.path.join(cat_dir, f"video_{int(os.times().elapsed)}.mp4")

    # Step 1: Voice Setup (Only if mode is not silent)
    if args.mode == "silent" or args.style == "silent_kinetic":
        print("[Step 1] Mode: SILENT KINETIC (No voiceover required, using background beat + SFX)")
        target_audio = None
    elif args.audio:
        target_audio = os.path.join(REMOTION_DIR, "public", "audio", "voiceover.mp3")
        vismart_public_audio = os.path.join(PROJECT_ROOT, "vismart-unified-creative-director", "remotion", "public", "audio", "voiceover.mp3")
        print(f"[Step 1] Using Uploaded Audio: {args.audio}")
        duration = process_uploaded_audio(args.audio, target_audio)
        shutil.copyfile(target_audio, vismart_public_audio)
        print(f"[Step 1 Complete] Voice Duration: {duration}s")
    else:
        target_audio = os.path.join(REMOTION_DIR, "public", "audio", "voiceover.mp3")
        vismart_public_audio = os.path.join(PROJECT_ROOT, "vismart-unified-creative-director", "remotion", "public", "audio", "voiceover.mp3")
        text = args.text or "क्या आप अपने बिज़नेस के लिए एक प्रोफेशनल वेबसाइट बनवाना चाहते हैं? अभी संपर्क करें Vismart Studio!"
        voice = args.voice or "hi-IN-MadhurNeural"
        pitch = getattr(args, "pitch", "+0Hz") or "+0Hz"
        print(f"[Step 1] Generating AI Voiceover: {text[:45]}... (rate: {args.rate}, pitch: {pitch})")
        duration = await generate_speech(text, target_audio, voice=voice, rate=args.rate, pitch=pitch)
        shutil.copyfile(target_audio, vismart_public_audio)
        print(f"[Step 1 Complete] Voice Duration: {duration}s")

    # Step 2: Visual Style Dispatcher
    if args.style == "long_explainer":
        entry_file = os.path.join(REMOTION_DIR, "src", "index.ts")
        comp_id = "LongExplainer16x9"
    elif args.style == "silent_kinetic" or args.mode == "silent":
        entry_file = os.path.join(REMOTION_DIR, "src", "index.ts")
        comp_id = "SilentKinetic"
    elif args.style == "vismart":
        entry_file = os.path.join(PROJECT_ROOT, "vismart-unified-creative-director", "remotion", "src", "index.tsx")
        comp_id = "Demo"
    else:
        entry_file = os.path.join(REMOTION_DIR, "src", "index.ts")
        comp_id = "Main"

    # Step 3: Headless MP4 Render
    print(f"[Step 2] Rendering {comp_id} via Remotion...")
    success = render_remotion_composition(entry_file, comp_id, out_mp4, remotion_dir=REMOTION_DIR)

    if success:
        cover_png = out_mp4.replace(".mp4", "_cover.png")
        render_cover_thumbnail(entry_file, comp_id, cover_png, frame=60, remotion_dir=REMOTION_DIR)
        print("=======================================================")
        print(f"🎉 VIDEO READY: {out_mp4}")
        print(f"🖼️ COVER THUMBNAIL: {cover_png}")
        print("=======================================================")
    else:
        print("❌ Video generation failed. Check logs above.")

def main():
    parser = argparse.ArgumentParser(description="Vismart Modular Video Production Engine")
    parser.add_argument("--audio", type=str, help="Path to user-uploaded audio file (mp3/wav/m4a)")
    parser.add_argument("--text", type=str, help="Hindi or English script to speak if no audio file is given")
    parser.add_argument("--voice", type=str, default="hi-IN-MadhurNeural", help="Edge-TTS voice identifier")
    parser.add_argument("--rate", type=str, default="+10%", help="Voice speed rate (e.g. +6 percent, +12 percent)")
    parser.add_argument("--pitch", type=str, default="+0Hz", help="Voice pitch adjustment (e.g. -10Hz for deep, +0Hz normal, +10Hz crisp)")
    parser.add_argument("--style", type=str, choices=["vismart", "agency_ui", "silent_kinetic", "long_explainer"], default="silent_kinetic", help="Video visual style")
    parser.add_argument("--format", type=str, choices=["reel", "long", "story"], default="reel", help="Output content format")
    parser.add_argument("--mode", type=str, choices=["voice", "silent"], default="voice", help="Audio mode (voice: speaks narration, silent: music & sfx only)")
    parser.add_argument("--output", type=str, help="Output MP4 file path")

    args = parser.parse_args()
    asyncio.run(run_pipeline(args))

if __name__ == "__main__":
    main()
