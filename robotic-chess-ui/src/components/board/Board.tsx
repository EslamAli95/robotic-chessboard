import { useState, useEffect } from "react";
import useChessGame from "../../hooks/useChessGame";
import HistoryPanel from "../history/HistoryPanel";
import TimerConfigDialog, {
  TimerConfig,
  Side,
  TimerMode,
} from "../timer/TimerConfigDialog";
import TimerDisplay from "../timer/TimerDisplay";
import EndBanner from "../endBanner/EndBanner";
import ChessArea from "./ChessArea";
import "./Board.css";

export default function Board() {
  const [timerConfig, setTimerConfig] = useState<TimerConfig | null>(null);
  const robotId: Side = timerConfig?.side ?? "white";
  const opponent = timerConfig?.opponent ?? "robot";
  const timerSettings: { mode: TimerMode; minutes: number } = timerConfig
    ? { mode: timerConfig.mode, minutes: timerConfig.minutes }
    : { mode: "clock", minutes: 5 };

  const { fen, moves, gameOver, makeMove, gameRef, undoLast, goToMove } =
    useChessGame(robotId, timerSettings, opponent);

  const [currentHalf, setCurrentHalf] = useState<number>(moves.length);
  const [drawAccepted, setDrawAccepted] = useState<boolean>(false);
  const [resigned, setResigned] = useState<boolean>(false);
  const [timeoutLoser, setTimeoutLoser] = useState<"w" | "b" | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    setCurrentHalf(moves.length);
    setDrawAccepted(false);
    setTimeoutLoser(null);
  }, [moves.length]);

  if (!timerConfig) {
    return <TimerConfigDialog onSubmit={(cfg) => setTimerConfig(cfg)} />;
  }

  const isViewingPast = currentHalf !== moves.length;
  const isGameEnded = drawAccepted || gameOver || resigned;
  // Lock the board if viewing history or if the game has ended
  const isLocked = isViewingPast || isGameEnded;

  // ── handle square selection, passed into ChessArea ───────────────
  const handleSelect = (sq: string) => {
    if (isViewingPast) {
      setErrorMessage("Return to the live position (▶▶) to resume play.");
      return;
    }
    if (isGameEnded) {
      setErrorMessage("Game over — start a new game.");
      return;
    }
    setSelected(sq);
    setErrorMessage(null);
  };

  return (
    <div className="game">
      <ChessArea
        fen={fen}
        gameRef={gameRef}
        makeMove={makeMove}
        locked={isLocked}
        selected={selected}
        onSelect={handleSelect}
        onError={(msg) => setErrorMessage(msg)}
        orientation={timerConfig.side}
      />
      <div className="history">
        {errorMessage && <p className="error">{errorMessage}</p>}
        <TimerDisplay
          config={timerConfig}
          currentHalf={currentHalf}
          gameOver={isGameEnded}
          onTimeout={(loser) => setTimeoutLoser(loser)}
        />
        <HistoryPanel
          moves={moves}
          currentHalf={currentHalf}
          onNavigate={(half) => {
            goToMove(half);
            setCurrentHalf(half);
          }}
          onUndo={() => undoLast()}
          onDraw={() => setDrawAccepted(true)}
          onResign={() => setResigned(true)}
        />
        <EndBanner
          timeoutLoser={timeoutLoser}
          resigned={resigned}
          drawAccepted={drawAccepted}
          gameRef={gameRef}
        />
      </div>
    </div>
  );
}
