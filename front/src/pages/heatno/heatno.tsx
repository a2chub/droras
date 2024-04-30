// import React from 'react'
import ReactDOM from "react-dom/client";
import { HeatNumber } from "./HeatNumber";
import "../index.css";
import "./heatno.css";

// biome-ignore lint/style/noNonNullAssertion: <explanation>
ReactDOM.createRoot(document.getElementById("root")!).render(
	// <React.StrictMode>
	<HeatNumber />,
	// </React.StrictMode>,
);
