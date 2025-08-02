import "./DrawDialog.css";

export interface DrawDialogProps {
  visible: boolean;
  onAccept: () => void;
  onReject: () => void;
}

export default function DrawDialog({
  visible,
  onAccept,
  onReject,
}: DrawDialogProps) {
  if (!visible) return null;
  return (
    <div className="draw-modal-backdrop">
      <div className="draw-modal">
        <p>Your opponent offers a draw. Do you accept?</p>
        <div className="draw-modal-buttons">
          <button onClick={onAccept}>Accept</button>
          <button onClick={onReject}>Reject</button>
        </div>
      </div>
    </div>
  );
}
