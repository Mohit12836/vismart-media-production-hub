import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { THEME } from "../theme";

export const SectionChip: React.FC<{ label: string }> = ({ label }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 220 },
  });

  return (
    <div
      style={{
        position: "absolute",
        top: 36,
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
        zIndex: 45,
        transform: `scale(${entrance})`,
      }}
    >
      <div
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 8,
          backgroundColor: "rgba(255, 255, 255, 0.08)",
          border: "1px solid rgba(255, 255, 255, 0.2)",
          backdropFilter: "blur(12px)",
          borderRadius: 999,
          padding: "8px 22px",
          fontSize: 16,
          fontWeight: 800,
          color: THEME.colors.cyan,
          letterSpacing: "0.06em",
          textTransform: "uppercase",
        }}
      >
        <span
          style={{
            width: 8,
            height: 8,
            borderRadius: "50%",
            backgroundColor: THEME.colors.cyan,
            boxShadow: "0 0 10px #00F2FE",
          }}
        />
        {label}
      </div>
    </div>
  );
};
