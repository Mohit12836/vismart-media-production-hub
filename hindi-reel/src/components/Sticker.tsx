import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { THEME } from "../theme";

interface StickerProps {
  text: string;
  color?: string;
  rotate?: number;
  appearAt?: number;
  textColor?: string;
  top?: number | string;
  left?: number | string;
  right?: number | string;
  bottom?: number | string;
}

export const Sticker: React.FC<StickerProps> = ({
  text,
  color = THEME.colors.yellow,
  rotate = -8,
  appearAt = 10,
  textColor = THEME.colors.ink,
  top,
  left,
  right,
  bottom,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame: frame - appearAt,
    fps,
    config: { damping: 10, stiffness: 220 },
  });

  if (frame < appearAt) return null;

  return (
    <div
      style={{
        position: "absolute",
        top,
        left,
        right,
        bottom,
        backgroundColor: color,
        color: textColor,
        border: `3px solid ${THEME.colors.ink}`,
        borderRadius: 14,
        padding: "8px 18px",
        fontFamily: "'Poppins', sans-serif",
        fontSize: 22,
        fontWeight: 900,
        boxShadow: "4px 4px 0px #0F172A",
        transform: `scale(${entrance}) rotate(${rotate}deg)`,
        zIndex: 60,
        whiteSpace: "nowrap",
      }}
    >
      {text}
    </div>
  );
};
