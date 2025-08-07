import axios from "axios";

axios.defaults.baseURL = "";

export const sendMove = (
  robotId: "white" | "black",
  from: string,
  to: string
) =>
  axios.post(`/robots/${robotId}/make-move`, {
    from_square: from,
    to_square: to,
  });

export const fetchLatestMove = (robotId: "white" | "black") =>
  axios.get(`/robots/${robotId}/latest-move`);
