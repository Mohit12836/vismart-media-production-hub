import React from "react";
import { Composition } from "remotion";
import { loadFont } from "@remotion/google-fonts/Poppins";
import { MyComposition, TOTAL_DURATION } from "./Composition";
import { compositionSchema } from "./schema";
import { SilentKineticReel, SILENT_KINETIC_DURATION } from "./compositions/SilentKineticReel";
import { LongExplainer16x9, LONG_EXPLAINER_DURATION } from "./compositions/LongExplainer16x9";
import { FactoryVideo } from "./compositions/FactoryVideo";

loadFont();

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="FactoryVideo"
        component={FactoryVideo}
        durationInFrames={750}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{scenes: ["अपनी पहली कहानी लिखें", "अगले दृश्य में उसका जवाब दें"], duration: 25, format: "reel", layout: "story", brand: "Your channel", accent: "#2563eb", assets: [], audio: null}}
        calculateMetadata={({props}) => ({durationInFrames: Math.round(props.duration * 30), width: props.format === "long" ? 1920 : 1080, height: props.format === "long" ? 1080 : 1920})}
      />
      <Composition
        id="Main"
        component={MyComposition}
        durationInFrames={TOTAL_DURATION}
        fps={30}
        width={720}
        height={1280}
        schema={compositionSchema}
        defaultProps={{
          creatorName: "MOHIT JAIN",
          phoneNumber: "6263879076",
          professionTitle: "HEALTHCARE WEBSITE ARCHITECT",
          accentColor: "#00F2FE",
        }}
      />

      {/* Silent Kinetic Beat-Synced Viral Reel */}
      <Composition
        id="SilentKinetic"
        component={SilentKineticReel}
        durationInFrames={SILENT_KINETIC_DURATION}
        fps={30}
        width={720}
        height={1280}
        defaultProps={{
          hookText: "DON'T BUILD A WEBSITE IN 2026...",
          metricTarget: 340000,
          clientName: "MOHIT JAIN",
          phoneNumber: "6263879076",
          brandName: "VISMART STUDIO",
        }}
      />

      {/* Long 16:9 Landscape Explainer (YouTube / Desktop) */}
      <Composition
        id="LongExplainer16x9"
        component={LongExplainer16x9}
        durationInFrames={LONG_EXPLAINER_DURATION}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          headline: "HOW TOP DENTAL CLINICS ATTRACT 50+ PATIENTS MONTHLY",
          subheadline: "The Complete 2026 Apple-Grade Healthcare Booking Architecture",
          clientName: "MOHIT JAIN",
          phoneNumber: "6263879076",
          brandName: "VISMART STUDIO",
        }}
      />
    </>
  );
};
