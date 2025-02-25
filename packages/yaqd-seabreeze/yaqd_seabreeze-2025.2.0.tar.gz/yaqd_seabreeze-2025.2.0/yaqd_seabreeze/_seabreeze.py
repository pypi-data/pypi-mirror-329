from __future__ import annotations

__all__ = ["Seabreeze"]

import asyncio
import numpy as np

from seabreeze.spectrometers import Spectrometer  # type: ignore
from yaqd_core import HasMapping, HasMeasureTrigger, IsSensor, IsDaemon


class Seabreeze(HasMapping, HasMeasureTrigger, IsSensor, IsDaemon):
    _kind = "seabreeze"

    def __init__(self, name, config, config_filepath):
        self.spec = Spectrometer.from_serial_number(config.get("serial"))

        super().__init__(name, config, config_filepath)
        self.serial = config["serial"] or self.spec.serial_number
        self.model = config["model"] or self.spec.model

        self._correct_dark_counts = config.get("correct_dark_counts", False)
        self._correct_nonlinearity = config.get("correct_nonlinearity", False)

        self._channel_names = ["mean", "std", "max", "min"]
        self._channel_units = {k: None for k in self._channel_names}
        self._channel_shapes = {k: (self.spec.pixels,) for k in self._channel_names}
        self._channel_mappings = {k: ["wavelengths"] for k in self._channel_names}
        self._mappings["wavelengths"] = self.spec.wavelengths()
        self._mapping_units = {"wavelengths": "nm"}
        self._acquisition_limits = (1, 512)  # self-imposed limits

        if self._state["integration_time_micros"]:
            self.set_integration_time_micros(self._state["integration_time_micros"])

    async def _measure(self):
        raw = []
        for _ in range(self._state["acquisition_number"]):
            raw.append(
                self.spec.intensities(self._correct_dark_counts, self._correct_nonlinearity)
            )
            await asyncio.sleep(0.0)
        raw = np.array(raw)
        out = {}
        if self._state["acquisition_number"] == 1:
            out["mean"] = out["min"] = out["max"] = raw[0]
            out["std"] = np.full(raw.shape[1:], fill_value=0)
        else:
            out["mean"] = raw.mean(axis=0)
            out["max"] = raw.max(axis=0)
            out["min"] = raw.min(axis=0)
            out["std"] = raw.std(axis=0)
        return out

    def set_integration_time_micros(self, micros: int) -> None:
        """Set the integration time in microseconds"""
        self._state["integration_time_micros"] = micros
        self.spec.integration_time_micros(micros)

    def get_integration_time_micros(self) -> int:
        """Get the integration time in microseconds"""
        return self._state["integration_time_micros"]

    def get_integration_time_units(self) -> str:
        return "us"

    def get_integration_time_limits(self) -> tuple[int, int]:
        return self.spec.integration_time_micros_limits

    def set_acquisitions(self, n: int):
        self._state["acquisition_number"] = min(
            max(self._acquisition_limits[0], n), self._acquisition_limits[1]
        )

    def get_acquisitions(self) -> int:
        return self._state["acquisition_number"]

    def get_acquisitions_limits(self) -> tuple[int, int]:
        return self._acquisition_limits
