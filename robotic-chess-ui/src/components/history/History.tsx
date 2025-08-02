import { useState, useEffect } from "react";
import "./History.css";

interface HistoryProps {
  moves: string[];
  currentHalf: number;
  onNavigate: (halfMoveIndex: number) => void;
  onUndoRequest: () => void;
  onDrawRequest: () => void;
  onsignRequest: () => void;
}

export default function History({
  moves,
  currentHalf,
  onNavigate,
  onUndoRequest,
  onDrawRequest,
  onsignRequest,
}: HistoryProps) {
  const totalHalfMoves = moves.length;

  // undo‐request UI state
  const [undoRequested, setUndoRequested] = useState<boolean>(false);
  const [drawRequested, setDrawRequested] = useState<boolean>(false);
  useEffect(() => {
    setUndoRequested(false);
  }, [moves.length]);

  // clamp requested half‐move & notify parent
  const goTo = (n: number) => {
    const clamped = Math.min(Math.max(0, n), totalHalfMoves);
    onNavigate(clamped);
  };

  // Build an array of full move‐pairs for display:
  // each row has white = moves[2*i], black = moves[2*i+1]
  const rows = Array.from(
    { length: Math.ceil(totalHalfMoves / 2) },
    (_, i) => ({
      num: i + 1,
      white: moves[i * 2] || "",
      black: moves[i * 2 + 1] || "",
    })
  );
  const handleUndoClick = () => {
    if (!undoRequested) {
      setUndoRequested(true);
      onUndoRequest();
    }
  };

  const handleDrawClick = () => {
    if (!drawRequested) {
      setDrawRequested(true);
      onDrawRequest();
    }
  };
  return (
    <div className="history-wrapper">
      <div className="history-toolbar">
        <button onClick={() => goTo(0)} title="Start">
          ⏮
        </button>
        <button onClick={() => goTo(currentHalf - 1)} title="Back">
          ◀
        </button>
        <button onClick={() => goTo(currentHalf + 1)} title="Forward">
          ▶
        </button>
        <button onClick={() => goTo(totalHalfMoves)} title="End">
          ⏭
        </button>
      </div>

      <div className="history-container">
        <table className="history-table">
          <tbody>
            {rows.map((r, idx) => {
              // compute the half‐move indices for white/black in this row:
              const whiteIndex = idx * 2 + 1;
              const blackIndex = idx * 2 + 2;
              return (
                <tr key={idx}>
                  <td className="num">{r.num}.</td>
                  <td className={whiteIndex === currentHalf ? "current" : ""}>
                    {r.white}
                  </td>
                  <td className={blackIndex === currentHalf ? "current" : ""}>
                    {r.black}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="history-footer">
        <button
          title="Undo"
          onClick={handleUndoClick}
          className={undoRequested ? "requested" : ""}
        >
          ↩
        </button>
        <button
          title="Offer Draw"
          onClick={handleDrawClick}
          className={drawRequested ? "requested" : ""}
        >
          ½
        </button>
        <button title="resign" onClick={onsignRequest}>
          🚩
        </button>
      </div>
    </div>
  );
}
