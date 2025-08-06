// File: src/hooks/useChessGame.ts

import { useRef, useState, useEffect } from "react";
import { Chess, Move as ChessJsMove } from "chess.js";
import { sendMove, fetchLatestMove } from "../api";
import { OpponentType } from "../components/timer/TimerConfigDialog";

/** Which robot this hook drives */
export type RobotId = "white" | "black";

/** Basic time-control settings */
export interface TimerSettings {
  mode: "clock" | "per-move";
  minutes: number;
}

export interface UseChessGame {
  fen: string;
  moves: string[];
  gameOver: boolean;
  robotId: RobotId;
  timerSettings: TimerSettings;
  error: string | null;

  makeMove: (from: string, to: string) => boolean;
  goToMove: (halfMoveIndex: number) => void;
  undoLast: () => void;
  gameRef: React.RefObject<Chess>;
}

export default function useChessGame(
  robotId: RobotId,
  timerSettings: TimerSettings,
  opponent: OpponentType,
  pollInterval = 2000
): UseChessGame {
  const gameRef = useRef(new Chess());
  const [fen, setFen] = useState<string>(gameRef.current.fen());
  const [moves, setMoves] = useState<string[]>([]);
  const [gameOver, setGameOver] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const makeMove = (from: string, to: string): boolean => {
    // Clear any previous error
    setError(null);

    let mv: ChessJsMove;
    try {
      const result = gameRef.current.move({ from, to, promotion: "q" });
      if (!result) {
        setError("Illegal move");
        return false;
      }
      mv = result;
    } catch {
      setError("Illegal move");
      return false;
    }

    const san = mv.san;
    setFen(gameRef.current.fen());
    setMoves((prev) => [...prev, san]);

    // Clear error now that the move was valid
    setError(null);

    if (gameRef.current.isCheckmate()) {
      setGameOver(true);
      const loser = gameRef.current.turn() === "w" ? "White" : "Black";
      const victor = loser === "White" ? "Black" : "White";
      alert(`Checkmate! ${victor} wins!`);
    }

    // Send move to backend
    sendMove(robotId, from, to)
      .then(() => {
        // On success, ensure error is cleared
        setError(null);
      })
      .catch((e: any) => {
        // Rollback on error
        gameRef.current.undo();
        setFen(gameRef.current.fen());
        setMoves((prev) => prev.filter((m) => m !== san));

        console.error("API error sending move:", e.response?.data || e);
        const detail =
          e.response?.data?.detail ||
          e.response?.data?.message ||
          e.message ||
          "Server error sending move to robot";

        setError(detail);
      });

    return true;
  };

  const goToMove = (halfMoveIndex: number): void => {
    const clamped = Math.min(Math.max(0, halfMoveIndex), moves.length);
    const g = new Chess();
    for (let i = 0; i < clamped; i++) {
      try {
        const result = g.move(moves[i], { strict: false });
        if (!result) {
          console.warn(`Failed to apply SAN move #${i + 1}: ${moves[i]}`);
        }
      } catch (err) {
        console.warn(`Error replaying SAN move #${i + 1}:`, moves[i], err);
      }
    }
    gameRef.current = g;
    setFen(g.fen());
    // Moving through history clears any error
    setError(null);
  };

  useEffect(() => {
    if (pollInterval <= 0) return;
    const id = setInterval(async () => {
      if (gameOver) return;

      if (opponent === "robot" || opponent === "human") {
        try {
          const res = await fetchLatestMove(robotId);
          const d = res.data;
          if (d.from_square && d.to_square) {
            const opp = gameRef.current.move({
              from: d.from_square,
              to: d.to_square,
            });
            if (opp) {
              setFen(gameRef.current.fen());
              setMoves((prev) => [...prev, opp.san]);
              // Successful opponent move clears error
              setError(null);
            }
          }
        } catch {
          // ignore polling errors
        }
      }
    }, pollInterval);

    return () => clearInterval(id);
  }, [gameOver, pollInterval, moves.length, robotId, opponent]);

  const undoLast = (): void => {
    if (moves.length === 0) return;
    gameRef.current.undo();
    setFen(gameRef.current.fen());
    setMoves((prev) => prev.slice(0, -1));
    // Undo also clears error state
    setError(null);
  };

  return {
    fen,
    moves,
    gameOver,
    makeMove,
    goToMove,
    undoLast,
    gameRef,
    robotId,
    timerSettings,
    error,
  };
}
