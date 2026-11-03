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

export const SILENT_KINETIC_DURATION = 420; // 14 seconds @ 30fps

export interface SilentKineticProps {
  hookText?: string;
  problemLeft?: string;
  solutionRight?: string;
  metricTarget?: number;
  clientName?: string;
  phoneNumber?: string;
  brandName?: string;
}

export const SilentKineticReel: React.FC<SilentKineticProps> = ({
  hookText = "DON'T BUILD A WEBSITE IN 2026...",
  metricTarget = 340000,
  clientName = "MOHIT JAIN",
  phoneNumber = "6263879076",
  brandName = "VISMART STUDIO",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Background subtle gradient pulse
  const bgScale = interpolate(Math.sin(frame / 20), [-1, 1], [1, 1.05]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#07090E",
        color: "#FFFFFF",
        fontFamily: "'Segoe UI', Roboto, 'Noto Sans Devanagari', sans-serif",
        overflow: "hidden",
      }}
    >
      {/* Background Music & SFX */}
      <Audio src={staticFile("audio/bg.mp3")} volume={0.8} />

      {/* Global Background Glow Orbs */}
      <div
        style={{
          position: "absolute",
          top: "15%",
          left: "50%",
          transform: `translate(-50%, -50%) scale(${bgScale})`,
          width: 500,
          height: 500,
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(0, 242, 254, 0.18) 0%, rgba(79, 70, 229, 0.08) 50%, transparent 80%)",
          filter: "blur(60px)",
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: "10%",
          left: "40%",
          width: 450,
          height: 450,
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(236, 72, 153, 0.15) 0%, transparent 70%)",
          filter: "blur(70px)",
          pointerEvents: "none",
        }}
      />

      {/* Top Permanent Branding Tag */}
      <div
        style={{
          position: "absolute",
          top: 40,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 50,
        }}
      >
        <div
          style={{
            padding: "8px 20px",
            borderRadius: 999,
            background: "rgba(255, 255, 255, 0.06)",
            border: "1px solid rgba(255, 255, 255, 0.15)",
            backdropFilter: "blur(12px)",
            fontSize: 14,
            fontWeight: 700,
            letterSpacing: 2,
            color: "#38BDF8",
            display: "flex",
            alignItems: "center",
            gap: 8,
          }}
        >
          <span style={{ width: 8, height: 8, borderRadius: "50%", backgroundColor: "#10B981" }} />
          {brandName} • 2026 SYSTEM
        </div>
      </div>

      {/* ================================================================ */}
      {/* SCENE 1: HOOK (0 - 90 frames / 3.0s) */}
      {/* ================================================================ */}
      <Sequence from={0} durationInFrames={90}>
        <Audio src={staticFile("audio/whoosh.mp3")} volume={0.9} startFrom={0} />
        <Scene1Hook hookText={hookText} />
      </Sequence>

      {/* ================================================================ */}
      {/* SCENE 2: BEFORE VS AFTER COMPARISON (90 - 200 frames / 3.6s) */}
      {/* ================================================================ */}
      <Sequence from={90} durationInFrames={110}>
        <Audio src={staticFile("audio/pop.mp3")} volume={0.8} />
        <Scene2Comparison />
      </Sequence>

      {/* ================================================================ */}
      {/* SCENE 3: LIVE SIMULATOR + METRIC ODOMETER (200 - 310 frames / 3.6s) */}
      {/* ================================================================ */}
      <Sequence from={200} durationInFrames={110}>
        <Audio src={staticFile("audio/ding.mp3")} volume={1.0} />
        <Scene3Simulator metricTarget={metricTarget} />
      </Sequence>

      {/* ================================================================ */}
      {/* SCENE 4: CTA CLOSER (310 - 420 frames / 3.6s) */}
      {/* ================================================================ */}
      <Sequence from={310} durationInFrames={110}>
        <Audio src={staticFile("audio/pop.mp3")} volume={0.8} />
        <Scene4CTA clientName={clientName} phoneNumber={phoneNumber} />
      </Sequence>
    </AbsoluteFill>
  );
};

