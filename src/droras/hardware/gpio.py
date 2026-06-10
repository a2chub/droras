"""GPIO implementation of StartSignal using gpiozero."""

import logging

logger = logging.getLogger(__name__)


class GpioStartSignal:
    def __init__(self, pin: int = 26) -> None:
        from gpiozero import LED  # delayed import to avoid GPIO init at module load
        self._led = LED(pin)

    def on(self) -> None:
        self._led.on()
        logger.info("GpioStartSignal: on")

    def off(self) -> None:
        self._led.off()
        logger.info("GpioStartSignal: off")
