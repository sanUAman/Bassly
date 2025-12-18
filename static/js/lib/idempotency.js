import { fetchWithResilience } from "./lib/http.js";

let failures = 0;

export async function safeRequest(...args) {
  try {
    const res = await fetchWithResilience(...args);
    failures = 0;
    hideDegradedBanner();
    enableButtons();
    return res;
  } catch (e) {
    failures++;

    if (failures >= 3) {
      showDegradedBanner();
      disableButtons();
    }

    throw e;
  }
}