# Design system (extracted from the reference reel)

Canvas: 720x1280, background #FFFFFF with faint dot/confetti accents. Flat 3D-ish pastel illustration style, thick dark outlines (3-4px #111), offset hard shadow (6px 6px 0 #111).

## Colors
- ink #111111
- pink #FF2E63 (headline emphasis, danger)
- blue/purple #4338FF / #7C3AED (tech words)
- green #10B981 / #14D9A5 (success, "free", "live")
- yellow #FFD60A (subtitle highlight, stickers)
- soft card tints: pink #FFE4EC, mint #DDF8EE, lilac #EDE7FF, cream #FFF6D6

## Typography (Google Fonts via @remotion/google-fonts)
- Headline: "Mukta" or "Poppins"+"Hind" 800 weight, 64-80px, line-height 1.05, centered, max 2 lines, outline stroke for pop.
- Emphasis line (2nd line) uses accent color (pink/green/purple) - one accent per scene.
- Subtitle bar: 44px, weight 700, black text; active word gets yellow rounded highlight (#FFD60A, radius 10px).
- Micro label chip (top): 18px monospace, pill with border, shows section name.
- Always load `devanagari` + `latin` subsets.

## Layout (720x1280)
- Top chip: y=40
- Headline block: y=100-330
- Hero card/illustration: y=360-900 (max 600x540)
- Mascot: bottom-left, 220px, y=1000-1230
- Subtitle strip: y=1090-1200, x=200..680 (right of mascot) or centered
- Source footnote (tiny, 14px grey) under card when citing facts.

## Motion language
- Headline: words pop in with spring (damping 12, stiffness 180), stagger 4 frames/word.
- Cards: slide up 40px + scale .92->1, spring.
- Stickers/badges: rotate -6deg to 3deg with bounce, appear on keyword timestamp.
- Emphasis: strike-through animation (pink X) for "wrong" things, green tick for "right".
- Scene transitions: 6-frame slide/fade via TransitionSeries; section changes use 10-frame wipe.
- Camera feel: slow zoom 1.00->1.04 across scene.
