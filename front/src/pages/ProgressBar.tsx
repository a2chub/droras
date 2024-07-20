import { useCallback, useEffect, useRef, useState } from "react";

const DURATION = 150;

export function ProgressBar(params: {
	enabled: boolean;
	onComplete: () => void;
}) {
	const timerRef = useRef(0);
	const startTime = useRef(0);
	const [progress, setProgress] = useState(0);
	const [timeText, setTimeText] = useState("0:00");
	const [timeLeftText, setTimeLeftText] = useState(
		`${Math.floor(DURATION / 60)}:${(DURATION % 60)
			.toString()
			.padStart(2, "0")}`,
	);

	const setTime = useCallback((secs: number) => {
		setTimeText(
			`${Math.floor(secs / 60)}:${(secs % 60).toString().padStart(2, "0")}`,
		);
		const leftSecs = DURATION - secs;
		setTimeLeftText(
			`${Math.floor(leftSecs / 60)}:${(leftSecs % 60)
				.toString()
				.padStart(2, "0")}`,
		);
	}, []);

	useEffect(() => {
		function stop(done: boolean) {
			if (timerRef.current) {
				window.clearInterval(timerRef.current);
				timerRef.current = 0;
				if (done) {
					params.onComplete();
				}
			}
		}
		if (params.enabled) {
			startTime.current = Date.now();
			timerRef.current = window.setInterval(() => {
				const elapsed = Math.floor((Date.now() - startTime.current) / 1000);
				if (elapsed > DURATION) {
					stop(true);
					return;
				}
				setTime(elapsed);
				setProgress((elapsed / DURATION) * 100);
			}, 1000);
		} else {
			stop(false);
			setTime(0);
			setProgress(0);
		}
		return () => window.clearInterval(timerRef.current);
	}, [params, setTime]);

	return (
		<div className="relative w-full h-8 overflow-hidden font-bold bg-gray-200 rounded-md">
			<div className="absolute top-0 flex items-center justify-between w-full h-full px-2 text-black ">
				<div>{timeText}</div>
				<div>{timeLeftText}</div>
			</div>
			<div
				className="absolute top-0 flex items-center justify-between w-full h-full px-2 text-white bg-blue-500"
				style={{ clipPath: `inset(0 ${100 - progress}% 0 0)` }}
			>
				<div>{timeText}</div>
				<div>{timeLeftText}</div>
			</div>
		</div>
	);
}
