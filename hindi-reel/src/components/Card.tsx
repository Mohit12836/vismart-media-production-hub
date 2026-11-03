import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { THEME } from "../theme";

interface CardProps {
  children: React.ReactNode;
  title?: string;
  bg?: string;
  delay?: number;
}

export const Card: React.FC<CardProps> = ({
  children,
  title = "Clinic Preview",
  bg = THEME.colors.white,
  delay = 5,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame: frame - delay,
    fps,
    config: { damping: 14, stiffness: 140 },
  });

  return (
    <div
      style={{
        position: "absolute",
        top: 240,
        left: 45,
        right: 45,
        height: 620,
        backgroundColor: bg,
        border: `4px solid ${THEME.colors.ink}`,
        borderRadius: 28,
        boxShadow: THEME.shadowLg,
        overflow: "hidden",
        zIndex: 30,
        display: "flex",
        flexDirection: "column",
        transform: `scale(${entrance}) translateY(${(1 - entrance) * 30}px)`,
      }}
    >
      {/* Header Bar */}
      <div
        style={{
          height: 48,
          backgroundColor: "#F1F5F9",
          borderBottom: `3px solid ${THEME.colors.ink}`,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 18px",
        }}
      >
        <div style={{ display: "flex", gap: 8 }}>
          <div style={{ width: 14, height: 14, borderRadius: "50%", backgroundColor: "#EF4444", border: "2px solid #0F172A" }} />
          <div style={{ width: 14, height: 14, borderRadius: "50%", backgroundColor: "#F59E0B", border: "2px solid #0F172A" }} />
          <div style={{ width: 14, height: 14, borderRadius: "50%", backgroundColor: "#10B981", border: "2px solid #0F172A" }} />
        </div>
        <div
          style={{
            fontSize: 16,
            fontWeight: 700,
            color: THEME.colors.muted,
            fontFamily: "monospace",
          }}
        >
          {title}
        </div>
        <div style={{ width: 44 }} />
      </div>

      {/* Body */}
      <div
        style={{
          flex: 1,
          padding: "24px",
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
  );
};
