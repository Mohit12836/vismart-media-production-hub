import os
import sys
import subprocess
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def render_remotion_composition(entry_file: str, composition_id: str, output_mp4: str, remotion_dir: str = None) -> bool:
    """
    Renders any Remotion composition headlessly to MP4 using hardware or software encoders.
    Works identically on Windows and Linux VPS.
    """
    if not remotion_dir:
        remotion_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "hindi-reel"))

    os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)
    abs_entry = os.path.abspath(entry_file).replace("\\", "/")
    abs_output = os.path.abspath(output_mp4).replace("\\", "/")

    print(f"[RemotionEngine] Starting render of {composition_id}...")
    start_t = time.time()

    cmd = [
        "node", os.path.join(remotion_dir, "node_modules", "@remotion", "cli", "remotion-cli.js"), "render",
        abs_entry,
        composition_id,
        abs_output,
        "--codec=h264",
        "--crf=20",
        "--concurrency=4"
    ]

    # Run inside project directory containing node_modules
    result = subprocess.run(cmd, cwd=remotion_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", timeout=7200)
    
    elapsed = round(time.time() - start_t, 1)
    if result.returncode == 0 and os.path.exists(output_mp4) and os.path.getsize(output_mp4) > 10000:
        size_mb = round(os.path.getsize(output_mp4) / (1024 * 1024), 2)
        print(f"[RemotionEngine] ✅ Render SUCCESS in {elapsed}s: {output_mp4} ({size_mb} MB)")
        return True
    else:
        print(f"[RemotionEngine] ❌ Render failed:\n{result.stderr}")
        return False

def render_cover_thumbnail(entry_file: str, composition_id: str, output_png: str, frame: int = 40, remotion_dir: str = None) -> bool:
    """Renders a single still frame as a YouTube/Reels cover."""
    if not remotion_dir:
        remotion_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "hindi-reel"))

    os.makedirs(os.path.dirname(os.path.abspath(output_png)), exist_ok=True)
    abs_entry = os.path.abspath(entry_file).replace("\\", "/")
    abs_output = os.path.abspath(output_png).replace("\\", "/")

    cmd = [
        "node", os.path.join(remotion_dir, "node_modules", "@remotion", "cli", "remotion-cli.js"), "still",
        abs_entry,
        composition_id,
        abs_output,
        f"--frame={frame}"
    ]

    result = subprocess.run(cmd, cwd=remotion_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
    return result.returncode == 0 and os.path.exists(output_png)
