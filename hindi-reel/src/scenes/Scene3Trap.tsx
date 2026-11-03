import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { THEME } from "../theme";

export const Scene3Trap: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const bubble1 = spring({ frame: frame - 2, fps, config: { damping: 14, stiffness: 180 } });
  const bubble2 = spring({ frame: frame - 10, fps, config: { damping: 14, stiffness: 180 } });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        gap: 16,
        justifyContent: "center",
      }}
    >
      {/* WhatsApp Simulation Card */}
      <div
        style={{
          width: "100%",
          backgroundColor: "#075E54",
          border: "1.5px solid rgba(255, 255, 255, 0.2)",
          borderRadius: 22,
          padding: "16px",
          display: "flex",
          alignItems: "center",
          gap: 12,
        }}
      >
        <div style={{ fontSize: 32 }}>💬</div>
        <div>
          <div style={{ fontSize: 18, fontWeight: 900, color: "#FFFFFF" }}>1-Click WhatsApp Appointment</div>
          <div style={{ fontSize: 13, color: "#86EFAC" }}>Direct booking on Doctor's phone</div>
        </div>
      </div>

      {/* Patient Chat Message */}
      <div
        style={{
          width: "88%",
          alignSelf: "flex-end",
          backgroundColor: "#128C7E",
          color: "#FFFFFF",
          borderRadius: "18px 18px 4px 18px",
          padding: "14px 16px",
          boxShadow: "0 10px 20px rgba(0,0,0,0.3)",
          transform: `scale(${bubble1})`,
        }}
      >
        <div style={{ fontSize: 16, fontWeight: 800 }}>"Doctor saab, kal subah 11 baje Root Canal ka appointment confirm kar do please!"</div>
        <div style={{ fontSize: 12, color: "#A7F3D0", textAlign: "right", marginTop: 4 }}>11:32 PM ✓✓</div>
      </div>

      {/* Before / After Trust Badge */}
      <div
        style={{
          width: "100%",
          backgroundColor: "rgba(0, 242, 254, 0.1)",
          border: "1px solid #00F2FE",
          borderRadius: 18,
          padding: "14px",
          textAlign: "center",
          transform: `scale(${bubble2})`,
        }}
      >
        <div style={{ fontSize: 16, fontWeight: 900, color: THEME.colors.cyan }}>
          ✨ Before-After Smile Gallery = 100% Instant Trust!
        </div>
      </div>
    </div>
  );
};
