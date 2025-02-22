#! /usr/bin/env poetry run python

import json
import pathlib
import argparse
import logging
import kalpaa
import kalpaa.common
import tantri.cli
import tantri.cli.input_files
import tantri.cli.input_files.write_dipoles
import tantri.dipoles.types
import typing


_logger = logging.getLogger(__name__)

# constants

# DOTS	DOTS	DOTS DOTS DOTS
# DOTS = "dots.json"
# POTENTIAL = "electric-potential"
# X_ELECTRIC_FIELD = "x-electric-field"
# LOG_PATTERN = "%(asctime)s | %(levelname)-7s | %(name)s:%(lineno)d | %(message)s"

# OUT_DIR = "out"

# parameters for iteration
# TODO Consider how these interact with indexes.json
# COUNTS = [1, 10]
# ORIENTATIONS = ["XY", "RANDOM", "Z"]
# NUM_REPLICAS = 3

# config type params, should be logged!
# INDEX_STARTER = 3141

# NUM_SEEDS = 100
# these are obviously not independent but it's just easier than thinking about floats to define them both here
# DELTA_T = 0.05
# SAMPLE_RATE = 10
# NUM_ITERATIONS = 100000 # for the time serieses how many steps

# for binnng
# NUM_BIN_TS = 25
# BIN_WIDTH_LOG = 0.25

# def get_config(count, orientation, seed):
# 	output_dict = {
# 		"x_min": -20,
# 		"x_max": 20,
# 		"y_min": -10,
# 		"y_max": 10,
# 		"z_min": 0,
# 		"z_max": 5,
# 		"mag": 100,
# 		"w_log_min": -4,
# 		"w_log_max": 1,
# 		"orientation": orientation,
# 		"dipole_count": count,
# 		"generation_seed": seed
# 	}
# 	return output_dict

# def set_up_logging(log_file):
# 	if log_file is None:
# 		handlers = [
# 			logging.StreamHandler(),
# 		]
# 	else:
# 		handlers = [
# 			logging.StreamHandler(),
# 			logging.FileHandler(log_file)
# 		]
# 	logging.basicConfig(
# 		level=logging.DEBUG,
# 		format = LOG_PATTERN,
# 		handlers=handlers,
# 	)
# 	logging.getLogger("pdme").setLevel(logging.ERROR)
# 	logging.captureWarnings(True)


class Stage01Runner:
	def __init__(self, config: kalpaa.Config):
		self.config = config
		_logger.info(f"Initialising Stage01 runner with {config=}")

	def generate_single_subdir(
		self, seed: int, count: int, orientation: str, replica: int
	):
		"""
		create a directory, populate it with stuff.
		"""

		_logger.info(
			f"Generating config for {seed=} {count=} {orientation=} {replica=}"
		)
		out = self.config.get_out_dir_path()
		directory = out / f"{orientation.lower()}-{count}-{replica}"
		directory.mkdir(parents=True, exist_ok=True)

		config_json = directory / "generation_config.json"
		dipoles_json = directory / "dipoles.json"

		with open(config_json, "w") as conf_file:
			params = kalpaa.ReducedModelParams(
				count=count, orientation=tantri.dipoles.types.Orientation(orientation)
			)
			_logger.debug(f"Got params {params=}")
			json.dump(params.config_dict(seed), conf_file)
			# json.dump(kalpa.common.model_config_dict(count, orientation, seed), conf_file)

		tantri.cli._generate_dipoles(config_json, dipoles_json, (seed, replica, 1))

		# tantri.cli._write_apsd(dipoles_json, DOTS, X_ELECTRIC_FIELD, DELTA_T, NUM_ITERATIONS, NUM_BIN_TS, (index, replica, 2), output_csv, binned_csv, BIN_WIDTH_LOG, True)
		for tantri_index, tantri_config in enumerate(
			self.config.generation_config.tantri_configs
		):
			output_csv = directory / kalpaa.common.tantri_full_output_name(tantri_index)
			binned_csv = directory / kalpaa.common.tantri_binned_output_name(
				tantri_index
			)
			tantri.cli._write_apsd(
				dipoles_json,
				self.config.general_config.dots_json_name,
				self.config.general_config.measurement_type.value,
				tantri_config.delta_t,
				tantri_config.num_iterations,
				self.config.generation_config.num_bin_time_series,
				(seed, replica, 2),
				output_csv,
				binned_csv,
				self.config.generation_config.bin_log_width,
				True,
			)

	# This whole method is duplication and is ripe for refactor, but that's fine!
	# deliberately bad to get it done.
	# here we're going to be manually specifying dipoles as we have from our config
	def generate_override_dipole(
		self,
		seed: int,
		override_name: str,
		override_dipoles: typing.Sequence[tantri.dipoles.types.DipoleTO],
	):
		"""
		create a directory, populate it with stuff.

		seed: still a seed integer to use
		override_name: the name of this dipole configuration, from config file
		override_dipoles: dipoles to override

		"""

		_logger.info(
			f"Writing override config {override_name} with dipoles: [{override_dipoles}]"
		)
		out = self.config.get_out_dir_path()
		directory = out / f"{override_name}"
		directory.mkdir(parents=True, exist_ok=True)

		_logger.debug("generated override directory")

		# config_json = directory / "generation_config.json"
		dipoles_json = directory / "dipoles.json"

		# with open(config_json, "w") as conf_file:
		# 	params = kalpa.ReducedModelParams(
		# 		count=count, orientation=tantri.dipoles.types.Orientation(orientation)
		# 	)
		# 	_logger.debug(f"Got params {params=}")
		# 	json.dump(params.config_dict(seed), conf_file)
		# 	# json.dump(kalpa.common.model_config_dict(count, orientation, seed), conf_file)

		# the original logic looked like this:
		# tantri.cli._generate_dipoles(config_json, dipoles_json, (seed, replica, 1))
		# We're replicating the bit that wrote the dipoles here, but that's a refactor opportunity
		with dipoles_json.open("w") as dipole_out:
			dipole_out.write(
				json.dumps(
					[dip.as_dict() for dip in override_dipoles],
					cls=tantri.cli.input_files.write_dipoles.NumpyEncoder,
				)
			)

		_logger.info(f"Wrote to dipoles file {dipoles_json}")

		# tantri.cli._write_apsd(dipoles_json, DOTS, X_ELECTRIC_FIELD, DELTA_T, NUM_ITERATIONS, NUM_BIN_TS, (index, replica, 2), output_csv, binned_csv, BIN_WIDTH_LOG, True)
		for tantri_index, tantri_config in enumerate(
			self.config.generation_config.tantri_configs
		):
			output_csv = directory / kalpaa.common.tantri_full_output_name(tantri_index)
			binned_csv = directory / kalpaa.common.tantri_binned_output_name(
				tantri_index
			)
			tantri.cli._write_apsd(
				dipoles_json,
				self.config.general_config.dots_json_name,
				self.config.general_config.measurement_type.value,
				tantri_config.delta_t,
				tantri_config.num_iterations,
				self.config.generation_config.num_bin_time_series,
				(seed, 2),
				output_csv,
				binned_csv,
				self.config.generation_config.bin_log_width,
				True,
			)

	def run(self):
		seed_index = 0
		if self.config.generation_config.override_dipole_configs is None:
			# should be by default
			_logger.debug("no override needed!")
			for count in self.config.generation_config.counts:
				for orientation in self.config.generation_config.orientations:
					for replica in range(self.config.generation_config.num_replicas):
						_logger.info(
							f"Generating for {seed_index=}: [{count=}, {orientation=}, {replica=}"
						)
						self.generate_single_subdir(
							seed_index, count, orientation, replica
						)
						seed_index += 1
		else:
			_logger.debug(
				f"Dipole generation override received: {self.config.generation_config.override_dipole_configs}"
			)
			for (
				override_name,
				override_dipoles,
			) in self.config.generation_config.override_dipole_configs.items():
				self.generate_override_dipole(
					seed_index, override_name, override_dipoles
				)


