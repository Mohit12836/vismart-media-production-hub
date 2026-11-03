# Voiceover, captions, sync

## Voiceover
1. Split `script.json` lines into one audio file per scene (`public/audio/s01.mp3`...). Easier sync than one long file.
2. TTS options: ElevenLabs (best Hindi), OpenAI TTS, Google Cloud TTS hi-IN (Neural2/Chirp). Keep API key in `.env`, never in code.
3. Speaking style: energetic, friendly, ~150 wpm, short pauses between sentences.
4. Measure duration: `ffprobe -v error -show_entries format=duration -of csv=p=0 s01.mp3` -> store as `durationInFrames = ceil(sec*30)+8` in script.json.

## Word timings (for highlight)
- Preferred: use TTS word timestamps if provider returns them.
- Fallback: run Whisper (`whisper s01.mp3 --language hi --word_timestamps True`) or `@remotion/install-whisper-cpp` and save `captions/s01.json` as `[{text, startMs, endMs}]`.
- Last fallback: split words evenly across audio length.

## Render
- `<Sequence from={sceneStart} durationInFrames={d}><Audio src={staticFile('audio/s01.mp3')} /></Sequence>`
- Background music: `public/audio/bg.mp3`, volume 0.12; duck to 0.05 while voice plays using `volume={(f)=>...}`.
- SFX: whoosh on scene change, pop on sticker, ding on tick (volume 0.4).

## Script format (data/script.json)
```json
[{"id":"s01","chip":"domain + hosting","line1":"Website ban gayi,","line2":"jeb me Rs 0!","accent":"pink",
  "visual":"browser-wallet","mascot":"explain","text":"Website ban gayi, jeb me zero!",
  "highlights":["zero"],"audio":"audio/s01.mp3","frames":96}]
```
