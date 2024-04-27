// import React from 'react'
import ReactDOM from "react-dom/client";
import { PilotsTelop } from "./PilotsTelop";
import "../index.css";
import "./telop.css";

// biome-ignore lint/style/noNonNullAssertion: <explanation>
ReactDOM.createRoot(document.getElementById("root")!).render(
	// <React.StrictMode>
	<PilotsTelop />,
	// </React.StrictMode>,
);
