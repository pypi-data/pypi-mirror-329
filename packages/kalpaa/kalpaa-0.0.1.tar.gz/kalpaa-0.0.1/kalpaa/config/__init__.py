import json
import deepdog.indexify
from dataclasses import dataclass, field
import typing
import tantri.dipoles.types
import pathlib
from enum import Enum, IntEnum
import logging

_logger = logging.getLogger(__name__)


class MeasurementTypeEnum(Enum):
	POTENTIAL = "electric-potential"
	X_ELECTRIC_FIELD = "x-electric-field"


class SkipToStage(IntEnum):
	# shouldn't need this lol
	STAGE_01 = 0
	STAGE_02 = 1
	STAGE_03 = 2
	STAGE_04 = 3


# Copy over some random constants to see if they're ever reused


@dataclass(frozen=True)
class GeneralConfig:
	dots_json_name: str = "dots.json"
	indexes_json_name: str = "indexes.json"
	out_dir_name: str = "out"
	log_pattern: str = (
		"%(asctime)s | %(process)d | %(levelname)-7s | %(name)s:%(lineno)d | %(message)s"
	)
	measurement_type: MeasurementTypeEnum = MeasurementTypeEnum.X_ELECTRIC_FIELD
	root_directory: pathlib.Path = pathlib.Path.cwd()

	mega_merged_name: str = "mega_merged_coalesced.csv"
	mega_merged_inferenced_name: str = "mega_merged_coalesced_inferenced.csv"

	skip_to_stage: typing.Optional[int] = None


@dataclass(frozen=True)
class TantriConfig:
	index_seed_starter: int = 31415
	num_seeds: int = 100
	delta_t: float = 0.05
	num_iterations: int = 100000
	# sample_rate = 10


@dataclass(frozen=True)
class GenerationConfig:
	# Interact with indexes.json, probably should be a subset
	counts: typing.Sequence[int] = field(default_factory=lambda: [1, 10])
	orientations: typing.Sequence[tantri.dipoles.types.Orientation] = field(
		default_factory=lambda: [
			tantri.dipoles.types.Orientation.RANDOM,
			tantri.dipoles.types.Orientation.Z,
			tantri.dipoles.types.Orientation.XY,
		]
	)
	# TODO: what's replica here?
	num_replicas: int = 3

	# the above three can be overrided with manually specified configurations
	override_dipole_configs: typing.Optional[
		typing.Mapping[str, typing.Sequence[tantri.dipoles.types.DipoleTO]]
	] = None

	tantri_configs: typing.Sequence[TantriConfig] = field(
		default_factory=lambda: [TantriConfig()]
	)

	num_bin_time_series: int = 25
	bin_log_width: float = 0.25


@dataclass(frozen=True)
class DeepdogConfig:
	"""
	Class that holds all of the computational parameters
	"""

	costs_to_try: typing.Sequence[float] = field(default_factory=lambda: [10, 1, 0.1])
	target_success: int = 1000
	max_monte_carlo_cycles_steps: int = 20
	# Whether to use a log log cost function
	use_log_noise: bool = False


@dataclass(frozen=True)
class Config:
	generation_config: GenerationConfig = GenerationConfig()
	general_config: GeneralConfig = GeneralConfig()
	deepdog_config: DeepdogConfig = DeepdogConfig()

	def absify(self, filename: str) -> pathlib.Path:
		ret = (self.general_config.root_directory / filename).resolve()
		_logger.debug(f"Absifying {filename=}, geting {ret}")
		return ret

	def get_out_dir_path(self) -> pathlib.Path:
		return self.absify(self.general_config.out_dir_name)

	def get_dots_json_path(self) -> pathlib.Path:
		return self.absify(self.general_config.dots_json_name)

	def indexifier(self) -> deepdog.indexify.Indexifier:
		with self.absify(self.general_config.indexes_json_name).open(
			"r"
		) as indexify_json_file:
			indexify_spec = json.load(indexify_json_file)
			indexify_data = indexify_spec["indexes"]
			if "seed_spec" in indexify_spec:
				seed_spec = indexify_spec["seed_spec"]
				indexify_data[seed_spec["field_name"]] = list(
					range(seed_spec["num_seeds"])
				)

			_logger.info(f"loading indexifier with data {indexify_data=}")
			return deepdog.indexify.Indexifier(indexify_data)


@dataclass(frozen=True)
class ReducedModelParams:
	"""
	Units usually in 10s of nm for distance, s or Hz as needed for time units, log units are log base 10 of Hz or s values.
	"""

	x_min: float = -20
	x_max: float = 20
	y_min: float = -10
	y_max: float = 10
	z_min: float = 5
	z_max: float = 6.5
	w_log_min: float = -5
	w_log_max: float = 1
	count: int = 1
	log_magnitude: float = 2
	orientation: tantri.dipoles.types.Orientation = (
		tantri.dipoles.types.Orientation.RANDOM
	)

	def config_dict(self, seed: int) -> typing.Dict[str, typing.Any]:
		output_dict = {
			"x_min": self.x_min,
			"x_max": self.x_max,
			"y_min": self.y_min,
			"y_max": self.y_max,
			"z_min": self.z_min,
			"z_max": self.z_max,
			"mag": 10**self.log_magnitude,
			"w_log_min": self.w_log_min,
			"w_log_max": self.w_log_max,
			"orientation": self.orientation,
			"dipole_count": self.count,
			"generation_seed": seed,
		}
		return output_dict
