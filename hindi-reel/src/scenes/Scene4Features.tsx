import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { THEME } from "../theme";

export const Scene4Features: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const mathSpring = spring({ frame, fps, config: { damping: 14, stiffness: 180 } });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        gap: 16,
        justifyContent: "center",
        transform: `scale(${mathSpring})`,
      }}
    >
      {/* Profit Calculator */}
      <div
        style={{
          width: "100%",
          background: "linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(19, 27, 46, 0.95) 100%)",
          border: "1.5px solid rgba(245, 158, 11, 0.4)",
          borderRadius: 24,
          padding: "20px",
          boxShadow: "0 15px 35px rgba(0,0,0,0.5)",
        }}
      >
        <div style={{ fontSize: 17, fontWeight: 900, color: THEME.colors.gold, borderBottom: "1px solid rgba(255,255,255,0.1)", paddingBottom: 10 }}>
          📊 CLINIC REVENUE MATHS:
        </div>

        <div style={{ marginTop: 14, display: "flex", flexDirection: "column", gap: 10 }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 17, fontWeight: 800, color: "#FFFFFF" }}>
            <span>🦷 2 Root Canals (RCT)</span>
            <span style={{ color: "#10B981" }}>+₹8,000</span>
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 17, fontWeight: 800, color: "#FFFFFF" }}>
            <span>💎 1 Dental Implant</span>
            <span style={{ color: "#10B981" }}>+₹25,000</span>
          </div>

          <div
            style={{
              borderTop: "1px dashed rgba(255, 255, 255, 0.2)",
              paddingTop: 10,
              marginTop: 6,
              display: "flex",
              justifyContent: "space-between",
              fontSize: 22,
              fontWeight: 900,
            }}
          >
            <span style={{ color: "#FFFFFF" }}>TOTAL PROFIT:</span>
            <span style={{ color: "#10B981", textShadow: "0 0 15px #10B981" }}>+₹33,000</span>
          </div>
        </div>
      </div>

      <div
        style={{
          backgroundColor: "rgba(16, 185, 129, 0.15)",
          border: "1.5px solid #10B981",
          borderRadius: 18,
          padding: "14px",
          textAlign: "center",
          fontWeight: 900,
          fontSize: 16,
          color: "#10B981",
        }}
      >
        ✅ Pehle Hi Mahine Me Website 100% Free!
      </div>
    </div>
  );
};
