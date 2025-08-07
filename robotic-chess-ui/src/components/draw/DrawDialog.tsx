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
        <p>Your opponent has offered a draw. Do you accept?</p>
        <div className="draw-modal-buttons">
          <button className="confirm" onClick={onAccept}>
            Yes
          </button>
          <button className="cancel" onClick={onReject}>
            No
          </button>
        </div>
      </div>
    </div>
  );
}
