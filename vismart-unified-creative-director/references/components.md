# Components (build once, reuse everywhere)

Create each in `src/components/`. All take `frame`-driven props, no internal timers.

1. **Mascot.tsx** - robot with blue cap, 4 poses: `explain` (hand open), `think` (hand on chin), `surprise` (hands up), `point`. Props: pose, enterFrame. Bobbing idle: translateY = sin(frame/12)*4. Use original SVG/PNG art (generate or draw your own - do not copy other creators' characters).
2. **Headline.tsx** - props: line1, line2, accent. Word-by-word spring entrance.
3. **SectionChip.tsx** - pill at top: dot + label ("pehle 2 shabd").
4. **Card.tsx** - bordered rounded box (radius 24, border 4px ink, hard shadow), header bar with 3 window dots + title tag; variants: browser, phone, laptop, file-list, chat.
5. **SplitCards.tsx** - two cards side by side (Domain vs Hosting, Plan A vs B) with labels and "?" sticker -> reveal.
6. **Sticker.tsx** - tilted badge ("FREE", "LIVE", "Rs 0", "Combo!"). Props: text, color, rotate, appearAt.
7. **SubtitleBar.tsx** - renders words from captions.json, highlights active word with yellow pill; previous words dim, upcoming words grey.
8. **StepBadge.tsx** - "tareeka 1/2/3" lock-icon cards (locked -> unlocked with confetti).
9. **BrowserBar.tsx** - fake URL bar with typing animation (`rahul.vercel.app` typed char by char via slice(0, frame*0.6)).
10. **Confetti.tsx** - 30 particles, deterministic via `random(seed)` from remotion.
11. **EndCTA.tsx** - Follow button, Save bookmark with "Saved ✓" pop, "send to a friend" laptop icon.

Props typed with zod so Studio can edit them.
