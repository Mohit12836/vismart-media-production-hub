import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { THEME } from "../theme";
import { CompositionProps } from "../schema";

export const Scene5NightBooking: React.FC<Partial<CompositionProps>> = ({
  creatorName = "MOHIT JAIN",
  phoneNumber = "6263879076",
  professionTitle = "HEALTHCARE WEBSITE ARCHITECT",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pulse = Math.sin(frame / 4) * 0.04 + 1.0;
  const cardSpring = spring({ frame, fps, config: { damping: 14, stiffness: 180 } });

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
      {/* VIP Profile Card */}
      <div
        style={{
          width: "95%",
          background: "linear-gradient(135deg, rgba(0, 242, 254, 0.15) 0%, rgba(19, 27, 46, 0.95) 100%)",
          border: "2px solid #00F2FE",
          borderRadius: 28,
          padding: "24px 20px",
          textAlign: "center",
          boxShadow: "0 0 35px rgba(0, 242, 254, 0.3)",
        }}
      >
        <div
          style={{
            display: "inline-block",
            backgroundColor: "rgba(0, 242, 254, 0.2)",
            border: "1px solid #00F2FE",
            borderRadius: 999,
            padding: "4px 16px",
            fontSize: 14,
            fontWeight: 800,
            color: THEME.colors.cyan,
            letterSpacing: "0.06em",
          }}
        >
          {professionTitle}
        </div>

        <div
          style={{
            fontSize: 36,
            fontWeight: 900,
            color: "#FFFFFF",
            marginTop: 10,
            letterSpacing: "0.02em",
          }}
        >
          {creatorName}
        </div>

        {/* Big Pulsing Number Box */}
        <div
          style={{
            marginTop: 14,
            backgroundColor: "rgba(16, 185, 129, 0.18)",
            border: "2px solid #10B981",
            borderRadius: 20,
            padding: "14px 16px",
            transform: `scale(${pulse})`,
            boxShadow: "0 0 25px rgba(16, 185, 129, 0.3)",
          }}
        >
          <div style={{ fontSize: 13, fontWeight: 800, color: "#86EFAC", letterSpacing: "0.05em" }}>
            CALL OR WHATSAPP NOW:
          </div>
          <div
            style={{
              fontFamily: "monospace",
              fontSize: 36,
              fontWeight: 900,
              color: "#10B981",
              letterSpacing: "0.06em",
              marginTop: 2,
            }}
          >
            📞 {phoneNumber}
          </div>
        </div>
      </div>

      {/* Buttons */}
      <div style={{ display: "flex", gap: 12, width: "95%" }}>
        <div
          style={{
            flex: 1,
            backgroundColor: "#25D366",
            color: "#000",
            borderRadius: 16,
            padding: "14px",
            textAlign: "center",
            fontWeight: 900,
            fontSize: 17,
            boxShadow: "0 10px 20px rgba(37, 211, 102, 0.3)",
          }}
        >
          💬 WhatsApp
        </div>
        <div
          style={{
            flex: 1,
            backgroundColor: "#00F2FE",
            color: "#000",
            borderRadius: 16,
            padding: "14px",
            textAlign: "center",
            fontWeight: 900,
            fontSize: 17,
            boxShadow: "0 10px 20px rgba(0, 242, 254, 0.3)",
          }}
        >
          📱 Call Demo
        </div>
      </div>
    </div>
  );
};
