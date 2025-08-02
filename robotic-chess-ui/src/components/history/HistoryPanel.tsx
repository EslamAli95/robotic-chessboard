import History from "./History";
import UndoDialog from "../undo/UndoDialog";
import DrawDialog from "../draw/DrawDialog";
import { useState } from "react";
import "./History.css";

interface Props {
  moves: string[];
  currentHalf: number;
  onNavigate: (h: number) => void;
  onUndo: () => void;
  onDraw: () => void;
  onResign: () => void;
}

export default function HistoryPanel({
  moves,
  currentHalf,
  onNavigate,
  onUndo,
  onDraw,
  onResign,
}: Props) {
  const [showUndo, setShowUndo] = useState(false);
  const [showDraw, setShowDraw] = useState(false);

  return (
    <>
      <History
        currentHalf={currentHalf}
        moves={moves}
        onNavigate={(h) => onNavigate(h)}
        onUndoRequest={() => setShowUndo(true)}
        onDrawRequest={() => setShowDraw(true)}
        onsignRequest={onResign}
      />
      <UndoDialog
        visible={showUndo}
        onAccept={() => {
          onUndo();
          setShowUndo(false);
        }}
        onReject={() => setShowUndo(false)}
      />
      <DrawDialog
        visible={showDraw}
        onAccept={() => {
          onDraw();
          setShowDraw(false);
        }}
        onReject={() => setShowDraw(false)}
      />
    </>
  );
}
