import axios from "axios";

const API_BASE =
  process.env.REACT_APP_API_URL ||
  (process.env.NODE_ENV === "production"
    ? "https://robotic-chess-backend.onrender.com"
    : "http://127.0.0.1:8000");

export const sendMove = (
  robotId: "white" | "black",
  from: string,
  to: string
) =>
  axios.post(`${API_BASE}/robots/${robotId}/make-move`, {
    from_square: from,
    to_square: to,
  });

export const fetchLatestMove = (robotId: "white" | "black") =>
  axios.get(`${API_BASE}/robots/${robotId}/latest-move`);
