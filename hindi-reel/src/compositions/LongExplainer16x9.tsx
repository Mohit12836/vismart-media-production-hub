import React from "react";
import {
  AbsoluteFill,
  Audio,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export const LONG_EXPLAINER_DURATION = 900; // 30 seconds @ 30fps (Sample long landscape explainer)

export interface LongExplainerProps {
  headline?: string;
  subheadline?: string;
  clientName?: string;
  phoneNumber?: string;
  brandName?: string;
}

export const LongExplainer16x9: React.FC<LongExplainerProps> = ({
  headline = "HOW TOP DENTAL CLINICS ATTRACT 50+ PATIENTS MONTHLY",
  subheadline = "The Complete 2026 Apple-Grade Healthcare Booking Architecture",
  clientName = "MOHIT JAIN",
  phoneNumber = "6263879076",
  brandName = "VISMART STUDIO",
}) => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#FFFFFF",
        color: "#0F172A",
        fontFamily: "'Segoe UI', Roboto, 'Noto Sans Devanagari', sans-serif",
        overflow: "hidden",
      }}
    >
      {/* Background Audio */}
      <Audio src={staticFile("audio/bg.mp3")} volume={0.6} />

      {/* Decorative Grid Lines */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: "radial-gradient(#CBD5E1 1px, transparent 1px)",
          backgroundSize: "32px 32px",
          opacity: 0.5,
        }}
      />

      {/* Top Header Bar */}
      <div
        style={{
          position: "absolute",
          top: 32,
          left: 48,
          right: 48,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          borderBottom: "2px solid #0F172A",
          paddingBottom: 20,
          zIndex: 50,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <div
            style={{
              width: 44,
              height: 44,
              borderRadius: 10,
              backgroundColor: "#0F172A",
              color: "#FFFFFF",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontWeight: 900,
              fontSize: 22,
            }}
          >
            V
          </div>
          <div>
            <div style={{ fontSize: 20, fontWeight: 900, letterSpacing: -0.5 }}>{brandName}</div>
            <div style={{ fontSize: 13, color: "#64748B", fontWeight: 700 }}>HEALTHCARE SYSTEMS DIVISION</div>
          </div>
        </div>

        <div
          style={{
            padding: "8px 20px",
            borderRadius: 999,
            border: "2px solid #0F172A",
            backgroundColor: "#F1F5F9",
            fontWeight: 800,
            fontSize: 14,
            display: "flex",
            alignItems: "center",
            gap: 8,
          }}
        >
          <span style={{ width: 8, height: 8, borderRadius: "50%", backgroundColor: "#10B981" }} />
          16:9 4K SYSTEM MASTER
        </div>
      </div>

      {/* ================================================================ */}
      {/* ACT 1: INTRO HEADLINE (0 - 240 frames / 8s) */}
      {/* ================================================================ */}
      <Sequence from={0} durationInFrames={250}>
        <Audio src={staticFile("audio/whoosh.mp3")} volume={0.8} />
        <Act1Intro headline={headline} subheadline={subheadline} />
      </Sequence>

      {/* ================================================================ */}
      {/* ACT 2: ARCHITECTURE COMPARISON (240 - 580 frames / 11s) */}
      {/* ================================================================ */}
      <Sequence from={240} durationInFrames={350}>
        <Audio src={staticFile("audio/pop.mp3")} volume={0.8} />
        <Act2Comparison />
      </Sequence>

      {/* ================================================================ */}
      {/* ACT 3: DASHBOARD METRICS & CTA (580 - 900 frames / 11s) */}
      {/* ================================================================ */}
      <Sequence from={580} durationInFrames={320}>
        <Audio src={staticFile("audio/ding.mp3")} volume={0.9} />
        <Act3MetricsCTA clientName={clientName} phoneNumber={phoneNumber} />
      </Sequence>
    </AbsoluteFill>
  );
};

const Act1Intro: React.FC<{ headline: string; subheadline: string }> = ({ headline, subheadline }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const enter = spring({ frame, fps, config: { stiffness: 220, damping: 20 } });
  const opacity = interpolate(frame, [0, 20], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        padding: "0 100px",
        textAlign: "center",
        opacity,
        transform: `scale(${enter})`,
      }}
    >
      <div
        style={{
          display: "inline-block",
          padding: "8px 24px",
          borderRadius: 999,
          backgroundColor: "#EF4444",
          color: "#FFFFFF",
          fontSize: 16,
          fontWeight: 900,
          letterSpacing: 2,
          marginBottom: 24,
          border: "2px solid #0F172A",
          boxShadow: "3px 3px 0px #0F172A",
        }}
      >
        ⚠️ 2026 CLINIC EXPANSION BLUEPRINT
      </div>

      <h1
        style={{
          fontSize: 64,
          fontWeight: 900,
          lineHeight: 1.1,
          letterSpacing: -2,
          maxWidth: 1400,
          marginBottom: 24,
        }}
      >
        {headline}
      </h1>

      <p
        style={{
          fontSize: 26,
          color: "#475569",
          fontWeight: 600,
          maxWidth: 1000,
        }}
      >
        {subheadline}
      </p>
    </AbsoluteFill>
  );
};

