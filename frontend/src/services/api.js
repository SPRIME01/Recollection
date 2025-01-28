export async function fetchTimeline() {
  const response = await fetch("/timeline");
  return await response.json();
}

export async function captureScreenshot() {
  const response = await fetch("/capture", { method: "POST" });
  return await response.json();
}
