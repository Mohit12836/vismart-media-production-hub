import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { THEME } from "../theme";

export type MascotPose = "explain" | "think" | "surprise" | "point";

export const Mascot: React.FC<{ pose: MascotPose }> = ({ pose }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Gentle floating animation
  const bobbing = Math.sin(frame / 8) * 6;

  // Spring entrance
  const entrance = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 120 },
  });

  return (
    <div
      style={{
        position: "absolute",
        left: 36,
        bottom: 70,
        width: 170,
        height: 190,
        transform: `translateY(${bobbing}px) scale(${entrance})`,
        zIndex: 50,
      }}
    >
      <svg
        viewBox="0 0 160 180"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style={{ width: "100%", height: "100%", filter: "drop-shadow(4px 4px 0px #0F172A)" }}
      >
        {/* Blue Cap */}
        <path
          d="M35 50 C35 25, 125 25, 125 50 Z"
          fill={THEME.colors.cyan}
          stroke={THEME.colors.ink}
          strokeWidth="4"
        />
        {/* Cap Visor */}
        <path
          d="M100 48 Q150 48 145 62 L105 60 Z"
          fill={THEME.colors.blue}
          stroke={THEME.colors.ink}
          strokeWidth="3"
        />

        {/* Head */}
        <rect
          x="30"
          y="50"
          width="100"
          height="80"
          rx="24"
          fill="#FFFFFF"
          stroke={THEME.colors.ink}
          strokeWidth="4"
        />

        {/* Cheeks */}
        <circle cx="46" cy="98" r="7" fill={THEME.colors.tintPink} />
        <circle cx="114" cy="98" r="7" fill={THEME.colors.tintPink} />

        {/* Eyes based on pose */}
        {pose === "surprise" ? (
          <>
            <circle cx="58" cy="80" r="12" fill={THEME.colors.ink} />
            <circle cx="102" cy="80" r="12" fill={THEME.colors.ink} />
            <circle cx="56" cy="77" r="4" fill="#FFFFFF" />
            <circle cx="100" cy="77" r="4" fill="#FFFFFF" />
            {/* O mouth */}
            <circle cx="80" cy="104" r="8" fill={THEME.colors.pink} stroke={THEME.colors.ink} strokeWidth="2.5" />
          </>
        ) : pose === "think" ? (
          <>
            <path d="M48 76 Q58 68 68 76" stroke={THEME.colors.ink} strokeWidth="4" fill="none" strokeLinecap="round" />
            <circle cx="102" cy="78" r="8" fill={THEME.colors.ink} />
            <circle cx="100" cy="76" r="2.5" fill="#FFFFFF" />
            {/* Smirk */}
            <path d="M72 104 Q84 100 92 105" stroke={THEME.colors.ink} strokeWidth="3" fill="none" strokeLinecap="round" />
          </>
        ) : (
          <>
            {/* Friendly big eyes */}
            <circle cx="58" cy="80" r="9" fill={THEME.colors.ink} />
            <circle cx="102" cy="80" r="9" fill={THEME.colors.ink} />
            <circle cx="56" cy="77" r="3" fill="#FFFFFF" />
            <circle cx="100" cy="77" r="3" fill="#FFFFFF" />
            {/* Big Smile */}
            <path
              d="M62 98 Q80 116 98 98"
              stroke={THEME.colors.ink}
              strokeWidth="3.5"
              fill={THEME.colors.tintPink}
              strokeLinecap="round"
            />
          </>
        )}

        {/* Body */}
        <path
          d="M48 132 L112 132 L120 175 L40 175 Z"
          fill={THEME.colors.cyan}
          stroke={THEME.colors.ink}
          strokeWidth="4"
        />

        {/* Tie or badge */}
        <polygon points="80,132 86,150 80,165 74,150" fill={THEME.colors.yellow} stroke={THEME.colors.ink} strokeWidth="2" />

        {/* Hands according to pose */}
        {pose === "point" ? (
          <path
            d="M120 145 Q150 120 155 100"
            stroke={THEME.colors.ink}
            strokeWidth="5"
            strokeLinecap="round"
            fill="none"
          />
        ) : pose === "think" ? (
          <path
            d="M110 148 Q118 120 102 110"
            stroke={THEME.colors.ink}
            strokeWidth="5"
            strokeLinecap="round"
            fill="none"
          />
        ) : pose === "surprise" ? (
          <>
            <path d="M42 145 Q20 125 24 105" stroke={THEME.colors.ink} strokeWidth="5" strokeLinecap="round" fill="none" />
            <path d="M118 145 Q140 125 136 105" stroke={THEME.colors.ink} strokeWidth="5" strokeLinecap="round" fill="none" />
          </>
        ) : (
          <path
            d="M42 145 Q25 140 32 120"
            stroke={THEME.colors.ink}
            strokeWidth="5"
            strokeLinecap="round"
            fill="none"
          />
        )}
      </svg>
    </div>
  );
};
