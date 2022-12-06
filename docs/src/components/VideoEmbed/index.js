import React from "react";

export default function VideoEmbed({ url }) {
  return (
    <div style={{ position: "relative", paddingTop: "56.25%" }}>
      <iframe
        src={url}
        style={{
          border: "none",
          position: "absolute",
          top: "0",
          left: "0",
          height: "100%",
          width: "100%",
        }}
        allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture;"
        allowfullscreen="true"
      ></iframe>
    </div>
  );
}
