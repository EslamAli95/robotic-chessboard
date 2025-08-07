import "./UndoDialog.css";
interface UndoDialogProps {
  visible: boolean;
  onAccept: () => void;
  onReject: () => void;
}

export default function UndoDialog({
  visible,
  onAccept,
  onReject,
}: UndoDialogProps) {
  if (!visible) return null;
  return (
    <div className="undo-modal">
      <p>Opponent requests to undo the last move</p>
      <button onClick={onAccept}>Accept</button>
      <button onClick={onReject}>Reject</button>
    </div>
  );
}
