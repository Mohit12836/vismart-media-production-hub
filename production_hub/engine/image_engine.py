import os
import urllib.parse
import urllib.request
import time

def generate_ai_image(prompt: str, output_path: str, width: int = 720, height: int = 1280, retries: int = 3) -> bool:
    """
    Generates a 100% Free AI Image using Pollinations AI (Zero API keys, Zero cost).
    Produces 9:16 high-resolution vertical cinematic images.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    clean_prompt = urllib.parse.quote(f"{prompt}, 8k resolution, cinematic lighting, photorealistic, professional photography, vertical 9:16")
    url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width={width}&height={height}&nologo=true&enhance=true&seed={int(time.time())}"
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    req = urllib.request.Request(url, headers=headers)
    
    for attempt in range(1, retries + 1):
        try:
            print(f"[ImageEngine] Generating image (Attempt {attempt}): '{prompt[:40]}...'")
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                if len(data) > 1000:
                    with open(output_path, "wb") as f:
                        f.write(data)
                    print(f"[ImageEngine] Saved successfully to {output_path} ({len(data)} bytes)")
                    return True
        except Exception as e:
            print(f"[ImageEngine] Error on attempt {attempt}: {e}")
            time.sleep(2)
            
    return False

if __name__ == "__main__":
    generate_ai_image("modern luxury medical dental clinic reception 4k", "test_preview.jpg")
