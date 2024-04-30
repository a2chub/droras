import { useSocket } from "@/lib/socket";

export function HeatNumber() {
	const { currentHeat } = useSocket();
	if (currentHeat > 0) {
		return (
			<div className="my-1 mx-2 text-4xl font-[Impact]">{currentHeat}</div>
		);
	}
	return null;
}
