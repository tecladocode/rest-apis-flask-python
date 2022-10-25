import React from "react";
import Background from "./background.png";

export default function LockedVideoEmbed() {
  return (
    <div style={{ maxWidth: "720px", margin: "4rem auto 4rem auto" }}>
      <div style={{ position: "relative", paddingTop: "56.25%" }}>
        <div
          style={{
            border: "none",
            position: "absolute",
            top: "0",
            left: "0",
            height: "100%",
            width: "100%",
            textAlign: "center",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <img
            src={Background}
            style={{
              zIndex: 1,
              position: "absolute",
              top: "0",
              left: "0",
              height: "100%",
              width: "100%",
              objectFit: "cover",
              filter: "blur(5px) grayscale(80%) brightness(0.4)",
            }}
          />
          <svg
            style={{ zIndex: 2 }}
            viewBox="0 0 100 100"
            height="50%"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M10.000 50.000 A40.000 40.000 0 1 0 90.000 50.000 A40.000 40.000 0 1 0 10.000 50.000 Z"
              fill="#D9EDFF"
            />
            <path
              d="M71.767,43.426a1.323,1.323,0,0,1,0,1.476C69.6,48.127,60.072,60.827,44.47,60.827s-25.129-12.7-27.3-15.925a1.326,1.326,0,0,1,0-1.476C19.341,40.2,28.868,27.5,44.47,27.5S69.6,40.2,71.767,43.426Z"
              fill="#ffffff"
            />
            <path
              d="M32.568 44.164 A11.902 11.902 0 1 0 56.372 44.164 A11.902 11.902 0 1 0 32.568 44.164 Z"
              fill="#B0D9FF"
            />
            <path
              d="M71.767,43.426a1.323,1.323,0,0,1,0,1.476C69.6,48.127,60.072,60.827,44.47,60.827s-25.129-12.7-27.3-15.925a1.326,1.326,0,0,1,0-1.476C19.341,40.2,28.868,27.5,44.47,27.5S69.6,40.2,71.767,43.426Z"
              fill="none"
              stroke="#020064"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M32.568 44.164 A11.902 11.902 0 1 0 56.372 44.164 A11.902 11.902 0 1 0 32.568 44.164 Z"
              fill="none"
              stroke="#020064"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M39.841 44.164 A4.629 4.629 0 1 0 49.099 44.164 A4.629 4.629 0 1 0 39.841 44.164 Z"
              fill="#ffffff"
            />
            <path
              d="M39.841 44.164 A4.629 4.629 0 1 0 49.099 44.164 A4.629 4.629 0 1 0 39.841 44.164 Z"
              fill="none"
              stroke="#020064"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M31.820 69.282 A12.65 1.725 0 1 0 57.120 69.282 A12.65 1.725 0 1 0 31.820 69.282 Z"
              fill="#B0D9FF"
            />
            <path
              d="M56.917 54.275 L80.377 54.275 L80.377 72.623 L56.917 72.623 Z"
              fill="#B0D9FF"
            />
            <path
              d="M59.263,54.275v-4.3A9.774,9.774,0,0,1,69.038,40.2h0a9.774,9.774,0,0,1,9.774,9.775v4.3H74.9v-4.3a5.865,5.865,0,0,0-5.865-5.865h0a5.865,5.865,0,0,0-5.865,5.865v4.3Z"
              fill="#ffffff"
              stroke="#020064"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M56.917 54.275 L80.377 54.275 L80.377 72.623 L56.917 72.623 Z"
              fill="none"
              stroke="#020064"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M71.775,62.066a2.737,2.737,0,1,0-3.91,2.463v1.447a1.173,1.173,0,0,0,1.173,1.173h0a1.173,1.173,0,0,0,1.173-1.173V64.529A2.729,2.729,0,0,0,71.775,62.066Z"
              fill="#ffffff"
              stroke="#020064"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <p
            style={{
              zIndex: 2,
              textAlign: "center",
              color: "#020064",
              color: "white",
              fontWeight: "bolder",
            }}
          >
            This video is locked. Please{" "}
            <a href="https://go.tecla.do/rest-apis-ebook">
              purchase the course
            </a>{" "}
            to view it.
          </p>
        </div>
      </div>
    </div>
  );
}
