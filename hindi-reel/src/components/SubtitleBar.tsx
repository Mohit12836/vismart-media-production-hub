import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { THEME } from "../theme";

interface SubtitleBarProps {
  text: string;
  highlights: string[];
  durationInFrames: number;
}

export const SubtitleBar: React.FC<SubtitleBarProps> = ({
  text,
  highlights,
  durationInFrames,
}) => {
  const frame = useCurrentFrame();
  const words = text.split(" ");
  const totalWords = words.length;

  const activeWordIndex = Math.min(
    totalWords - 1,
    Math.max(
      0,
      Math.floor(
        interpolate(frame, [6, durationInFrames - 6], [0, totalWords - 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        })
      )
    )
  );

  return (
    <div
      style={{
        position: "absolute",
        left: 40,
        right: 40,
        bottom: 80,
        height: 145,
        backgroundColor: "rgba(19, 27, 46, 0.95)",
        border: "1px solid rgba(255, 255, 255, 0.15)",
        backdropFilter: "blur(20px)",
        borderRadius: 24,
        padding: "16px 20px",
        boxShadow: "0 15px 35px rgba(0,0,0,0.5)",
        zIndex: 50,
        display: "flex",
        flexWrap: "wrap",
        alignItems: "center",
        justifyContent: "center",
        alignContent: "center",
        gap: "6px 8px",
      }}
    >
      {words.map((word, i) => {
        const isActive = i === activeWordIndex;
        const isPast = i < activeWordIndex;
        const isHighlight = highlights.some((h) =>
          word.toLowerCase().includes(h.toLowerCase())
        );

        return (
          <span
            key={i}
            style={{
              fontFamily: "'Poppins', sans-serif",
              fontSize: 24,
              fontWeight: 800,
              padding: "2px 8px",
              borderRadius: 8,
              backgroundColor: isActive
                ? THEME.colors.yellow
                : isHighlight && isPast
                ? "rgba(0, 242, 254, 0.2)"
                : "transparent",
              color: isActive
                ? "#000000"
                : isPast
                ? "#FFFFFF"
                : "rgba(255, 255, 255, 0.35)",
              transform: isActive ? "scale(1.1)" : "scale(1)",
              boxShadow: isActive ? "0 0 15px rgba(250, 204, 21, 0.6)" : "none",
              display: "inline-block",
            }}
          >
            {word}
          </span>
        );
      })}
    </div>
  );
};
