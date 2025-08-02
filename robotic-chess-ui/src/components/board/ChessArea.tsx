import { Chessboard } from "react-chessboard";
import { buildHighlights } from "../../utils/highlights";
import { CSSProperties, useEffect, useState } from "react";
import { Chess } from "chess.js";

interface Props {
  fen: string;
  gameRef: React.RefObject<Chess>;
  makeMove: (from: string, to: string) => boolean;
  locked: boolean;
  selected?: string | null;
  onSelect: (sq: string) => void;
  orientation?: "white" | "black";
  onError?: (msg: string) => void;
}

export default function ChessArea({
  fen,
  gameRef,
  makeMove,
  locked,
  selected,
  onSelect,
  onError,
  orientation = "white",
}: Props) {
  const [possible, setPossible] = useState<string[]>([]);
  const [styles, setStyles] = useState<Record<string, CSSProperties>>({});

  useEffect(() => {
    setStyles(buildHighlights(selected || null, possible, gameRef.current));
  }, [selected, possible, fen, gameRef]);

  const handleSquare = (sq: string) => {
    if (locked) return;
    onSelect(sq);
    const dests = gameRef.current
      .moves({ square: sq as any, verbose: true })
      .map((m: any) => m.to);
    setPossible(dests);
  };

  // must accept (from, to, piece) and always return boolean
  const handleDrop = (from: string, to: string, _piece: any): boolean => {
    if (locked) {
      return false;
    }
    const ok = makeMove(from, to);
    if (!ok) {
      onError?.("Invalid move!");
    }
    return ok;
  };

  return (
    <div className="board">
      <Chessboard
        position={fen}
        boardOrientation={orientation}
        onSquareClick={handleSquare}
        onPieceDrop={(src: string, dst: string, piece: any) =>
          handleDrop(src, dst, piece)
        }
        boardWidth={700}
        customSquareStyles={styles}
        customBoardStyle={{ border: "2px solid #000", borderRadius: "8px" }}
        animationDuration={locked ? 0 : 300}
      />
    </div>
  );
}
