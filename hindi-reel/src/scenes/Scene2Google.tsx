import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { THEME } from "../theme";

export const Scene2Google: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const phoneSpring = spring({ frame, fps, config: { damping: 14, stiffness: 180 } });

  const query = "Best Dentist Near Me 📍";
  const typedLen = Math.min(query.length, Math.floor(frame / 1.5));
  const displayed = query.slice(0, typedLen);

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 16,
        transform: `scale(${phoneSpring})`,
      }}
    >
      {/* Smartphone Search Simulation */}
      <div
        style={{
          width: "94%",
          backgroundColor: "#0F172A",
          border: "1.5px solid rgba(255, 255, 255, 0.15)",
          borderRadius: 24,
          padding: "20px 16px",
          display: "flex",
          flexDirection: "column",
          gap: 14,
          boxShadow: "0 20px 40px rgba(0,0,0,0.6)",
        }}
      >
        {/* Search Bar */}
        <div
          style={{
            backgroundColor: "rgba(255, 255, 255, 0.08)",
            border: "1px solid rgba(0, 242, 254, 0.4)",
            borderRadius: 999,
            padding: "12px 18px",
            display: "flex",
            alignItems: "center",
            gap: 10,
          }}
        >
          <span style={{ fontSize: 20 }}>🔍</span>
          <span style={{ fontSize: 18, fontWeight: 700, color: "#FFFFFF", fontFamily: "monospace" }}>
            {displayed}
            {frame % 12 < 6 && <span style={{ color: THEME.colors.cyan }}>|</span>}
          </span>
        </div>

        {/* Competitor with Website - Top Result */}
        <div
          style={{
            backgroundColor: "rgba(16, 185, 129, 0.12)",
            border: "1px solid #10B981",
            borderRadius: 18,
            padding: "14px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <div>
            <div style={{ fontSize: 17, fontWeight: 800, color: "#FFFFFF" }}>Apex Dental Care ⭐ 4.9</div>
            <div style={{ fontSize: 13, fontWeight: 700, color: "#10B981", marginTop: 2 }}>
              ✓ Website Live • 1-Click WhatsApp Ready
            </div>
          </div>
          <div
            style={{
              backgroundColor: "#10B981",
              color: "#000",
              fontWeight: 900,
              fontSize: 12,
              padding: "6px 12px",
              borderRadius: 8,
            }}
          >
            PATIENT BOOKED!
          </div>
        </div>

        {/* Your Clinic Alert */}
        <div
          style={{
            backgroundColor: "rgba(255, 51, 102, 0.1)",
            border: "1px dashed #FF3366",
            borderRadius: 18,
            padding: "14px",
            textAlign: "center",
          }}
        >
          <div style={{ fontSize: 15, fontWeight: 800, color: "#FF3366" }}>
            ❌ No Website = Patient Never Found You!
          </div>
        </div>
      </div>
    </div>
  );
};
