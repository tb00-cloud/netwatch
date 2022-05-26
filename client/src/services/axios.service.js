import axios from 'axios';

export function http(params) {
  // let proto = location.protocol
  // let host = location.hostname
  // let base = proto + "//" + host + "/api"
  return axios.create({
    baseURL: "/api/",
    headers: { "Content-Type": "application/json" },
    withCredentials: true,
    params:params
  })
} 