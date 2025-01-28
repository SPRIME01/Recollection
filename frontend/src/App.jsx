import React, { useState, useEffect } from "react";
import Timeline from "./components/Timeline";
import { fetchTimeline } from "./services/api";

export default function App() {
  const [screenshots, setScreenshots] = useState([]);

  useEffect(() => {
    fetchTimeline().then(data => setScreenshots(data.screenshots));
  }, []);

  return (
    <div>
      <h1>recollection</h1>
      <Timeline screenshots={screenshots} />
    </div>
  );
}
