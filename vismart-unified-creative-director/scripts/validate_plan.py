#!/usr/bin/env python3
import json,sys,math
from pathlib import Path

def validate(data):
 errors=[]; warnings=[]
 meta=data.get('meta',{}); beats=data.get('beats',[])
 if not isinstance(beats,list) or not beats: return ['beats must be nonempty'],[]
 last=0; ids=set()
 for idx,b in enumerate(beats):
  key=f'beat[{idx}]'; ident=b.get('id')
  if not ident or ident in ids: errors.append(f'{key}: missing/duplicate id')
  ids.add(ident)
  try: start=float(b['start']); end=float(b['end'])
  except (KeyError,ValueError,TypeError): errors.append(f'{key}: invalid times');continue
  if not all(math.isfinite(v) for v in (start,end)):errors.append(f'{key}: non-finite timestamps')
  if start < 0 or end<=start: errors.append(f'{key}: invalid interval')
  if start<last-1e-6:errors.append(f'{key}: overlaps previous beat')
  if start>last+.08:warnings.append(f'{key}: gap of {start-last:.2f}s; intentional?')
  if end-start>8:warnings.append(f'{key}: long hold {end-start:.1f}s; review intentionality')
  last=end
  for field in ('voice','viewer_goal','visual','shot','motion','caption','audio','asset_strategy','evidence'):
   if not str(b.get(field,'')).strip(): errors.append(f'{key}: missing {field}')
  e=b.get('emotion',{})
  if not e.get('primary'):errors.append(f'{key}: missing primary emotion')
  if e.get('confidence') not in ('text-inferred','audio-informed','human-verified'): errors.append(f'{key}: invalid emotion confidence')
  try:
   intensity=float(e['intensity'])
   if not (0<=intensity<=1):errors.append(f'{key}: emotion intensity out of range')
  except (KeyError,ValueError,TypeError):errors.append(f'{key}: invalid emotion intensity')
  if b.get('asset_strategy','').startswith('paid'):errors.append(f'{key}: paid visual forbidden')
 if 'duration' in meta and abs(float(meta['duration'])-last)>.15: errors.append('meta.duration differs from beats end')
 if meta.get('word_alignment')!='verified':warnings.append('word alignment not verified; highlight captions need human review')
 return errors,warnings
if __name__=='__main__':
 d=json.loads(Path(sys.argv[1]).read_text(encoding='utf8'));errors,warnings=validate(d)
 for w in warnings:print('WARN:',w)
 for e in errors:print('ERROR:',e)
 print('PASS: temporal/structural validation' if not errors else 'FAIL')
 sys.exit(bool(errors))
