import { useEffect, useState } from "react";

const address = import.meta.env.DEV ? "http://localhost:8000" : "";

export function PilotsTelop() {
	const [pilots, setPilots] = useState<string[]>([]);

	useEffect(() => {
		async function fetchPilots() {
			try {
				const response = await fetch(`${address}/current_pilots`);
				const data = await response.json();
				console.log(data);
				setPilots(data);
			} catch (error) {
				console.error("Failed to fetch pilots:", error);
			}
		}

		fetchPilots();
		const intervalId = setInterval(fetchPilots, 2000);

		return () => clearInterval(intervalId);
	}, []);

	return (
		<div className="flex justify-around w-full my-2 text-xl font-bold">
			<div className="w-full text-center">
				{pilots.length > 0 ? pilots[0] : ""}
			</div>
			<div className="w-full text-center">
				{pilots.length > 1 ? pilots[1] : ""}
			</div>
			<div className="w-full text-center">
				{pilots.length > 2 ? pilots[2] : ""}
			</div>
		</div>
	);
}
