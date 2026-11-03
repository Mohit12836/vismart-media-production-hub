import {useEffect, useState} from "react";
import {AbsoluteFill, Audio, Sequence, cancelRender, continueRender, delayRender, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from "remotion";
import {motion, palettes, neutral} from "./theme";
import type {CreativePlan, DirectedScenePlan, DirectedTiming} from "./types";

type Palette = typeof palettes.directed_motion;
const clamp = {extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const};
const tween = (f: number, from: number, to: number, a: number, b: number) => interpolate(f, [from, to], [a, b], {...clamp, easing: motion.out});

function Bubble({text, incoming = true, palette}: {text: string; incoming?: boolean; palette: Palette}) {
  return <div style={{marginLeft: incoming ? 0 : 42, marginRight: incoming ? 42 : 0, background: incoming ? neutral.white : palette.line, border: `2px solid ${palette.line}`, padding: "26px 28px", borderRadius: incoming ? "22px 22px 22px 5px" : "22px 22px 5px 22px", fontSize: 36, lineHeight: 1.55, color: palette.text, boxShadow: `0 8px 22px ${neutral.shadow}`}}>{text}</div>;
}

function Phone({scene, palette}: {scene: DirectedScenePlan; palette: Palette}) {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const incoming = spring({frame: frame - Math.round(fps * .12), fps, config: motion.snappy});
  const leaving = scene.visual === "inbox" ? tween(frame, fps * 1.4, fps * 2.2, 0, 1) : 0;
  const solved = scene.visual === "handoff" || scene.visual === "steps" || scene.visual === "cta";
  return <div style={{position: "relative", width: 586, height: 760, borderRadius: 48, padding: "28px 15px 22px", background: neutral.dark, boxShadow: `0 32px 70px ${neutral.shadow}`, transform: `rotate(${Math.sin(frame/fps*1.1)*.7}deg)`}}>
    <div style={{position: "absolute", left: "50%", top: 9, transform: "translateX(-50%)", width: 86, height: 13, borderRadius: 9, background: neutral.muted}} />
    <div style={{height: "100%", overflow: "hidden", borderRadius: 32, background: palette.paper, color: palette.text}}>
      <div style={{height: 100, padding: "27px 25px", display: "flex", alignItems: "center", gap: 18, background: palette.line, fontSize: 27, fontWeight: 700}}><span style={{display: "block", width: 40, height: 40, borderRadius: "50%", background: palette.hero}} /> आपकी business chat</div>
      <div style={{padding: "32px 22px", display: "flex", flexDirection: "column", gap: 26}}>
        <div style={{transform: `translate(${leaving * -600}px,${(1 - incoming) * 40}px) scale(${.96 + incoming * .04})`, opacity: 1 - leaving}}><Bubble text={scene.message || "यह सामान मिलेगा?"} palette={palette} /></div>
        {scene.reply || solved ? <div style={{opacity: tween(frame, fps * .8, fps * 1.15, 0, 1), transform: `translateY(${tween(frame, fps * .8, fps * 1.15, 36, 0)}px)`}}><Bubble incoming={false} text={scene.reply || "हाँ। कौन-सा size चाहिए?"} palette={palette} /></div> : <div style={{margin: "10px 20px", color: neutral.red, fontWeight: 700, fontSize: 38, transform: `translateY(${Math.sin(frame/fps*2)*3}px)`}}>जवाब बाकी है…</div>}
        {solved ? <div style={{fontSize: 27, color: palette.dim, margin: "8px 24px", opacity: tween(frame, fps * 1.6, fps * 2, 0, 1)}}>अगला कदम साफ है ✓</div> : null}
      </div>
    </div>
    <div style={{position: "absolute", bottom: 8, left: "40%", width: "20%", height: 5, borderRadius: 3, background: neutral.muted}} />
  </div>;
}

function Options({scene, palette}: {scene: DirectedScenePlan; palette: Palette}) {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return <div style={{width: 850, display: "flex", flexDirection: "column", gap: 35}}>
    {(["A", "B"] as const).map((letter, i) => {
      const p = spring({frame: f - Math.round(i * fps * .14), fps, config: motion.smooth});
      const correct = scene.visual === "answer" && scene.correct === letter;
      return <div key={letter} style={{background: correct ? palette.hero : palette.paper, color: correct ? neutral.white : palette.ink, border: `3px solid ${correct ? palette.hero : palette.line}`, borderRadius: 24, padding: "38px 32px", minHeight: 195, display: "flex", gap: 26, alignItems: "center", transform: `translateX(${(1-p) * (i ? 70 : -70)}px) scale(${.96 + p * .04})`, opacity: i ? Math.min(1,p) : 1, boxShadow: `0 18px 40px ${neutral.shadow}`}}>
        <div style={{fontFamily: "sans-serif", fontSize: 44, fontWeight: 900, border: "2px solid currentColor", borderRadius: "50%", width: 76, height: 76, display: "grid", placeItems: "center", flexShrink: 0}}>{letter}</div>
        <div style={{fontSize: 45, fontWeight: 700, lineHeight: 1.5}}>{letter === "A" ? scene.option_a : scene.option_b}{correct ? " ✓" : ""}</div>
      </div>;
    })}
  </div>;
}

function Shop({scene, palette}: {scene: DirectedScenePlan; palette: Palette}) {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame, fps, config: motion.smooth});
  return <div style={{width: 840, transform: `translateY(${(1-p)*35}px) rotate(${Math.sin(frame/fps)*.3}deg)`}}>
    <svg viewBox="0 0 840 400" width="840" height="400" aria-label="Illustrated shop">
      <rect x="90" y="100" width="660" height="270" rx="20" fill={palette.paper} stroke={palette.line} strokeWidth="4" />
      <path d="M65 100 L120 20 H720 L775 100Z" fill={palette.hero} />
      {[0,1,2,3,4,5].map(i=><rect key={i} x={90+i*110} y={100} width={110} height={42} rx={18} fill={i%2?palette.surface:palette.hero} />)}
      <rect x="150" y="170" width="250" height="145" rx="10" fill={palette.surface}/><rect x="470" y="165" width="190" height="205" rx="12" fill={palette.surface}/>
      <circle cx="275" cy="215" r="28" fill={palette.hero}/><path d="M220 310 Q220 250 275 250 Q330 250 330 310" fill={palette.hero}/>
      <text x="570" y="265" textAnchor="middle" fontSize="32" fill={palette.text} fontFamily="ReelHindi">दुकान</text>
    </svg>
    <div style={{margin: "15px 50px 0", transform: `translateX(${Math.sin(frame/fps)*5}px)`}}><Bubble text={scene.message || "यह सामान मिलेगा?"} palette={palette} /></div>
    <div style={{margin: "24px 50px 0", opacity: tween(frame, fps, fps*1.35, 0, 1)}}><Bubble incoming={false} text={scene.reply || "थोड़ी देर में जवाब देता हूँ…"} palette={palette} /></div>
  </div>;
}

