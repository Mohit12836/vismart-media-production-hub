import React from 'react';
import {
  Composition,
  registerRoot,
  useCurrentFrame,
  interpolate,
  AbsoluteFill,
  Sequence,
  Audio,
  staticFile,
} from 'remotion';
import plan from '../../examples/dentist-scene-plan.json';

const FPS = 30;

const backgrounds: Record<string, string> = {
  concern: '#14243c',
  curiosity: '#132e45',
  relief: '#f3f7fa',
  confidence: '#f8fafc',
};

const palette = (s: string) => backgrounds[s] || '#182a41';

function MainComposition() {
  return (
    <AbsoluteFill style={{ background: '#0c1320', fontFamily: "'Poppins', sans-serif" }}>
      {/* 1 Continuous Perfect Voiceover Audio */}
      <Audio src={staticFile('audio/voiceover.mp3')} />

      {plan.beats.map((beat, i) => {
        const from = Math.round(beat.start * FPS);
        const duration = Math.round((beat.end - beat.start) * FPS);
        return (
          <Sequence key={beat.id} from={from} durationInFrames={duration}>
            <Shot beat={beat} order={i} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
}

function Shot({ beat, order }: { beat: (typeof plan.beats)[number]; order: number }) {
  const f = useCurrentFrame();
  const dark = ['concern', 'curiosity'].includes(beat.emotion.primary);
  const totalFrames = Math.max(1, Math.round((beat.end - beat.start) * FPS));

  const zoom = interpolate(f, [0, totalFrames], [1, 1.04], { extrapolateRight: 'clamp' });
  const op = interpolate(f, [0, 8, totalFrames - 8, totalFrames], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const fg = dark ? '#f7fafc' : '#18283e';
  const accent = dark ? '#00f2fe' : '#10b981';

  return (
    <AbsoluteFill style={{ background: palette(beat.emotion.primary), color: fg, opacity: op, overflow: 'hidden' }}>
      {/* Ambient Radial Soft Light */}
      <div
        style={{
          position: 'absolute',
          top: 250,
          left: 110,
          width: 500,
          height: 500,
          borderRadius: '50%',
          background: `radial-gradient(circle, ${accent}25 0%, transparent 70%)`,
          filter: 'blur(50px)',
          pointerEvents: 'none',
        }}
      />

      <AbsoluteFill style={{ transform: `scale(${zoom})`, justifyContent: 'center', alignItems: 'center' }}>
        <svg viewBox="0 0 720 980" width="100%" height="80%" aria-label={beat.visual}>
          <defs>
            <linearGradient id={'g' + order} x1="0" y1="0" x2="1" y2="1">
              <stop stopColor={accent} stopOpacity="0.25" />
              <stop offset="1" stopColor={accent} stopOpacity="0" />
            </linearGradient>
          </defs>
          <circle cx="360" cy="460" r="310" fill={`url(#g${order})`} />

          {/* Beat 1: Customer bypassing shop to competitor */}
          {order === 0 ? (
            <>
              {/* Your Shop (Offline) */}
              <rect x="70" y="280" width="260" height="260" rx="30" fill={dark ? '#1e293b' : '#ffffff'} stroke="#64748b" strokeWidth="5" />
              <text x="110" y="340" fontSize="28" fontWeight="bold" fill={dark ? '#94a3b8' : '#475569'}>आपकी दुकान</text>
              <text x="145" y="420" fontSize="55">🏪</text>
              <rect x="95" y="470" width="210" height="40" rx="12" fill="#ef444422" />
              <text x="112" y="496" fontSize="16" fontWeight="bold" fill="#ef4444">ऑफलाइन / नो वेबसाइट</text>

              {/* Competitor Shop (Online) */}
              <rect x="390" y="280" width="260" height="260" rx="30" fill={dark ? '#132e45' : '#ffffff'} stroke="#10b981" strokeWidth="6" />
              <text x="430" y="340" fontSize="28" fontWeight="bold" fill="#10b981">दूसरा बिजनेस</text>
              <text x="465" y="420" fontSize="55">🏢</text>
              <rect x="415" y="470" width="210" height="40" rx="12" fill="#10b98122" />
              <text x="432" y="496" fontSize="16" fontWeight="bold" fill="#10b981">✓ वेबसाइट एक्टिव</text>

              {/* Bypassing Arrow */}
              <path d="M 200 580 Q 360 680 520 580" fill="none" stroke="#f59e0b" strokeWidth="8" strokeDasharray="12 8" />
              <polygon points="520,570 540,585 520,600" fill="#f59e0b" />
              <text x="250" y="660" fontSize="22" fontWeight="bold" fill="#f59e0b">ग्राहक सीधा दूसरे के पास गया!</text>
            </>
          ) : null}

          {/* Beat 2: Google Search & 3 Key Information Checkpoints */}
          {order === 1 ? (
            <>
              {/* Phone Frame */}
              <rect x="150" y="160" width="420" height="620" rx="40" fill={dark ? '#0f172a' : '#ffffff'} stroke="#38bdf8" strokeWidth="8" />
              {/* Search Bar */}
              <rect x="180" y="220" width="360" height="65" rx="32" fill={dark ? '#1e293b' : '#f1f5f9'} stroke="#64748b" strokeWidth="2" />
              <text x="210" y="260" fontSize="22" fill={dark ? '#38bdf8' : '#0284c7'} fontWeight="bold">🔍 Best Service Near Me</text>
              
              {/* 3 Checklist Items */}
              <g transform="translate(180, 320)">
                <rect x="0" y="0" width="360" height="65" rx="18" fill="#10b98118" stroke="#10b981" strokeWidth="2" />
                <text x="20" y="40" fontSize="22" fontWeight="bold" fill="#10b981">1. क्या सर्विस देते हैं? 🛠️</text>
              </g>
              <g transform="translate(180, 410)">
                <rect x="0" y="0" width="360" height="65" rx="18" fill="#38bdf818" stroke="#38bdf8" strokeWidth="2" />
                <text x="20" y="40" fontSize="22" fontWeight="bold" fill="#38bdf8">2. काम की क्वालिटी कैसी है? ✨</text>
              </g>
              <g transform="translate(180, 500)">
                <rect x="0" y="0" width="360" height="65" rx="18" fill="#f59e0b18" stroke="#f59e0b" strokeWidth="2" />
                <text x="20" y="40" fontSize="22" fontWeight="bold" fill="#f59e0b">3. संपर्क कैसे किया जाए? 📞</text>
              </g>
            </>
          ) : null}

          {/* Beat 3: Competitor's website opened with everything in one place */}
          {order === 2 ? (
            <>
              {/* Split Cards: No Info vs Full Website */}
              <rect x="60" y="230" width="280" height="480" rx="32" fill="#ef444412" stroke="#ef4444" strokeWidth="4" />
              <text x="100" y="290" fontSize="26" fontWeight="bold" fill="#ef4444">❌ जानकारी गायब</text>
              <text x="90" y="360" fontSize="18" fill={dark ? '#cbd5e1' : '#475569'}>• नो फ़ोटोज़</text>
              <text x="90" y="420" fontSize="18" fill={dark ? '#cbd5e1' : '#475569'}>• नो प्राइज़िंग</text>
              <text x="90" y="480" fontSize="18" fill={dark ? '#cbd5e1' : '#475569'}>• नो रिव्यूज</text>
              <text x="85" y="580" fontSize="18" fontWeight="bold" fill="#ef4444">ग्राहक का भरोसा टूटा ✘</text>

              <rect x="380" y="230" width="280" height="480" rx="32" fill="#10b98112" stroke="#10b981" strokeWidth="5" />
              <text x="410" y="290" fontSize="26" fontWeight="bold" fill="#10b981">✓ दूसरे की वेबसाइट</text>
              <text x="410" y="360" fontSize="18" fill={dark ? '#cbd5e1' : '#475569'}>✓ सब कुछ 1 जगह</text>
              <text x="410" y="420" fontSize="18" fill={dark ? '#cbd5e1' : '#475569'}>✓ 5-स्टार रिव्यूज</text>
              <text x="410" y="480" fontSize="18" fill={dark ? '#cbd5e1' : '#475569'}>✓ डायरेक्ट WhatsApp</text>
              <text x="405" y="580" fontSize="18" fontWeight="bold" fill="#10b981">100% भरोसा बन गया ✓</text>
            </>
          ) : null}

          {/* Beat 4: Missed Customer & Lost Deal Alert */}
          {order === 3 ? (
            <>
              <rect x="80" y="240" width="560" height="460" rx="36" fill="#ef444415" stroke="#ef4444" strokeWidth="6" />
              <circle cx="360" cy="350" r="55" fill="#ef4444" />
              <text x="335" y="370" fontSize="60">⚠️</text>
              <text x="140" y="460" fontSize="36" fontWeight="900" fill="#ef4444">काम किसी और को मिल गया!</text>
              <text x="160" y="520" fontSize="22" fontWeight="bold" fill={dark ? '#ffffff' : '#0f172a'}>ग्राहक को जरूरत आपकी सर्विस की थी,</text>
              <text x="180" y="560" fontSize="22" fontWeight="bold" fill="#f59e0b">लेकिन वेबसाइट न होने से डील मिस हुई!</text>
              <rect x="160" y="610" width="400" height="50" rx="16" fill="#ef4444" />
              <text x="200" y="642" fontSize="22" fontWeight="bold" fill="#ffffff">सीधा हज़ारों रुपयों का नुकसान!</text>
            </>
          ) : null}

          {/* Beat 5: Solution - Professional Business Website Mockup */}
          {order === 4 ? (
            <>
              {/* Browser Window */}
              <rect x="60" y="200" width="600" height="540" rx="36" fill="#ffffff" stroke="#10b981" strokeWidth="6" />
              {/* Window Header */}
              <rect x="60" y="200" width="600" height="60" rx="20" fill="#1e293b" />
              <circle cx="95" cy="230" r="8" fill="#ef4444" />
              <circle cx="120" cy="230" r="8" fill="#f59e0b" />
              <circle cx="145" cy="230" r="8" fill="#10b981" />
              <text x="210" y="238" fontSize="20" fill="#94a3b8" fontFamily="monospace">www.yourbusiness.com</text>

              {/* 4 Feature Cards inside Website */}
              <rect x="90" y="290" width="250" height="110" rx="18" fill="#dbeafe" stroke="#3b82f6" strokeWidth="2" />
              <text x="110" y="340" fontSize="22" fontWeight="bold" fill="#1e40af">🛠️ Services</text>
              <text x="110" y="375" fontSize="16" fill="#64748b">काम की रियल फ़ोटोज़</text>

              <rect x="380" y="290" width="250" height="110" rx="18" fill="#fef3c7" stroke="#f59e0b" strokeWidth="2" />
              <text x="400" y="340" fontSize="22" fontWeight="bold" fill="#b45309">⭐ Reviews</text>
              <text x="400" y="375" fontSize="16" fill="#64748b">5-Star ग्राहक रेटिंग</text>

              <rect x="90" y="430" width="250" height="110" rx="18" fill="#f3e8ff" stroke="#a855f7" strokeWidth="2" />
              <text x="110" y="480" fontSize="22" fontWeight="bold" fill="#6b21a8">📍 Location</text>
              <text x="110" y="515" fontSize="16" fill="#64748b">Google Maps रूट</text>

              <rect x="380" y="430" width="250" height="110" rx="18" fill="#dcfce7" stroke="#16a34a" strokeWidth="2" />
              <text x="400" y="480" fontSize="22" fontWeight="bold" fill="#15803d">💬 WhatsApp</text>
              <text x="400" y="515" fontSize="16" fill="#64748b">1-Click डायरेक्ट चैट</text>

              {/* Bottom Trust Tag */}
              <rect x="130" y="580" width="460" height="60" rx="20" fill="#10b981" />
              <text x="160" y="618" fontSize="24" fontWeight="bold" fill="#ffffff">सब कुछ एक ही जगह = 100% भरोसा!</text>
            </>
          ) : null}

          {/* Beat 6: Multi-Device Responsive Showcase */}
          {order === 5 ? (
            <>
              {/* Desktop Monitor */}
              <rect x="90" y="220" width="540" height="340" rx="28" fill="#ffffff" stroke="#0284c7" strokeWidth="6" />
              <rect x="90" y="220" width="540" height="50" rx="16" fill="#0284c7" />
              <text x="130" y="253" fontSize="22" fontWeight="bold" fill="#ffffff">Professional Website Preview</text>
              
              {/* Mockup Elements on Screen */}
              <rect x="120" y="300" width="220" height="140" rx="16" fill="#e0f2fe" />
              <rect x="360" y="300" width="240" height="35" rx="10" fill="#94a3b8" />
              <rect x="360" y="350" width="180" height="25" rx="8" fill="#cbd5e1" />
              <rect x="360" y="390" width="140" height="40" rx="12" fill="#10b981" />
              <text x="385" y="417" fontSize="18" fontWeight="bold" fill="#ffffff">Book Now</text>

              {/* Mobile Phone Mockup Overlay on Right */}
              <rect x="440" y="380" width="210" height="340" rx="30" fill="#0f172a" stroke="#10b981" strokeWidth="6" />
              <rect x="460" y="420" width="170" height="220" rx="14" fill="#ffffff" />
              <rect x="480" y="450" width="130" height="40" rx="10" fill="#10b981" />
              <text x="495" y="476" fontSize="16" fontWeight="bold" fill="#ffffff">1-Click Call</text>

              {/* Tag below */}
              <rect x="120" y="600" width="480" height="65" rx="20" fill="#0284c7" />
              <text x="155" y="640" fontSize="24" fontWeight="bold" fill="#ffffff">दिखने में शानदार • उपयोग में आसान</text>
            </>
          ) : null}

          {/* Beat 7: Vismart Studio VIP CTA */}
          {order === 6 ? (
            <>
              {/* Grand VIP Branding Card */}
              <rect x="60" y="190" width="600" height="560" rx="40" fill="#ffffff" stroke="#10b981" strokeWidth="8" />
              <rect x="80" y="210" width="560" height="85" rx="22" fill="#10b981" />
              <text x="140" y="265" fontSize="38" fontWeight="900" fill="#ffffff">✨ VISMART STUDIO</text>

              {/* Pitch Hook */}
              <text x="110" y="350" fontSize="28" fontWeight="bold" fill="#0f172a">अपनी दुकान या बिजनेस का नाम</text>
              <text x="180" y="390" fontSize="30" fontWeight="900" fill="#10b981">WhatsApp पर भेजें!</text>

              {/* Demo Promise */}
              <rect x="100" y="430" width="520" height="90" rx="22" fill="#f0fdf4" stroke="#16a34a" strokeWidth="3" />
              <text x="125" y="470" fontSize="22" fontWeight="bold" fill="#15803d">हम आपको दिखाएंगे कि आपके बिजनेस की</text>
              <text x="175" y="502" fontSize="24" fontWeight="900" fill="#15803d">वेबसाइट कैसी दिख सकती है!</text>

              {/* Big WhatsApp CTA Button */}
              <rect x="120" y="555" width="480" height="85" rx="26" fill="#25d366" />
              <text x="175" y="610" fontSize="34" fontWeight="900" fill="#ffffff">💬 WhatsApp पर मैसेज करें</text>
              
              <text x="230" y="685" fontSize="26" fontWeight="bold" fill="#64748b">VISMART STUDIO</text>
            </>
          ) : null}
        </svg>
      </AbsoluteFill>

      {/* Top Headline Caption */}
      <div
        style={{
          position: 'absolute',
          top: 100,
          left: 40,
          right: 40,
          fontWeight: 900,
          fontSize: 50,
          lineHeight: 1.18,
          textAlign: 'center',
          letterSpacing: '-0.01em',
        }}
      >
        {beat.caption}
      </div>

      {/* Bottom Subtitle Karaoke Box */}
      <div
        style={{
          position: 'absolute',
          bottom: 150,
          left: 40,
          right: 40,
          fontSize: 27,
          fontWeight: 700,
          textAlign: 'center',
          background: dark ? '#0e1723f0' : '#fffffffa',
          borderRadius: 24,
          padding: '20px 24px',
          lineHeight: 1.45,
          boxShadow: '0 15px 35px rgba(0,0,0,0.3)',
          border: dark ? '1px solid rgba(255,255,255,0.15)' : '1px solid rgba(0,0,0,0.1)',
        }}
      >
        {beat.voice}
      </div>

      {/* Bottom Progress Scrubber */}
      <div style={{ position: 'absolute', bottom: 85, left: 60, right: 60, height: 8, background: dark ? '#ffffff33' : '#17364d22', borderRadius: 8 }}>
        <div style={{ height: '100%', width: `${Math.min(100, (f / totalFrames) * 100)}%`, background: accent, borderRadius: 8 }} />
      </div>
    </AbsoluteFill>
  );
}

function Root() {
  return (
    <Composition
      id="Demo"
      component={MainComposition}
      fps={FPS}
      width={720}
      height={1280}
      durationInFrames={Math.ceil(plan.meta.duration * FPS)}
    />
  );
}

registerRoot(Root);
