import tomli
import pathlib
from kalpaa.config import (
	Config,
	# GenerationConfig,
	GeneralConfig,
	# DeepdogConfig,
	MeasurementTypeEnum,
)
import tantri.dipoles.types
import dacite
import numpy

import logging

_logger = logging.getLogger(__name__)

_common_dacite_config = dacite.Config(
	strict=True,
	type_hooks={numpy.ndarray: numpy.array},
	cast=[MeasurementTypeEnum, pathlib.Path, tantri.dipoles.types.Orientation],
)


def read_general_config_dict(general_config_dict: dict) -> GeneralConfig:
	"""
	Converts a dictionary to a GeneralConfig object

	:param general_config_dict: dictionary containing general config values
	:return: GeneralConfig object
	"""
	general_config = dacite.from_dict(
		data_class=GeneralConfig,
		data=general_config_dict,
		config=_common_dacite_config,
	)
	return general_config


def read_config_dict(file_path: pathlib.Path) -> dict:
	"""
	Reads a TOML file and returns the contents as a dictionary

	:param file_path: path to the TOML file
	:return: dictionary containing the config values
	"""
	_logger.debug(f"Reading config from {file_path=}")
	with open(file_path, "rb") as toml_file:
		config_dict = tomli.load(toml_file)
	return config_dict


def serialize_config(config_dict: dict) -> Config:
	"""
	Converts a dictionary to a Config object

	Makes assumptions about structure of the config_dict, so validation should happen here too if needed.

	:param config_dict: dictionary containing config values
	:return: Config object
	"""
	# generation_config = GenerationConfig(**config_dict["generation_config"])

	# general_config_dict = config_dict["general_config"]
	# general_config = GeneralConfig(
	# 	root_directory=general_config_dict["root_directory"],
	# 	out_dir_name=general_config_dict["out_dir_name"],
	# 	dots_json_name=general_config_dict["dots_json_name"],
	# 	mega_merged_name=general_config_dict["mega_merged_name"],
	# 	mega_merged_inferenced_name=general_config_dict["mega_merged_inferenced_name"],
	# 	skip_to_stage=general_config_dict["skip_to_stage"],
	# 	measurement_type=MeasurementTypeEnum(general_config_dict["measurement_type"]),
	# 	indexes_json_name=general_config_dict["indexes_json_name"],
	# 	log_pattern=general_config_dict["log_pattern"],
	# )

	# deepdog_config = DeepdogConfig(**config_dict["deepdog_config"])
	# config = Config(
	# 	generation_config=generation_config,
	# 	general_config=general_config,
	# 	deepdog_config=deepdog_config,
	# )
	config = dacite.from_dict(
		data_class=Config,
		data=config_dict,
		config=_common_dacite_config,
	)
	_logger.warning(config)

	return config


def read_config(file_path: pathlib.Path) -> Config:
	config_dict = read_config_dict(file_path)
	return serialize_config(config_dict)
