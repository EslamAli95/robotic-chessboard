// src/components/end/EndBanner.tsx
import React from "react";
import { Chess } from "chess.js";
import "./EndBanner.css";

interface Props {
  timeoutLoser: "w" | "b" | null;
  resigned: boolean;
  drawAccepted: boolean;
  gameRef: React.RefObject<Chess>;
}

export default function EndBanner({
  timeoutLoser,
  resigned,
  drawAccepted,
  gameRef,
}: Props) {
  let message: string | null = null;

  if (timeoutLoser !== null) {
    const loserName = timeoutLoser === "w" ? "White" : "Black";
    const winnerName = timeoutLoser === "w" ? "Black" : "White";
    message = `${loserName} timed out — ${winnerName} wins!`;
  } else if (resigned) {
    message =
      gameRef.current.turn() === "w"
        ? "Black wins! White resigned."
        : "White wins! Black resigned.";
  } else if (drawAccepted) {
    message = "Game drawn by agreement";
  } else {
    return null;
  }

  return (
    <div className="draw-banner">
      {message}
      <button
        className="new-game-button"
        onClick={() => window.location.reload()}
      >
        New Game
      </button>
    </div>
  );
}
