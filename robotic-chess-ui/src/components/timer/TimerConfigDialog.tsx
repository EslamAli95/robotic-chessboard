import { useState } from "react";
import "./TimerConfigDialog.css";

export type TimerMode = "clock" | "per-move";
export type Side = "white" | "black";
export type OpponentType = "robot" | "human";

export interface TimerConfig {
  mode: TimerMode;
  minutes: number;
  side: Side;
  opponent: OpponentType;
}

interface Props {
  onSubmit: (cfg: TimerConfig) => void;
}

export default function TimerConfigDialog({ onSubmit }: Props) {
  const [mode, setMode] = useState<TimerMode>("clock");
  const [minutes, setMinutes] = useState<number>(5);
  const [side, setSide] = useState<Side>("white");
  const [opponent, setOpponent] = useState<OpponentType>("robot");

  return (
    <div className="timer-backdrop">
      <div className="timer-dialog">
        <h2>Game Timer Settings</h2>
        <div className="form-row">
          <label htmlFor="opponent">Opponent</label>
          <select
            id="opponent"
            value={opponent}
            onChange={(e) => setOpponent(e.target.value as OpponentType)}
          >
            <option value="robot">Robotic Board</option>
            <option value="human">Remote Human</option>
          </select>
        </div>
        <div className="form-row">
          <label htmlFor="mode">Mode</label>
          <select
            id="mode"
            value={mode}
            onChange={(e) => setMode(e.target.value as TimerMode)}
          >
            <option value="clock">Chess Clock</option>
            <option value="per-move">Per-Move Timer</option>
          </select>
        </div>
        <div className="form-row">
          <label htmlFor="minutes">Minutes per side</label>
          <input
            id="minutes"
            type="number"
            min={1}
            value={minutes}
            onChange={(e) => setMinutes(Number(e.target.value))}
          />
        </div>
        <div className="form-row side-toggle">
          <label className={`toggle ${side === "white" ? "active" : ""}`}>
            <input
              type="radio"
              name="side"
              value="white"
              checked={side === "white"}
              onChange={() => setSide("white")}
            />
            White
          </label>
          <label className={`toggle ${side === "black" ? "active" : ""}`}>
            <input
              type="radio"
              name="side"
              value="black"
              checked={side === "black"}
              onChange={() => setSide("black")}
            />
            Black
          </label>
        </div>
        <button
          className="start-button"
          onClick={() => onSubmit({ mode, minutes, side, opponent })}
        >
          Start Game
        </button>
      </div>
    </div>
  );
}