const Act2Comparison: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const enterLeft = spring({ frame, fps, config: { stiffness: 200, damping: 22 } });
  const enterRight = spring({ frame: frame - 15, fps, config: { stiffness: 200, damping: 22 } });

  return (
    <AbsoluteFill
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        padding: "0 80px",
      }}
    >
      <div style={{ textAlign: "center", marginBottom: 36 }}>
        <h2 style={{ fontSize: 44, fontWeight: 900, letterSpacing: -1 }}>
          TRADITIONAL WEBSITE VS VISMART AI ARCHITECTURE
        </h2>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 40 }}>
        {/* Left: Traditional */}
        <div
          style={{
            padding: 36,
            borderRadius: 24,
            backgroundColor: "#FEF2F2",
            border: "2px solid #0F172A",
            boxShadow: "4px 4px 0px #0F172A",
            transform: `translateX(${(1 - enterLeft) * -80}px)`,
            opacity: enterLeft,
          }}
        >
          <div style={{ fontSize: 24, fontWeight: 900, color: "#DC2626", marginBottom: 16 }}>
            ❌ Typical ₹5,000 Template Website
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 14, fontSize: 19, color: "#475569", fontWeight: 600 }}>
            <div>• 9-second slow loading on 4G mobile devices</div>
            <div>• Zero WhatsApp integration or online deposit collection</div>
            <div>• 85% of visitors leave without booking</div>
          </div>
        </div>

        {/* Right: Vismart */}
        <div
          style={{
            padding: 36,
            borderRadius: 24,
            backgroundColor: "#F0FDF4",
            border: "2px solid #0F172A",
            boxShadow: "6px 6px 0px #0F172A",
            transform: `translateX(${(1 - enterRight) * 80}px)`,
            opacity: enterRight,
          }}
        >
          <div style={{ fontSize: 24, fontWeight: 900, color: "#15803D", marginBottom: 16 }}>
            ✅ Vismart Apple-Grade AI Clinic Platform
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 14, fontSize: 19, color: "#166534", fontWeight: 600 }}>
            <div>• 0.4s instant auto-fit across mobile, iPad, and desktop</div>
            <div>• 1-Click WhatsApp appointment booking + token deposit</div>
            <div>• +310% higher conversion of high-paying dental patients</div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Act3MetricsCTA: React.FC<{ clientName: string; phoneNumber: string }> = ({ clientName, phoneNumber }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const enter = spring({ frame, fps, config: { stiffness: 220, damping: 20 } });
  const metric = Math.floor(interpolate(frame, [0, 80], [0, 485000], { extrapolateRight: "clamp" }));

  return (
    <AbsoluteFill
      style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        alignItems: "center",
        padding: "0 80px",
        gap: 60,
        transform: `scale(${enter})`,
      }}
    >
      {/* Left: Odometer Metric */}
      <div
        style={{
          padding: 44,
          borderRadius: 28,
          backgroundColor: "#F8FAFC",
          border: "2px solid #0F172A",
          boxShadow: "6px 6px 0px #0F172A",
        }}
      >
        <div style={{ fontSize: 16, fontWeight: 900, color: "#64748B", letterSpacing: 2, marginBottom: 8 }}>
          MONTHLY CLINIC APPOINTMENT VALUE
        </div>
        <div
          style={{
            fontSize: 72,
            fontWeight: 900,
            color: "#0F172A",
            letterSpacing: -2,
            lineHeight: 1,
            marginBottom: 12,
          }}
        >
          ₹{metric.toLocaleString("en-IN")}
        </div>
        <div style={{ fontSize: 20, fontWeight: 800, color: "#16A34A" }}>
          ▲ +310% Growth Generated via Automated Funnel
        </div>
      </div>

      {/* Right: CTA Box */}
      <div
        style={{
          padding: 44,
          borderRadius: 28,
          backgroundColor: "#0F172A",
          color: "#FFFFFF",
          border: "2px solid #0F172A",
          boxShadow: "6px 6px 0px #2563EB",
          textAlign: "center",
        }}
      >
        <div
          style={{
            display: "inline-block",
            padding: "6px 18px",
            borderRadius: 999,
            backgroundColor: "rgba(255, 255, 255, 0.12)",
            color: "#38BDF8",
            fontSize: 13,
            fontWeight: 900,
            letterSpacing: 2,
            marginBottom: 18,
          }}
        >
          LIMITED AVAILABILITY • 48-HOUR LAUNCH
        </div>

        <h2 style={{ fontSize: 36, fontWeight: 900, lineHeight: 1.2, marginBottom: 24 }}>
          BUILD YOUR AUTOMATED CLINIC WEBSITE
        </h2>

        <div
          style={{
            padding: "18px 28px",
            borderRadius: 18,
            backgroundColor: "#22C55E",
            color: "#052E16",
            fontSize: 26,
            fontWeight: 900,
            letterSpacing: 0.5,
            marginBottom: 20,
            boxShadow: "0 10px 25px rgba(34, 197, 94, 0.4)",
          }}
        >
          📱 WhatsApp: {phoneNumber}
        </div>

        <div style={{ fontSize: 18, color: "#94A3B8", fontWeight: 700 }}>
          Chief Architect: <span style={{ color: "#FFFFFF" }}>{clientName}</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
