import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { THEME } from "../theme";
import { Sticker } from "../components/Sticker";

export const Scene8Cta: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pulse = Math.sin(frame / 4) * 0.05 + 1.0;

  const cardSpring = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 140 },
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        gap: 16,
        justifyContent: "center",
        alignItems: "center",
        transform: `scale(${cardSpring})`,
      }}
    >
      <Sticker text="🎁 FREE LIVE DEMO" color={THEME.colors.yellow} top={-12} right={-8} rotate={-6} appearAt={6} />

      {/* Main Calling Profile Card */}
      <div
        style={{
          width: "95%",
          backgroundColor: "#FFFFFF",
          border: `3.5px solid ${THEME.colors.ink}`,
          borderRadius: 24,
          padding: "20px 18px",
          textAlign: "center",
          boxShadow: "6px 6px 0px #0F172A",
        }}
      >
        <div
          style={{
            display: "inline-block",
            backgroundColor: THEME.colors.tintCyan,
            border: `2px solid ${THEME.colors.cyan}`,
            borderRadius: 999,
            padding: "4px 16px",
            fontSize: 14,
            fontWeight: 800,
            color: THEME.colors.cyan,
          }}
        >
          HEALTHCARE WEBSITE SPECIALIST
        </div>

        <div
          style={{
            fontSize: 32,
            fontWeight: 900,
            color: THEME.colors.ink,
            marginTop: 8,
          }}
        >
          MOHIT JAIN
        </div>

        {/* Big Phone Number with Glow / Pulse */}
        <div
          style={{
            marginTop: 10,
            backgroundColor: "#F0FDF4",
            border: `3px solid ${THEME.colors.green}`,
            borderRadius: 18,
            padding: "12px 14px",
            transform: `scale(${pulse})`,
          }}
        >
          <div style={{ fontSize: 13, fontWeight: 800, color: THEME.colors.muted }}>
            DIRECT CALL & WHATSAPP:
          </div>
          <div
            style={{
              fontFamily: "monospace",
              fontSize: 32,
              fontWeight: 900,
              color: THEME.colors.green,
              letterSpacing: "0.05em",
            }}
          >
            📞 6263879076
          </div>
        </div>
      </div>

      {/* Action Buttons Row */}
      <div style={{ display: "flex", gap: 12, width: "95%" }}>
        <div
          style={{
            flex: 1,
            backgroundColor: THEME.colors.whatsapp,
            color: "#FFF",
            border: `3px solid ${THEME.colors.ink}`,
            borderRadius: 16,
            padding: "12px",
            textAlign: "center",
            fontWeight: 900,
            fontSize: 16,
            boxShadow: "3px 3px 0px #0F172A",
          }}
        >
          💬 WhatsApp Now
        </div>
        <div
          style={{
            flex: 1,
            backgroundColor: THEME.colors.cyan,
            color: "#FFF",
            border: `3px solid ${THEME.colors.ink}`,
            borderRadius: 16,
            padding: "12px",
            textAlign: "center",
            fontWeight: 900,
            fontSize: 16,
            boxShadow: "3px 3px 0px #0F172A",
          }}
        >
          📱 Call Now
        </div>
      </div>
    </div>
  );
};
