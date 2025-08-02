import { Chess } from "chess.js";

export function buildHighlights(
  selected: string | null,
  destinations: string[],
  chess: Chess
): Record<string, React.CSSProperties> {
  const map: Record<string, React.CSSProperties> = {};
  if (selected) {
    map[selected] = { backgroundColor: "var(--highlight-selected)" };
  }
  destinations.forEach((sq) => {
    map[sq] = { backgroundColor: "var(--highlight-possible)" };
  });
  // Highlight the king in red if that side is in check
  if (chess.isCheck()) {
    const board = chess.board();
    const turn = chess.turn();
    for (let rank = 0; rank < 8; rank++) {
      for (let file = 0; file < 8; file++) {
        const piece = board[rank][file];
        if (piece?.type === "k" && piece.color === turn) {
          const sq = `${"abcdefgh"[file]}${8 - rank}`;
          map[sq] = { backgroundColor: "rgba(255, 1, 1, 0.5)" };
        }
      }
    }
  }
  return map;
}
