export type WordTiming = {text: string; start: number; end: number};
export type DirectedScenePlan = {
  visual: string; headline: string; label?: string; message?: string; reply?: string;
  option_a?: string; option_b?: string; correct?: string;
};
export type CreativePlan = {audience: string; first_frame: string; payoff: string; fictional: boolean; scenes: DirectedScenePlan[]};
export type DirectedTiming = {from: number; duration: number; audio: string | null; words: WordTiming[]};
