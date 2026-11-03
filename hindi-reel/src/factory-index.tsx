import React from "react";
import {Composition, registerRoot} from "remotion";
import {FactoryVideo} from "./compositions/FactoryVideo";

// Separate entry avoids downloading the legacy studio's font families on every render.
const FactoryRoot: React.FC = () => <Composition
  id="FactoryVideo"
  component={FactoryVideo}
  durationInFrames={750}
  fps={30}
  width={1080}
  height={1920}
  defaultProps={{scenes: ["अपनी पहली कहानी लिखें", "अगले दृश्य में उसका जवाब दें"], duration: 25, format: "reel", layout: "story", brand: "Your channel", accent: "#2563eb", assets: [], audio: null}}
  calculateMetadata={({props}) => ({durationInFrames: Math.round(props.duration * 30), width: props.format === "long" ? 1920 : 1080, height: props.format === "long" ? 1080 : 1920})}
/>;

registerRoot(FactoryRoot);
