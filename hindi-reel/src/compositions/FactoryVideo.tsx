import React from "react";
import {AbsoluteFill, Audio, Img, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from "remotion";

export type FactoryProps = {
  scenes: string[];
  duration: number;
  format: string;
  layout: string;
  brand: string;
  accent: string;
  assets: string[];
  audio: string | null;
};

const Scene: React.FC<{text: string; index: number; count: number; layout: string; accent: string; asset?: string}> = ({text, index, count, layout, accent, asset}) => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const wide = width > height;
  const enter = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: "clamp"});
  const isQuestion = layout === "quiz" && index === 0;
  const isAnswer = layout === "quiz" && index === count - 1;
  const light = layout === "listicle" || isAnswer;
  return <AbsoluteFill style={{backgroundColor: light ? "#eff4ff" : layout === "story" ? "#202a3c" : "#101c34", color: light ? "#142340" : "white", justifyContent: "center", padding: wide ? "120px 180px" : "180px 92px", fontFamily: "'Noto Sans Devanagari', 'Noto Sans', sans-serif"}}>
    {asset ? <Img src={staticFile(`factory-assets/${asset}`)} style={{position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover", transform: `scale(${1 + frame / 1800})`}} /> : null}
    {asset ? <AbsoluteFill style={{background: "linear-gradient(0deg,rgba(6,15,30,.95),rgba(6,15,30,.2))"}} /> : null}
    {layout === "listicle" ? <div style={{position: "absolute", top: wide ? 90 : 210, right: 90, color: accent, opacity: .15, fontSize: wide ? 280 : 400, fontWeight: 900}}>{index + 1}</div> : null}
    <div style={{position: "relative", opacity: enter, transform: `translateY(${(1 - enter) * 24}px)`, marginTop: asset ? "auto" : 0}}>
      <div style={{fontSize: 30, fontWeight: 700, marginBottom: 34, color: asset ? "#b5d5ff" : accent}}>{isQuestion ? "सोचिए…" : isAnswer ? "जवाब" : layout === "story" ? `${index + 1} / ${count}` : layout === "listicle" ? `TIP ${index + 1}` : ""}</div>
      <div style={{fontSize: wide ? (text.length > 100 ? 62 : 82) : (text.length > 100 ? 64 : 88), lineHeight: 1.38, fontWeight: 800, overflowWrap: "anywhere", textShadow: asset ? "0 3px 16px #000" : undefined}}>{text}</div>
      {layout === "kinetic" ? <div style={{marginTop: 42, height: 9, width: `${30 + enter * 60}%`, backgroundColor: accent}} /> : null}
    </div>
  </AbsoluteFill>;
};

export const FactoryVideo: React.FC<FactoryProps> = ({scenes, layout, brand, accent, assets, audio}) => {
  const frame = useCurrentFrame();
  const {durationInFrames, width, height} = useVideoConfig();
  return <AbsoluteFill>
    {scenes.map((text, index) => {
      const from = Math.round(index * durationInFrames / scenes.length);
      const until = Math.round((index + 1) * durationInFrames / scenes.length);
      return <Sequence key={index} from={from} durationInFrames={until - from}><Scene text={text} index={index} count={scenes.length} layout={layout} accent={accent} asset={assets[index]} /></Sequence>;
    })}
    {audio ? <Audio src={staticFile(audio)} /> : null}
    <div style={{position: "absolute", top: height > width ? 105 : 45, left: 65, color: "white", backgroundColor: "#142340", borderRadius: 8, padding: "12px 22px", fontFamily: "sans-serif", fontSize: 26, maxWidth: width - 130}}>{brand}</div>
    <div style={{position: "absolute", bottom: height > width ? 180 : 50, left: 65, right: 65, height: 5, background: "#8296b555"}}><div style={{height: "100%", backgroundColor: accent, width: `${100 * frame / durationInFrames}%`}} /></div>
  </AbsoluteFill>;
};
