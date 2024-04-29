import { useCallback, useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { useSocket } from "@/lib/socket";
import { ProgressBar } from "./ProgressBar";

const TableRow = (params: {
	heatNo: number;
	className: string;
	pilots: string[];
	focus: boolean;
}) => {
	return (
		<tr
			className={
				params.focus
					? "border-y-2 border-green-500/50 text-2xl font-bold bg-green-500/20"
					: "border-b"
			}
		>
			<td className="py-3 text-center">{params.heatNo}</td>
			<td className="text-center">{params.className}</td>
			<td className="text-center">{params.pilots[0]}</td>
			<td className="text-center">{params.pilots[1]}</td>
			<td className="text-center">{params.pilots[2]}</td>
		</tr>
	);
};

function App() {
	// currentHeat is 1-based
	const {
		currentHeat,
		setCurrentHeat,
		heatList,
		startHeat,
		reloadHeatList,
		downloadHeatList,
		uploadLog,
	} = useSocket();
	const numHeats = heatList.length;

	const [timerEnabled, setTimerEnabled] = useState(false);

	useEffect(() => {
		if (currentHeat > 0) {
			window.history.pushState({}, "", `/${currentHeat}`);
		}
	}, [currentHeat]);

	const handleStart = useCallback(() => {
		if (timerEnabled) {
			setTimerEnabled(false);
		} else {
			setTimerEnabled(true);
			startHeat();
		}
	}, [timerEnabled, startHeat]);

	const goPrev = useCallback(() => {
		setTimerEnabled(false);
		setCurrentHeat(((currentHeat - 1 + numHeats - 1) % numHeats) + 1);
	}, [currentHeat, numHeats, setCurrentHeat]);

	const goNext = useCallback(() => {
		setTimerEnabled(false);
		setCurrentHeat(((currentHeat - 1 + 1) % numHeats) + 1);
	}, [currentHeat, numHeats, setCurrentHeat]);

	const c = currentHeat - 1; // to zero-based to lookup from the heat list
	const prev = heatList[(c + numHeats - 1) % numHeats];
	const current = heatList[c];
	const next = heatList[(c + 1) % numHeats];

	useEffect(() => {
		function onKeyDown(e: KeyboardEvent) {
			switch (e.key) {
				case "1":
					handleStart();
					break;
				case "2":
					goPrev();
					break;
				case "3":
					goNext();
					break;
			}
		}
		window.addEventListener("keydown", onKeyDown);
		return () => window.removeEventListener("keydown", onKeyDown);
	}, [handleStart, goPrev, goNext]);

	return (
		<div className="container max-w-screen-md pt-4 mx-auto text-lg">
			<table className="w-full mb-6 table-auto">
				<thead>
					<tr className="border-b-2">
						<th className="py-3">Heat</th>
						<th>Class</th>
						<th>E1 / 5705</th>
						<th>F1 / 5740</th>
						<th>F4 / 5800</th>
					</tr>
					{prev && (
						<TableRow
							heatNo={((c + numHeats - 1) % numHeats) + 1}
							className={prev.className}
							pilots={prev.pilots}
							focus={false}
						/>
					)}
					{current && (
						<TableRow
							heatNo={c + 1}
							className={current.className}
							pilots={current.pilots}
							focus={true}
						/>
					)}
					{next && (
						<TableRow
							heatNo={((c + 1) % numHeats) + 1}
							className={next.className}
							pilots={next.pilots}
							focus={false}
						/>
					)}
				</thead>
			</table>
			<div className="w-full my-6">
				<ProgressBar enabled={timerEnabled} onComplete={goNext} />
			</div>
			<div className="flex justify-center gap-4 mt-6">
				<Button
					className={`py-6 text-xl ${
						timerEnabled
							? "bg-red-500 hover:bg-red-500/90"
							: "bg-green-600 hover:bg-green-600/90"
					} `}
					onClick={handleStart}
				>
					{timerEnabled ? "ストップ" : "スタート"}
					<kbd className="flex items-center justify-center w-6 h-6 ml-2 bg-gray-800 rounded text-md">
						1
					</kbd>
				</Button>
				<Button
					className="py-6 text-xl bg-slate-400 hover:bg-slate-400/90"
					onClick={goPrev}
				>
					前のヒート
					<kbd className="flex items-center justify-center w-6 h-6 ml-2 bg-gray-800 rounded text-md">
						2
					</kbd>
				</Button>
				<Button
					className="py-6 text-xl bg-blue-600 hover:bg-blue-600/90"
					onClick={goNext}
				>
					次のヒート
					<kbd className="flex items-center justify-center w-6 h-6 ml-2 bg-gray-800 rounded text-md">
						3
					</kbd>
				</Button>
			</div>
			<hr className="my-6" />
			<div className="flex justify-center gap-4 text-gray-400">
				<Button variant="outline" size="sm" onClick={reloadHeatList}>
					ヒートリスト再読み込み
				</Button>
				<Button variant="outline" size="sm" onClick={downloadHeatList}>
					ヒートリスト再ダウンロード
				</Button>
				<Button variant="outline" size="sm" onClick={uploadLog}>
					ログアップロード
				</Button>
			</div>
		</div>
	);
}

export default App;
