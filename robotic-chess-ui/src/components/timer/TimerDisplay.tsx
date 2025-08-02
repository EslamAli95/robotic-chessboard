import { useEffect, useState, useRef } from "react";
import { TimerConfig } from "./TimerConfigDialog";
import "./TimerDisplay.css";

interface Props {
  config: TimerConfig;
  currentHalf: number;
  gameOver: boolean;
  onTimeout: (loser: "w" | "b") => void;
}

export default function TimerDisplay({
  config,
  currentHalf,
  gameOver,
  onTimeout,
}: Props) {
  const { mode, minutes } = config;
  const [whiteTime, setWhiteTime] = useState(minutes * 60);
  const [blackTime, setBlackTime] = useState(minutes * 60);

  const prevHalf = useRef(currentHalf);

  // Determine whose turn it is by half-move: even → white, odd → black
  const activeColor = currentHalf % 2 === 0 ? "w" : "b";

  useEffect(() => {
    if (mode === "per-move" && currentHalf !== prevHalf.current) {
      if (activeColor === "w") {
        setWhiteTime(minutes * 60);
      } else {
        setBlackTime(minutes * 60);
      }
    }
    prevHalf.current = currentHalf;
  }, [currentHalf, mode, minutes, activeColor]);

  // Countdown loop
  useEffect(() => {
    if (gameOver) return;
    const tick = () => {
      if (mode === "clock") {
        if (activeColor === "w") setWhiteTime((t) => Math.max(0, t - 1));
        else setBlackTime((t) => Math.max(0, t - 1));
      } else {
        // per-move: only activeColor counts down
        if (activeColor === "w") setWhiteTime((t) => Math.max(0, t - 1));
        else setBlackTime((t) => Math.max(0, t - 1));
      }
    };
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [activeColor, mode, gameOver]);

  // Fire timeout callback
  useEffect(() => {
    if (whiteTime === 0) onTimeout("w");
    if (blackTime === 0) onTimeout("b");
  }, [whiteTime, blackTime, onTimeout]);

  const format = (t: number) => {
    const m = Math.floor(t / 60)
      .toString()
      .padStart(2, "0");
    const s = (t % 60).toString().padStart(2, "0");
    return `${m}:${s}`;
  };

  return (
    <div className="timer-display">
      <div className={activeColor === "w" ? "active" : ""}>
        White: {format(whiteTime)}
      </div>
      <div className={activeColor === "b" ? "active" : ""}>
        Black: {format(blackTime)}
      </div>
    </div>
  );
}