function Caption({timing, palette}: {timing: DirectedTiming; palette: Palette}) {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const seconds = frame/fps;
  const active = timing.words.findIndex(word=>seconds>=word.start && seconds<=word.end);
  if(active<0) return null;
  const start = Math.floor(active/4)*4;
  return <div style={{position: "absolute", top: 1390, left: 75, right: 105, display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "6px 12px", fontSize: 43, fontWeight: 700, lineHeight: 1.6}}>
    {timing.words.slice(start,start+4).map((word,i)=><span key={start+i} style={{padding: "4px 10px", borderRadius: 10, color: start+i===active && palette.hero!==palettes.directed_motion.hero ? neutral.white : palette.text, background: start+i===active ? palette.hero : palette.paper}}>{word.text}</span>)}
  </div>;
}

function Scene({scene, timing, palette, index, total, style}: {scene: DirectedScenePlan; timing: DirectedTiming; palette: Palette; index: number; total: number; style: string}) {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame, fps, config: motion.smooth});
  const exit = interpolate(frame, [timing.duration-Math.round(.28*fps),timing.duration], [0,1], {...clamp,easing:motion.in});
  const titleWords = scene.headline.split(' ');
  const isOptions = scene.visual === "choices" || scene.visual === "answer";
  return <AbsoluteFill style={{color: palette.ink, transform:`translateX(${exit*-90}px)`, opacity: 1-exit*.7}}>
    <div style={{position: "absolute", left: 90, right: 120, top: 240, fontSize: style==="chat_story"?84:94, lineHeight: 1.28, fontWeight: 700, letterSpacing:-2}}>
      {titleWords.map((word,i)=>{const p= i===0?1:spring({frame:frame-Math.round(i*.085*fps),fps,config:motion.snappy});return <span key={i} style={{display:"inline-block",marginRight:18,opacity:Math.min(1,p),transform:`translateY(${(1-p)*25}px) scale(${.96+p*.04})`}}>{word}</span>})}
    </div>
    <div style={{position: "absolute", top: isOptions?610:545, left: 0, right: 0, display: "flex", justifyContent: "center", transform: `translateY(${(1-enter)*24 + Math.sin(frame/fps*1.3)*3}px) scale(${.98+enter*.02})`}}>
      {isOptions ? <Options scene={scene} palette={palette}/> : scene.visual==="shop" ? <Shop scene={scene} palette={palette}/> : scene.visual==="steps" ? <div style={{width:800,padding:40,borderRadius:28,background:palette.paper,boxShadow:`0 25px 50px ${neutral.shadow}`}}>{["पूछताछ पहचानें","जवाब साफ लिखें","अगला कदम बताएँ"].map((text,i)=><div key={text} style={{fontSize:48,color:palette.text,padding:"36px 0",borderBottom:i<2?`2px solid ${palette.line}`:undefined,opacity:tween(frame,i*fps*.4,i*fps*.4+fps*.3,.35,1),transform:`translateX(${tween(frame,i*fps*.4,i*fps*.4+fps*.3,20,0)}px)`}}><span style={{color:palette.hero,marginRight:22}}>✓</span>{text}</div>)}</div> : <Phone scene={scene} palette={palette}/>}
    </div>
    <div style={{position:"absolute",top:1310,left:90,right:120,textAlign:"center",fontSize:29,fontWeight:700,color:palette.dim}}>{scene.label || `${index+1} / ${total}`}</div>
    <Caption timing={timing} palette={palette}/>
    {timing.audio ? <Audio src={staticFile(timing.audio)} volume={.95}/> : null}
  </AbsoluteFill>;
}

