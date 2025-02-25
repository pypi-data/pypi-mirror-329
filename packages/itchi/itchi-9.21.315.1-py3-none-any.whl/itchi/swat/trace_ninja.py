import logging
from pathlib import Path
from pydantic import BaseModel, ConfigDict
from typing import Optional
from itchi.swat.encoding import DecoderConfig, ObjectEncoding
from itchi.config import SwatConfig


class TraceNinjaConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    winidea_workspace: Path
    trace_recording_duration_ms: int = 10_000
    trace_bin: Path
    trace_txt: Path
    trace_btf: Path
    decoder: DecoderConfig

    def write(self, json_path: Path):
        logging.info(f"Write '{json_path}'.")
        json_str = self.model_dump_json(indent=4, exclude_none=True)
        with open(json_path, "w") as f:
            f.write(json_str)

    def append_encoding(self, encoding: ObjectEncoding):
        self.decoder.objects.append(encoding)


def get_trace_ninja_config(config: SwatConfig) -> TraceNinjaConfig:
    c = TraceNinjaConfig(
        winidea_workspace=config.winidea_workspace,
        trace_bin=config.trace_file_name.with_suffix(".bin"),
        trace_txt=config.trace_file_name.with_suffix(".txt"),
        trace_btf=config.trace_file_name.with_suffix(".btf"),
        decoder=DecoderConfig(),
    )
    return c
