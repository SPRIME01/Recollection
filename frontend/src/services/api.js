const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

export async function fetchTimeline() {
  const response = await fetch(`${API_BASE_URL}/timeline`);
  return await response.json();
}

export async function captureScreenshot() {
  const response = await fetch(`${API_BASE_URL}/capture`, { method: "POST" });
  return await response.json();
}