export function DirectedVideo({creative_plan, directed_timeline, creative_style, brand, soundkit}: {creative_plan: CreativePlan; directed_timeline: DirectedTiming[]; creative_style: string; brand: string; soundkit?: boolean}) {
  const frame=useCurrentFrame();
  const {fps,durationInFrames}=useVideoConfig();
  const [fontHandle]=useState(()=>delayRender("Loading local Hindi type"));
  useEffect(()=>{Promise.all([document.fonts.load('700 80px "ReelHindi"'),document.fonts.load('400 40px "ReelHindi"')]).then(()=>continueRender(fontHandle)).catch(cancelRender)},[fontHandle]);
  const palette=palettes[creative_style as keyof typeof palettes] || palettes.directed_motion;
  const noise="url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='1'/%3E%3C/filter%3E%3Crect width='120' height='120' filter='url(%23n)' opacity='.3'/%3E%3C/svg%3E\")";
  return <AbsoluteFill style={{background:palette.bg,fontFamily:'ReelHindi, sans-serif',overflow:"hidden"}}>
    <style>{`@font-face{font-family:ReelHindi;src:url('${staticFile('factory-fonts/NotoSansDevanagari-Regular.ttf')}');font-weight:400}@font-face{font-family:ReelHindi;src:url('${staticFile('factory-fonts/NotoSansDevanagari-Bold.ttf')}');font-weight:700}`}</style>
    <AbsoluteFill style={{background:`radial-gradient(ellipse at ${35+Math.sin(frame/fps*.4)*10}% 50%,${palette.surface},transparent 75%)`}}/>
    <svg width="1080" height="1920" style={{position:"absolute",opacity:.12}}><path d={`M-100 ${570+Math.sin(frame/fps)*20} Q550 50 1200 700 M-100 1000 Q400 1600 1200 900`} fill="none" stroke={palette.dim} strokeWidth="2"/></svg>
    {directed_timeline.map((timing,index)=><Sequence key={index} from={timing.from} durationInFrames={timing.duration}><Scene scene={creative_plan.scenes[index]} timing={timing} palette={palette} index={index} total={directed_timeline.length} style={creative_style}/>{soundkit?<Audio src={staticFile(index===0?'factory-sfx/pop.wav':'factory-sfx/sweep.wav')} volume={.22}/>:null}</Sequence>)}
    <div style={{position:"absolute",top:160,left:90,right:120,color:palette.dim,fontSize:25,fontWeight:700,display:"flex",justifyContent:"space-between"}}><span>{brand}</span><span>{creative_plan.fictional?'काल्पनिक उदाहरण':'उदाहरण / demo'}</span></div>
    <AbsoluteFill style={{pointerEvents:"none",background:palette.hero,mixBlendMode:"soft-light",opacity:.035}}/>
    <AbsoluteFill style={{pointerEvents:"none",backgroundImage:noise,backgroundSize:"120px",opacity:.035,mixBlendMode:"multiply"}}/>
    <AbsoluteFill style={{pointerEvents:"none",background:"radial-gradient(ellipse at center,transparent 62%,rgba(8,15,35,.12))"}}/>
    <div style={{position:"absolute",top:1585,left:90,right:120,height:5,background:palette.surface}}><div style={{height:5,background:palette.dim,width:`${frame/durationInFrames*100}%`}}/></div>
    {soundkit?<Audio src={staticFile('factory-sfx/bed.wav')} volume={.12}/>:null}
  </AbsoluteFill>;
}
