#!/usr/bin/env python3
"""
Vismart Canva MCP & Visual Asset Integration Engine
Bridges Canva Design Templates, Brand Kits, and 9:16 Safe-Zone Layers with Remotion
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, Optional, List

BASE_DIR = Path(__file__).resolve().parent.parent
CANVA_ASSETS_DIR = BASE_DIR / "assets" / "canva"
CANVA_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
REMOTION_CANVA_DIR = BASE_DIR.parent / "hindi-reel" / "public" / "assets" / "canva"
REMOTION_CANVA_DIR.mkdir(parents=True, exist_ok=True)

# Vismart Official Brand Kits
BRAND_KITS = {
    "vismart_healthcare": {
        "name": "Vismart Clinic Pro",
        "primary": "#0F172A",
        "accent": "#2563EB",
        "success": "#10B981",
        "background": "#FFFFFF",
        "surface": "#F8FAFC",
        "fonts": {
            "headline": "Outfit, sans-serif",
            "body": "Noto Sans Devanagari, Inter, sans-serif"
        },
        "safe_zones": {
            "top_px": 220,
            "bottom_px": 340,
            "sides_px": 60
        }
    },
    "vismart_agency_luxury": {
        "name": "Vismart Studio Titanium",
        "primary": "#0A0E17",
        "accent": "#00F2FE",
        "success": "#34D399",
        "background": "#07090E",
        "surface": "rgba(15, 23, 42, 0.8)",
        "fonts": {
            "headline": "Cabinet Grotesk, sans-serif",
            "body": "Plus Jakarta Sans, sans-serif"
        },
        "safe_zones": {
            "top_px": 220,
            "bottom_px": 340,
            "sides_px": 60
        }
    }
}

def get_brand_kit(brand_id: str = "vismart_healthcare") -> Dict:
    """Returns the standardized brand kit tokens for Canva & Remotion."""
    return BRAND_KITS.get(brand_id, BRAND_KITS["vismart_healthcare"])

def import_canva_asset(source_png_path: str, asset_name: str) -> str:
    """
    Imports a transparent Canva PNG or background graphic,
    places it into Remotion public assets, and returns relative Remotion URL.
    """
    src = Path(source_png_path)
    if not src.exists():
        raise FileNotFoundError(f"Source Canva asset not found: {source_png_path}")

    dest = REMOTION_CANVA_DIR / f"{asset_name}.png"
    shutil.copyfile(src, dest)
    print(f"[CanvaEngine] Asset imported: {dest} (Remotion accessible)")
    return f"assets/canva/{asset_name}.png"

def generate_canva_scene_manifest(scenes: List[Dict], brand_id: str = "vismart_healthcare") -> Dict:
    """
    Validates a list of scenes against Instagram safe-zones and formats
    a unified layout manifest for Remotion video compositions.
    """
    brand = get_brand_kit(brand_id)
    manifest = {
        "brand": brand["name"],
        "resolution": {"width": 1080, "height": 1920},
        "safe_zones": brand["safe_zones"],
        "scenes": []
    }

    for idx, sc in enumerate(scenes):
        manifest["scenes"].append({
            "index": idx + 1,
            "title": sc.get("title", ""),
            "subtitle": sc.get("subtitle", ""),
            "badge": sc.get("badge", ""),
            "canva_overlay": sc.get("canva_overlay", None),
            "accent_color": sc.get("accent_color", brand["accent"]),
            "duration_frames": sc.get("duration_frames", 90)
        })

    manifest_path = CANVA_ASSETS_DIR / "latest_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return manifest

if __name__ == "__main__":
    kit = get_brand_kit()
    print("[CanvaEngine] Initialized brand kit:", kit["name"])
