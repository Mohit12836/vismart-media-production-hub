# QA Contract

Automated gate: required fields; finite timestamps; no negative times; no temporal overlap; positive beat durations; no missing visual/camera intents; range check emotion intensity; warning for unusually long holds; no unsubstantiated quantitative claim. Run `scripts/validate_plan.py`.

Visual manual gate: 0.5s contact sheet + before/after each cut + 3 representative full-resolution stills. Verify Hindi font, safe areas under app UI overlays, caption focus and legibility at phone size, consistent character/props, cut continuity, 3D intersections, color and exposure, mobile viewing.

Audio manual gate: listen at phone volume; narration intelligibility, captions actually match words, music ducking, no clipping, no abrupt cuts, intentional silences and emotional appropriateness. Alignment estimates are not verified word timestamps.

Business trust gate: sample claims and ROI clearly marked, permissions for photos and logos, visual stock not falsely presented as a real clinic/client result, sources and asset licenses recorded.

Statuses: pass / needs review / fail. A rendering command's exit code only proves technical export, not creative quality.
