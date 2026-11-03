import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { THEME } from "../theme";

export const Scene1Alert: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pulse = Math.sin(frame / 4) * 0.05 + 1.0;
  const cardSpring = spring({ frame, fps, config: { damping: 14, stiffness: 180 } });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 20,
        transform: `scale(${cardSpring})`,
      }}
    >
      {/* Top Warning Badge */}
      <div
        style={{
          backgroundColor: "rgba(255, 51, 102, 0.15)",
          border: "1px solid #FF3366",
          borderRadius: 999,
          padding: "6px 20px",
          color: "#FF3366",
          fontSize: 16,
          fontWeight: 800,
          letterSpacing: "0.08em",
        }}
      >
        ⚠️ ATTENTION ALL CLINIC OWNERS
      </div>

      {/* Main Alert Card */}
      <div
        style={{
          width: "92%",
          background: "linear-gradient(135deg, rgba(255, 51, 102, 0.12) 0%, rgba(19, 27, 46, 0.9) 100%)",
          border: "1.5px solid rgba(255, 51, 102, 0.4)",
          borderRadius: 28,
          padding: "28px 20px",
          textAlign: "center",
          boxShadow: "0 0 30px rgba(255, 51, 102, 0.2)",
          transform: `scale(${pulse})`,
        }}
      >
        <div style={{ fontSize: 44 }}>🚨</div>
        <div
          style={{
            fontSize: 26,
            fontWeight: 900,
            color: "#FFFFFF",
            marginTop: 8,
          }}
        >
          50+ PATIENTS LOST
        </div>
        <div
          style={{
            fontFamily: "monospace",
            fontSize: 50,
            fontWeight: 900,
            color: THEME.colors.red,
            textShadow: "0 0 25px rgba(255, 51, 102, 0.8)",
            marginTop: 4,
          }}
        >
          -₹2,00,000
        </div>
        <div
          style={{
            fontSize: 16,
            fontWeight: 700,
            color: THEME.colors.muted,
            marginTop: 8,
          }}
        >
          हर महीने आपके एरिया से दूसरे क्लिनिक चले जाते हैं!
        </div>
      </div>
    </div>
  );
};
