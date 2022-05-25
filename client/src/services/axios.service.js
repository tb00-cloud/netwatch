import axios from 'axios';

export function http(params) {
  return axios.create({
    baseURL: "http://localhost:5000",
    headers: { "Content-Type": "application/json" },
    withCredentials: true,
    params:params
  })
} 