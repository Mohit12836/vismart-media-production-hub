import React from "react";
import { Audio, Series, staticFile } from "remotion";
import scriptData from "./data/script.json";
import { SceneContainer, SceneData } from "./components/SceneContainer";
import { Scene1Alert } from "./scenes/Scene1Alert";
import { Scene2Google } from "./scenes/Scene2Google";
import { Scene3Trap } from "./scenes/Scene3Trap";
import { Scene4Features } from "./scenes/Scene4Features";
import { Scene5NightBooking } from "./scenes/Scene5NightBooking";
import { THEME } from "./theme";
import { CompositionProps } from "./schema";

const scenes = scriptData as SceneData[];

export const TOTAL_DURATION = scenes.reduce((acc, s) => acc + s.frames, 0);

export const MyComposition: React.FC<CompositionProps> = (props) => {
  return (
    <div style={{ width: 720, height: 1280, backgroundColor: THEME.colors.bg }}>
      {/* Background Pulse Groove */}
      <Audio src={staticFile("audio/bg.mp3")} volume={0.04} loop />

      <Series>
        {scenes.map((scene) => {
          let SceneVisual: React.ReactNode = null;
          switch (scene.id) {
            case "s01":
              SceneVisual = <Scene1Alert />;
              break;
            case "s02":
              SceneVisual = <Scene2Google />;
              break;
            case "s03":
              SceneVisual = <Scene3Trap />;
              break;
            case "s04":
              SceneVisual = <Scene4Features />;
              break;
            case "s05":
              SceneVisual = <Scene5NightBooking {...props} />;
              break;
            default:
              SceneVisual = null;
          }

          return (
            <Series.Sequence key={scene.id} durationInFrames={scene.frames}>
              <SceneContainer scene={scene}>{SceneVisual}</SceneContainer>
            </Series.Sequence>
          );
        })}
      </Series>
    </div>
  );
};