// -------------------------------------------------------------------------
// Sub-components for Scenes
// -------------------------------------------------------------------------

const Scene1Hook: React.FC<{ hookText: string }> = ({ hookText }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { stiffness: 280, damping: 22 } });
  const opacity = interpolate(frame, [0, 15], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        padding: "0 36px",
        textAlign: "center",
        opacity,
      }}
    >
      <div
        style={{
          display: "inline-block",
          padding: "8px 18px",
          borderRadius: 8,
          backgroundColor: "#EF4444",
          color: "#FFFFFF",
          fontSize: 16,
          fontWeight: 800,
          letterSpacing: 2,
          marginBottom: 28,
          boxShadow: "0 0 25px rgba(239, 68, 68, 0.5)",
          transform: `scale(${scale})`,
        }}
      >
        ⚠️ WARNING: STOP RIGHT NOW
      </div>

      <h1
        style={{
          fontSize: 48,
          fontWeight: 900,
          lineHeight: 1.15,
          letterSpacing: -1,
          transform: `scale(${scale})`,
          textTransform: "uppercase",
          background: "linear-gradient(180deg, #FFFFFF 30%, #94A3B8 100%)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
        }}
      >
        {hookText}
      </h1>

      <p
        style={{
          fontSize: 22,
          color: "#38BDF8",
          marginTop: 24,
          fontWeight: 600,
          letterSpacing: 0.5,
        }}
      >
        Until you see how clinics are booking 50+ patients daily.
      </p>
    </AbsoluteFill>
  );
};

