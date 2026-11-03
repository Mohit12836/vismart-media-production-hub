# Scene Grammar and Graphics Routing

## Semantics first
Write: claim → evidence/visual metaphor → viewer attention target → scene staging → frame/action timing → exit. Don't use random stock footage because keywords matched.

## Render strategy
- Procedural SVG/React: charts, maps, UI, numbers, diagrams, title cards. Fast and crisp.
- Canvas: repeated particles, hand-drawn style, shape morph and 2D characters; render deterministically.
- Three.js/R3F: actual spatial need (depth, anatomy, moving camera, 3D product). Use `@remotion/three` when integrated and stable; GPU-dependent.
- Free stock: real human context, shop scenes, exterior; verify footage license, release and limitations; don't represent as actual customer.
- Pre-rendered assets: Blender or existing style renderer frame sequences; only if code/asset is actually present and tested.

## Six inherited faceless grammars
1. Deep Dive 3D: camera journeys and anatomical metaphors; optional true Three.js, fallback labeled diagram.
2. Night File 3D: spatial concealment, noir lighting, maps/dates; avoid unjustified true-crime implication.
3. Inside Out: high contrast 2D diagrams, x-ray metaphors, educational pacing.
4. Stick Story: simple expressive body language, steps, staging and spatial continuity.
5. Paper Atlas: maps, time/place relations, paper layers and animated paths.
6. Tall Tale 3D: playful 2.5D hybrid scenes and comic reaction timing.
Additional: Hindi Explainer, Local Business Ad, SaaS/UI Demo, Product Ad.

## Composition grammar
- Full bleed environment: emotional context and location.
- Negative-space hero: suspense or emphasis.
- Split comparison: only when two alternatives are truly contrasted.
- UI walkthrough: zoom into functional touch point, not everything at once.
- Information-first diagram: high contrast and no fake decorative charts.
- Reaction insert: emotion changes reveal user decision.

## Speed safeguards
Use static but purposeful holds; 0.8–7s is indicative, not a rule. Cut on semantic changes, audio phrase boundaries or motivated action. Cache common geometry/assets and render draft before full HD.
