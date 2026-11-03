// Adapted from haidrrrry/remotion-motion-graphics/assets/theme.ts (MIT).
// Phone proportions are adapted from Karanjot786/reelcn/registry/items/phone-frame.tsx (MIT).
// Exact source versions and copyright notices: production_hub/creative_skills.json, .agents/skills/*/LICENSE.
import {Easing} from "remotion";
export const motion = {
  out: Easing.bezier(.16, 1, .3, 1), in: Easing.bezier(.7, 0, .84, 0),
  smooth: {damping: 22, stiffness: 110, mass: .85}, snappy: {damping: 16, stiffness: 180, mass: .65},
};
export const palettes = {
  directed_motion: {bg: "#182640", surface: "#243657", ink: "#f6f9ff", dim: "#b6c8e5", hero: "#70e1c0", paper: "#eef9f6", text: "#162b36", line: "#c7e3dc"},
  chat_story: {bg: "#f2eaf5", surface: "#e3d5ec", ink: "#372443", dim: "#765f85", hero: "#9257b7", paper: "#fffaff", text: "#372443", line: "#d8c4e4"},
  choice_quiz: {bg: "#f0f4ff", surface: "#dbe5ff", ink: "#1b3058", dim: "#657ba3", hero: "#285ed6", paper: "#ffffff", text: "#1b3058", line: "#c6d5f1"},
};
export const neutral = {white: "#ffffff", dark: "#101a2a", red: "#d95965", muted: "#8997a9", glass: "rgba(255,255,255,.08)", shadow: "rgba(8,20,42,.18)"};
