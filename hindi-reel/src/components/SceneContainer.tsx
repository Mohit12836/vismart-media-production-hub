import React from "react";
import { Audio, staticFile } from "remotion";
import { Headline } from "./Headline";
import { SectionChip } from "./SectionChip";
import { SubtitleBar } from "./SubtitleBar";
import { THEME } from "../theme";

export interface SceneData {
  id: string;
  chip: string;
  line1: string;
  line2: string;
  accent: string;
  subtitle: string;
  highlights: string[];
  audio: string;
  durationSec: number;
  frames: number;
}

interface SceneContainerProps {
  scene: SceneData;
  children: React.ReactNode;
}

export const SceneContainer: React.FC<SceneContainerProps> = ({ scene, children }) => {
  return (
    <div
      style={{
        width: 720,
        height: 1280,
        backgroundColor: THEME.colors.bg,
        position: "relative",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      {/* Cinematic Ambient Glow in Background */}
      <div
        style={{
          position: "absolute",
          top: 150,
          left: 100,
          width: 520,
          height: 520,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${scene.accent}25 0%, transparent 70%)`,
          filter: "blur(60px)",
          pointerEvents: "none",
        }}
      />

      {/* Voiceover Audio */}
      <Audio src={staticFile(scene.audio)} />

      {/* Transition Whoosh SFX at start */}
      <Audio src={staticFile("audio/whoosh.mp3")} volume={0.25} />

      {/* Top Section Chip */}
      <SectionChip label={scene.chip} />

      {/* Headline Block */}
      <Headline line1={scene.line1} line2={scene.line2} accent={scene.accent} />

      {/* Center Apple-Grade Display Frame */}
      <div
        style={{
          position: "absolute",
          top: 240,
          left: 40,
          right: 40,
          height: 690,
          backgroundColor: THEME.colors.bgCard,
          border: `1.5px solid ${THEME.colors.border}`,
          borderRadius: 36,
          boxShadow: THEME.shadow,
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
          zIndex: 30,
        }}
      >
        {/* Sleek Top Status Bar with Glass Glow */}
        <div
          style={{
            height: 44,
            backgroundColor: "rgba(255, 255, 255, 0.04)",
            borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "0 20px",
          }}
        >
          <div style={{ display: "flex", gap: 7 }}>
            <div style={{ width: 11, height: 11, borderRadius: "50%", backgroundColor: "#FF5F56" }} />
            <div style={{ width: 11, height: 11, borderRadius: "50%", backgroundColor: "#FFBD2E" }} />
            <div style={{ width: 11, height: 11, borderRadius: "50%", backgroundColor: "#27C93F" }} />
          </div>
          <div
            style={{
              fontSize: 13,
              fontWeight: 700,
              color: THEME.colors.muted,
              letterSpacing: "0.08em",
              textTransform: "uppercase",
            }}
          >
            CLINIC SYSTEM PRO
          </div>
          <div style={{ width: 35 }} />
        </div>

        {/* Dynamic Center Visual */}
        <div
          style={{
            flex: 1,
            padding: "24px 20px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            position: "relative",
          }}
        >
          {children}
        </div>
      </div>

      {/* Centered Modern Subtitle Bar */}
      <SubtitleBar
        text={scene.subtitle}
        highlights={scene.highlights}
        durationInFrames={scene.frames}
      />
    </div>
  );
};
