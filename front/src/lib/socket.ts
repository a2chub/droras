import { useEffect, useState } from "react";
import io from "socket.io-client";

const address = import.meta.env.DEV ? "ws://localhost:8000/" : "";
const socket = io(address, { transports: ["websocket"] });

export type HeatData = {
	className: string;
	pilots: string[];
};

export const useSocket = () => {
	const [currentHeat, _setCurrentHeat] = useState(0);
	const [heatList, setHeatList] = useState<HeatData[]>([]);

	useEffect(() => {
		function onCurrentHeat(heat: number) {
			_setCurrentHeat(heat);
		}
		function onHeatList(rawHeatList: string[][]) {
			setHeatList(
				rawHeatList.map((row: string[]) => ({
					className: row[4],
					pilots: row.slice(0, 3),
				})),
			);
		}
		socket.on("current_heat", onCurrentHeat);
		socket.on("heat_list", onHeatList);
		return () => {
			socket.off("current_heat", onCurrentHeat);
			socket.off("heat_list", onHeatList);
		};
	}, []);

	const setCurrentHeat = (heat: number) => {
		_setCurrentHeat(heat);
		socket.emit("set_current_heat", heat);
	};

	const startHeat = () => {
		socket.emit("start_heat");
	};

	const reloadHeatList = () => {
		socket.emit("reload_heat_list");
	};

	const downloadHeatList = () => {
		socket.emit("download_heat_list");
	};

	const uploadLog = () => {
		socket.emit("upload_log");
	};

	return {
		currentHeat,
		heatList,
		setCurrentHeat,
		startHeat,
		reloadHeatList,
		downloadHeatList,
		uploadLog,
	};
};
