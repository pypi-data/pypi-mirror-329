from __future__ import annotations

import asyncio
import numpy as np
import pathlib
import importlib.util

from seabreeze.spectrometers import Spectrometer  # type: ignore
from yaqd_core import HasMapping, HasMeasureTrigger, IsSensor, IsDaemon


__all__ = ["SeabreezeScript"]


class SeabreezeScript(HasMapping, HasMeasureTrigger, IsSensor, IsDaemon):
    _kind = "seabreeze-script"

    def __init__(self, name, config, config_filepath):
        self.spec = Spectrometer.from_serial_number(config.get("serial"))

        super().__init__(name, config, config_filepath)
        self.serial = config["serial"] or self.spec.serial_number
        self.model = config["model"] or self.spec.model

        self._correct_dark_counts = config.get("correct_dark_counts", False)
        self._correct_nonlinearity = config.get("correct_nonlinearity", False)

        path = pathlib.Path(self._config["processing_path"])
        if (
            file_spec := importlib.util.spec_from_file_location(
                path.name.removesuffix(path.suffix), path
            )
        ) is not None:
            self.processing_module = importlib.util.module_from_spec(file_spec)
            file_spec.loader.exec_module(self.processing_module)
        else:
            raise ImportError(f"cannot find shots_processing in path {path}")

        self._mappings["wavelengths"] = self.spec.wavelengths()
        self._mapping_units = {"wavelengths": "nm"}

        self._channel_names = self.processing_module.channel_names  # expected by parent
        self._channel_units = self.processing_module.channel_units  # expected by parent
        self._channel_mappings = self.processing_module.channel_mappings  # expected by parent
        self._channel_shapes = {
            k: (self.spec.pixels,) if self._channel_mappings[k] == "spec" else (1,)
            for k in self.processing_module.channel_names
        }

        self._acquisition_limits = (1, 1024)  # self-imposed limits

        if self._state["integration_time_micros"]:
            self.set_integration_time_micros(self._state["integration_time_micros"])

    async def _measure(self):
        raw = []
        for _ in range(self._state["acquisition_number"]):
            raw.append(
                self.spec.intensities(self._correct_dark_counts, self._correct_nonlinearity)
            )
            await asyncio.sleep(0.0)
        try:
            out = self.processing_module.process(np.array(raw))
        except Exception as e:
            self.logger.error(e)
            out = {name: np.full(shape, np.nan) for name, shape in self._channel_shapes.items()}
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
