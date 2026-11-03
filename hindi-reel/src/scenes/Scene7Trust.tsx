import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { THEME } from "../theme";
import { Sticker } from "../components/Sticker";

export const Scene7Trust: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const b1 = spring({ frame: frame - 2, fps, config: { damping: 12, stiffness: 160 } });
  const b2 = spring({ frame: frame - 8, fps, config: { damping: 12, stiffness: 160 } });
  const b3 = spring({ frame: frame - 14, fps, config: { damping: 12, stiffness: 160 } });
  const b4 = spring({ frame: frame - 20, fps, config: { damping: 12, stiffness: 160 } });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: 12,
        alignContent: "center",
      }}
    >
      <Sticker text="⚡ 100% RELIABLE" color={THEME.colors.cyan} textColor="#FFF" top={-12} left={-8} rotate={-6} appearAt={6} />

      {/* Badge 1 */}
      <div
        style={{
          backgroundColor: THEME.colors.tintCyan,
          border: `3px solid ${THEME.colors.cyan}`,
          borderRadius: 18,
          padding: "16px 12px",
          textAlign: "center",
          boxShadow: "3px 3px 0px #0F172A",
          transform: `scale(${b1})`,
        }}
      >
        <div style={{ fontSize: 30 }}>🚀</div>
        <div style={{ fontSize: 16, fontWeight: 900, color: THEME.colors.ink, marginTop: 4 }}>1-Sec Fast</div>
        <div style={{ fontSize: 12, fontWeight: 700, color: THEME.colors.muted }}>Ultra Lightning Speed</div>
      </div>

      {/* Badge 2 */}
      <div
        style={{
          backgroundColor: THEME.colors.tintPink,
          border: `3px solid ${THEME.colors.pink}`,
          borderRadius: 18,
          padding: "16px 12px",
          textAlign: "center",
          boxShadow: "3px 3px 0px #0F172A",
          transform: `scale(${b2})`,
        }}
      >
        <div style={{ fontSize: 30 }}>📱</div>
        <div style={{ fontSize: 16, fontWeight: 900, color: THEME.colors.ink, marginTop: 4 }}>100% Mobile</div>
        <div style={{ fontSize: 12, fontWeight: 700, color: THEME.colors.muted }}>Fluid on Every Phone</div>
      </div>

      {/* Badge 3 */}
      <div
        style={{
          backgroundColor: THEME.colors.tintGreen,
          border: `3px solid ${THEME.colors.green}`,
          borderRadius: 18,
          padding: "16px 12px",
          textAlign: "center",
          boxShadow: "3px 3px 0px #0F172A",
          transform: `scale(${b3})`,
        }}
      >
        <div style={{ fontSize: 30 }}>🔍</div>
        <div style={{ fontSize: 16, fontWeight: 900, color: THEME.colors.ink, marginTop: 4 }}>Google SEO</div>
        <div style={{ fontSize: 12, fontWeight: 700, color: THEME.colors.muted }}>Rank #1 in Your City</div>
      </div>

      {/* Badge 4 */}
      <div
        style={{
          backgroundColor: THEME.colors.tintYellow,
          border: `3px solid ${THEME.colors.orange}`,
          borderRadius: 18,
          padding: "16px 12px",
          textAlign: "center",
          boxShadow: "3px 3px 0px #0F172A",
          transform: `scale(${b4})`,
        }}
      >
        <div style={{ fontSize: 30 }}>👨‍💻</div>
        <div style={{ fontSize: 16, fontWeight: 900, color: THEME.colors.ink, marginTop: 4 }}>1-Year Support</div>
        <div style={{ fontSize: 12, fontWeight: 700, color: THEME.colors.muted }}>Free Maintenance</div>
      </div>
    </div>
  );
};
