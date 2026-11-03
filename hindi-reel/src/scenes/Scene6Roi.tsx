import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { THEME } from "../theme";
import { Sticker } from "../components/Sticker";

export const Scene6Roi: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const calcSpring = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 150 },
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        gap: 14,
        justifyContent: "center",
        transform: `scale(${calcSpring})`,
      }}
    >
      <Sticker text="💰 100% FREE ROI" color={THEME.colors.yellow} top={-12} right={-8} rotate={8} appearAt={10} />

      {/* Maths Box */}
      <div
        style={{
          width: "100%",
          backgroundColor: THEME.colors.tintYellow,
          border: `3px solid ${THEME.colors.ink}`,
          borderRadius: 22,
          padding: "18px",
          boxShadow: "4px 4px 0px #0F172A",
        }}
      >
        <div style={{ fontSize: 18, fontWeight: 900, color: THEME.colors.ink, borderBottom: "2px solid #E2E8F0", paddingBottom: 8 }}>
          📊 SIMPLE CLINIC MATHS:
        </div>

        <div style={{ marginTop: 12, display: "flex", flexDirection: "column", gap: 8 }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 16, fontWeight: 800 }}>
            <span>🦷 2 Root Canals (RCT)</span>
            <span style={{ color: THEME.colors.green }}>+₹8,000</span>
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 16, fontWeight: 800 }}>
            <span>💎 1 Dental Implant</span>
            <span style={{ color: THEME.colors.green }}>+₹25,000</span>
          </div>
          <div
            style={{
              borderTop: "2px dashed #0F172A",
              paddingTop: 8,
              marginTop: 4,
              display: "flex",
              justifyContent: "space-between",
              fontSize: 20,
              fontWeight: 900,
            }}
          >
            <span>TOTAL NEW PROFIT:</span>
            <span style={{ color: THEME.colors.green }}>₹33,000+</span>
          </div>
        </div>
      </div>

      <div
        style={{
          backgroundColor: THEME.colors.tintGreen,
          border: `3px solid ${THEME.colors.green}`,
          borderRadius: 18,
          padding: "12px",
          textAlign: "center",
          fontWeight: 900,
          fontSize: 17,
          color: THEME.colors.green,
        }}
      >
        ✅ Pehle Hi Mahine Me Website Ka Kharcha 100% Vasool!
      </div>
    </div>
  );
};
