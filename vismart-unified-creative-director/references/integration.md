# Integration decisions and honest limitations

The Hindi skill upload includes `AGENTS.md`, `SKILL.md`, and four references; no complete source project. The faceless upload includes README + SKILL, but not the cited `styles/` folders, `scripts/`, `src/core/kit.js` or sample renders. Therefore source-level merging of its exact Six 3D/2D engines is **not possible from supplied files**. This pack preserves the rules and creates a standalone baseline renderer; it's not a port of absent code.

The 2D baseline implements semantic scenes, beat timing, emotional palette, camera-like move using frame time, basic SVG illustrations, subtitles, audio if a supplied file is available, and Remotion output. Adding real 3D requires dependencies/assets and performance testing. Alignment, voice synthesis and production stock acquisition are documented integration points, not fabricated capabilities of this baseline.

Stage 1: validate scene plans and create code-driven ad videos. Stage 2: add actual word-level Whisper timestamps, audio ducking, asset provenance. Stage 3: integrate reusable Three.js scene packages once the original full faceless source is provided, or implement new models ourselves. Stage 4: audio/video metrics and creative human-in-loop QA.