const Scene2Comparison: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const enterLeft = spring({ frame, fps, config: { stiffness: 220, damping: 24 } });
  const enterRight = spring({ frame: frame - 10, fps, config: { stiffness: 220, damping: 24 } });

  return (
    <AbsoluteFill
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        padding: "0 28px",
        gap: 20,
      }}
    >
      <div style={{ textAlign: "center", marginBottom: 10 }}>
        <h2 style={{ fontSize: 32, fontWeight: 800, letterSpacing: -0.5 }}>
          WHICH WEBSITE DOES YOUR CLINIC HAVE?
        </h2>
      </div>

      {/* Bad / Old Card */}
      <div
        style={{
          padding: 22,
          borderRadius: 20,
          background: "rgba(239, 68, 68, 0.08)",
          border: "1.5px solid rgba(239, 68, 68, 0.35)",
          transform: `translateX(${(1 - enterLeft) * -60}px)`,
          opacity: enterLeft,
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
          <span style={{ fontSize: 18, fontWeight: 800, color: "#F87171" }}>❌ ₹5,000 Cheap Template</span>
          <span style={{ fontSize: 14, color: "#9CA3AF" }}>2015 Format</span>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 6, fontSize: 15, color: "#D1D5DB" }}>
          <div>• Takes 12 seconds to load (Users bounce)</div>
          <div>• Looks ugly and broken on mobile</div>
          <div>• Zero patients book online</div>
        </div>
      </div>

      {/* Good / Luxury Card */}
      <div
        style={{
          padding: 22,
          borderRadius: 20,
          background: "linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(14, 165, 233, 0.15) 100%)",
          border: "1.5px solid #10B981",
          boxShadow: "0 0 30px rgba(16, 185, 129, 0.2)",
          transform: `translateX(${(1 - enterRight) * 60}px)`,
          opacity: enterRight,
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
          <span style={{ fontSize: 18, fontWeight: 800, color: "#34D399" }}>✅ Apple-Grade AI Clinic System</span>
          <span style={{ fontSize: 13, background: "#10B981", color: "#000", fontWeight: 800, padding: "2px 8px", borderRadius: 6 }}>
            PRO
          </span>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 6, fontSize: 15, color: "#F3F4F6" }}>
          <div>• 0.4s Instant Auto-Fit Speed</div>
          <div>• 1-Click WhatsApp & PhonePe Booking</div>
          <div>• Doctors get 3x more premium patients</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Scene3Simulator: React.FC<{ metricTarget: number }> = ({ metricTarget }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pop = spring({ frame, fps, config: { stiffness: 260, damping: 20 } });
  const currentMetric = Math.floor(interpolate(frame, [0, 80], [0, metricTarget], { extrapolateRight: "clamp" }));

  return (
    <AbsoluteFill
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        padding: "0 28px",
      }}
    >
      {/* Notification Toast */}
      <div
        style={{
          width: "100%",
          padding: "16px 20px",
          borderRadius: 18,
          background: "rgba(15, 23, 42, 0.85)",
          border: "1px solid rgba(56, 189, 248, 0.4)",
          boxShadow: "0 10px 40px rgba(0, 0, 0, 0.5)",
          display: "flex",
          alignItems: "center",
          gap: 14,
          marginBottom: 35,
          transform: `scale(${pop})`,
        }}
      >
        <div
          style={{
            width: 44,
            height: 44,
            borderRadius: 12,
            backgroundColor: "#10B981",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            fontSize: 22,
          }}
        >
          💳
        </div>
        <div>
          <div style={{ fontSize: 13, color: "#38BDF8", fontWeight: 700, letterSpacing: 1 }}>NEW PATIENT BOOKED!</div>
          <div style={{ fontSize: 16, color: "#FFFFFF", fontWeight: 700 }}>₹1,500 Consultation Pre-Paid</div>
        </div>
      </div>

      {/* Big Animated Counter */}
      <div style={{ textAlign: "center" }}>
        <div style={{ fontSize: 16, color: "#94A3B8", letterSpacing: 2, fontWeight: 700, marginBottom: 6 }}>
          MONTHLY APPOINTMENT REVENUE
        </div>
        <div
          style={{
            fontSize: 56,
            fontWeight: 900,
            letterSpacing: -1,
            color: "#38BDF8",
            textShadow: "0 0 35px rgba(56, 189, 248, 0.6)",
          }}
        >
          ₹{currentMetric.toLocaleString("en-IN")}
        </div>
        <div style={{ fontSize: 16, color: "#34D399", fontWeight: 700, marginTop: 8 }}>
          ▲ +310% Growth in 30 Days
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Scene4CTA: React.FC<{ clientName: string; phoneNumber: string }> = ({ clientName, phoneNumber }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pulse = interpolate(Math.sin(frame / 10), [-1, 1], [1, 1.04]);
  const enter = spring({ frame, fps, config: { stiffness: 240, damping: 20 } });

  return (
    <AbsoluteFill
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        padding: "0 28px",
        textAlign: "center",
        transform: `scale(${enter})`,
      }}
    >
      <div
        style={{
          width: "100%",
          padding: 30,
          borderRadius: 28,
          background: "linear-gradient(180deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.95) 100%)",
          border: "2px solid #38BDF8",
          boxShadow: "0 0 50px rgba(56, 189, 248, 0.25)",
        }}
      >
        <span
          style={{
            display: "inline-block",
            padding: "6px 14px",
            borderRadius: 999,
            backgroundColor: "rgba(56, 189, 248, 0.15)",
            color: "#38BDF8",
            fontSize: 13,
            fontWeight: 800,
            letterSpacing: 2,
            marginBottom: 16,
          }}
        >
          LIMITED OFFER • LIVE IN 48 HOURS
        </span>

        <h2 style={{ fontSize: 32, fontWeight: 900, lineHeight: 1.2, marginBottom: 20 }}>
          GET YOUR CLINIC'S AI WEBSITE READY
        </h2>

        {/* WhatsApp Call Card */}
        <div
          style={{
            padding: "16px 20px",
            borderRadius: 18,
            backgroundColor: "#25D366",
            color: "#052e16",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: 12,
            fontSize: 22,
            fontWeight: 900,
            letterSpacing: 0.5,
            transform: `scale(${pulse})`,
            boxShadow: "0 10px 30px rgba(37, 211, 102, 0.4)",
            marginBottom: 16,
          }}
        >
          <span>📱</span> WhatsApp: {phoneNumber}
        </div>

        <div style={{ fontSize: 16, color: "#94A3B8", fontWeight: 600 }}>
          Direct Architect: <span style={{ color: "#FFFFFF", fontWeight: 800 }}>{clientName}</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
