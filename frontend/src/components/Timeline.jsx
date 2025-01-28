import React from "react";

export default function Timeline({ screenshots }) {
  return (
    <div className="timeline">
      {screenshots.map((screenshot, index) => (
        <div key={index} className="screenshot">
          <img src={} alt="Screenshot" />
          <p>{screenshot.text}</p>
        </div>
      ))}
    </div>
  );
}
