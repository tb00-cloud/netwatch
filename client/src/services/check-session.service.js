import Vue from 'vue'

export function checkSessionState() {
  const state = Vue.$cookies.get("loginState");
  if (state == 1) {
    return true;
  } else {
    return false;
  }
}