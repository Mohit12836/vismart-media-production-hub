import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { THEME } from "../theme";

interface HeadlineProps {
  line1: string;
  line2: string;
  accent: string;
}

export const Headline: React.FC<HeadlineProps> = ({ line1, line2, accent }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance1 = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 200 },
  });

  const entrance2 = spring({
    frame: frame - 3,
    fps,
    config: { damping: 14, stiffness: 200 },
  });

  return (
    <div
      style={{
        position: "absolute",
        top: 88,
        left: 30,
        right: 30,
        textAlign: "center",
        zIndex: 40,
        display: "flex",
        flexDirection: "column",
        gap: 2,
      }}
    >
      <div
        style={{
          fontFamily: "'Poppins', sans-serif",
          fontSize: 46,
          fontWeight: 800,
          color: THEME.colors.ink,
          lineHeight: 1.15,
          transform: `scale(${entrance1})`,
          letterSpacing: "-0.01em",
        }}
      >
        {line1}
      </div>
      <div
        style={{
          fontFamily: "'Poppins', sans-serif",
          fontSize: 50,
          fontWeight: 900,
          color: accent,
          lineHeight: 1.15,
          transform: `scale(${entrance2})`,
          textShadow: `0 0 25px ${accent}60`,
          letterSpacing: "-0.01em",
        }}
      >
        {line2}
      </div>
    </div>
  );
};
