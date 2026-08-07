import axios from "axios";

export const authClient = axios.create({
  baseURL: "http://35.154.105.107:8001",
  headers: { "Content-Type": "application/json" },
});
