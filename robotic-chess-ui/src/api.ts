import axios from "axios";

const API_BASE = process.env.REACT_APP_API_URL!;

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
