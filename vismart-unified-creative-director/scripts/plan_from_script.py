#!/usr/bin/env python3
# Intentionally conservative: heuristic planning is NOT emotional comprehension or audio alignment.
import json,sys,re
from pathlib import Path
lines=[x.strip() for x in Path(sys.argv[1]).read_text(encoding='utf8').splitlines() if x.strip()]
beats=[];t=0.0
for i,s in enumerate(lines):
 emotion='curiosity' if '?' in s or 'क्या' in s else 'concern' if any(w in s for w in ('नहीं','खाली','समस्या','परेशान')) else 'confidence'
 dur=max(2.0,round(len(s.split())/2.35,2))
 beats.append(dict(id=f'b{i+1:02}',start=round(t,2),end=round(t+dur,2),voice=s,emotion=dict(primary=emotion,secondary='',intensity=.5,confidence='text-inferred'),viewer_goal='REVIEW: viewer takeaway',visual='REVIEW: semantic visual interpretation',shot='REVIEW: shot and staging',motion='static-hold',caption='REVIEW: caption from aligned words',audio='REVIEW: cue/intentional silence',asset_strategy='original-svg',evidence='REVIEW: factual claims and provenance'))
 t+=dur
print(json.dumps({'meta':dict(title='Draft - human direction required',fps=30,width=720,height=1280,language='hi',duration=round(t,2),audio_file=None,visual_cost_policy='zero-paid',word_alignment='unverified',genre='unclassified'),'beats':beats},ensure_ascii=False,indent=2))
