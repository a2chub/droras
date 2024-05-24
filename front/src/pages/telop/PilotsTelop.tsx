import { useSocket } from "@/lib/socket";

export function PilotsTelop() {
	const { currentHeat, heatList } = useSocket();

	if (currentHeat <= 0) return null;

	const heatIndex = currentHeat - 1;
	const pilots = heatList[heatIndex] ? heatList[heatIndex].pilots : [];

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
