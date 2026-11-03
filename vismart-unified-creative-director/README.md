# Vismart Unified Creative Director v1

Merged Skill **specification plus executable 2D baseline and validation scripts**. Merges the two user's uploaded Skill documents by preserving source references and creating a unified pipeline for meaning/emotion/scene timing/Remotion visuals.

**What exists:** complete master `SKILL.md`, 4 new technical references, preserved original references, example beat-based JSON, heuristic draft planner, structural plan validator, Remotion SVG demo source.

**What does not yet exist:** the faceless-shorts original runnable 3D style kit (not included in the upload), trained emotion recognizer, production word-level forced aligner, an ElevenLabs integration, automatic selection of licensed stock, validated final voice-attached demo, and a full 3D/30-style template library. Do not represent the prototype as those capabilities.

## Try
```
python scripts/validate_plan.py examples/dentist-scene-plan.json
python scripts/plan_from_script.py examples/dentist-script.txt > /tmp/draft-plan.json
cd remotion
npm install
npm run render:demo
```

## Design rules
- Narration's **meaning** and intention drive scenes, not keyword-matching.
- The viewer's mental state and each reveal affect camera and sound.
- Natural spoken sentences can span several visual cuts.
- No need to change screens every second; hold meaningful shots.
- Any supplied voice is external, voice price is independent of visuals.
- All visual generation is free code-first; asset licenses must be checked.

## Source limitations
First user ZIP had Hindi SKILL + references, not its actual Remotion project. Second user's upload had faceless README + SKILL, not its runnable 3D kit. This is a clean reimplementation blueprint and working **2D** starter, not a literal binary/code merge of the missing projects.