def parse_args():

	parser = argparse.ArgumentParser(
		"Single dipole 4 config maker",
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	)

	parser.add_argument(
		"--log-file",
		type=str,
		help="A filename for logging to, if not provided will only log to stderr",
		default=None,
	)
	args = parser.parse_args()
	return args


# def gen_config(index: int, count: int, orientation: str, replica: int):
# 	"""
# 	create a directory, populate it with stuff.
# 	"""

# 	_logger.info(f"Generating config for {index=} {count=} {orientation=} {replica=}")
# 	out = pathlib.Path(OUT_DIR)
# 	directory = out / f"{orientation.lower()}-{count}-{replica}"
# 	directory.mkdir(parents=True, exist_ok=True)

# 	config_json = directory/"generation_config.json"
# 	dipoles_json = directory/"dipoles.json"

# 	output_csv = directory/"apsd.csv"
# 	binned_csv = directory/"binned_apsd.csv"

# 	with open(config_json, "w") as conf_file:
# 		json.dump(get_config(count, orientation, index), conf_file)


# 	tantri.cli._generate_dipoles(config_json, dipoles_json, (index, replica, 1))

# 	tantri.cli._write_apsd(dipoles_json, DOTS, X_ELECTRIC_FIELD, DELTA_T, NUM_ITERATIONS, NUM_BIN_TS, (index, replica, 2), output_csv, binned_csv, BIN_WIDTH_LOG, True)


def main():
	args = parse_args()

	tantri_configs = [
		kalpaa.TantriConfig(31415, 100, 5, 100000),
		kalpaa.TantriConfig(314, 100, 0.00005, 100000),
	]
	generation_config = kalpaa.GenerationConfig(
		tantri_configs=tantri_configs,
		counts=[1],
		num_replicas=3,
		orientations=[tantri.dipoles.types.Orientation.Z],
	)

	config = kalpaa.Config(generation_config=generation_config)

	kalpaa.common.set_up_logging(config, args.log_file)

	_logger.info("Generating our data, for the following iterations")

	_logger.info(config)
	# _logger.info(f"{COUNTS=}")
	# _logger.info(f"{ORIENTATIONS=}")
	# _logger.info(f"{NUM_REPLICAS=}")

	# _logger.info("Our parameters used: ")

	# _logger.info(f"\t{INDEX_STARTER=}")

	# _logger.info(f"\t{NUM_SEEDS=}")
	# # these are obviously not independent but it's just easier than thinking about floats to define them both here
	# _logger.info(f"\t{DELTA_T=}")
	# _logger.info(f"\t{SAMPLE_RATE=}")
	# _logger.info(f"\t{NUM_ITERATIONS=}")

	# # for binnng
	# _logger.info(f"\t{NUM_BIN_TS=}")
	# _logger.info(f"\t{BIN_WIDTH_LOG=}")

	runner = Stage01Runner(config)
	runner.run()


if __name__ == "__main__":
	main()
