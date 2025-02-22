import argparse
import pathlib

# import csv
import numpy
import deepdog
import deepdog.direct_monte_carlo.compose_filter
import deepdog.indexify
import deepdog.direct_monte_carlo
import logging

# # import itertools
import pdme

import tantri.cli
import tantri.cli.file_importer
import tantri.dipoles.types
import typing

# import pdme.measurement
#
# # import random
# # import sys
# # import re
# # import math
# # import os
import json

# # from dataclasses import dataclass
#
#
# folder in curr dir
import kalpaa
import kalpaa.common


_logger = logging.getLogger(__name__)

# LOG_PATTERN = "%(asctime)s | %(levelname)-7s | %(name)s:%(lineno)d | %(message)s"


# JOBS = list(range(18))
# TOOD move to json file and read
# COSTS = [10.0, 5.0, 1.0, 0.5, 0.1, 0.06]
# DOTS_DICT = {
# 	"dot1": "dot1",
# 	"dot2": "dot1,dot2",
# 	"line": "dot1,dot2,line",
# 	"triangle1": "dot1,dot2,triangle1",
# 	"triangle2": "dot1,dot2,triangle2",
# 	"uprise1": "dot1,dot2,uprise1",
# 	"uprise2": "dot1,dot2,uprise2",
# }


def enumify_orientation_string(
	orientation_string: str,
) -> tantri.dipoles.types.Orientation:
	canonical_orientation_string = orientation_string.upper()

	if canonical_orientation_string in ["FIXEDZ", "Z"]:
		return tantri.dipoles.types.Orientation.Z

	if canonical_orientation_string in ["FIXEDXY", "XY"]:
		return tantri.dipoles.types.Orientation.XY

	if canonical_orientation_string in ["FREE", "RANDOM"]:
		return tantri.dipoles.types.Orientation.RANDOM

	else:
		raise ValueError(
			f"Could not find match for orientation_string {orientation_string=}"
		)


class Stage02Runner:
	def __init__(self, config: kalpaa.Config):
		self.config = config
		_logger.info(f"Initialising Stage02 runner with {config=}")

		with config.absify(config.general_config.indexes_json_name).open(
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
			self.indexifier = deepdog.indexify.Indexifier(indexify_data)

		self.dots = tantri.cli.file_importer.read_dots_json_file(
			self.config.absify(self.config.general_config.dots_json_name)
		)
		_logger.info(f"Got dots {self.dots=}")

	def _dots_to_include(self, current_dot: str) -> typing.Sequence[str]:
		if current_dot == "dot1":
			return ["dot1"]
		if current_dot == "dot2":
			return ["dot1", "dot2"]
		else:
			return ["dot1", "dot2", current_dot]

	def run_in_subdir(self, subdir: pathlib.Path):
		with kalpaa.common.new_cd(subdir):
			_logger.debug(f"Running inside {subdir=}")

			# TODO hardcoding that we're executing every job index.
			num_jobs = len(self.indexifier)
			_logger.debug(f"Have {num_jobs=}")
			seed_index = 0
			for job_index in range(num_jobs):
				for cost in self.config.deepdog_config.costs_to_try:
					for dot in self.dots:

						seed_index += 1

						combined_dot_name = ",".join(
							[d for d in self._dots_to_include(dot.label)]
						)
						trial_name = (
							f"{dot.label}-{combined_dot_name}-{cost}-{job_index}"
						)
						_logger.info(f"Working on {trial_name=}")
						_logger.debug(f"Have {seed_index=}")
						self.single_run_in_subdir(
							job_index, cost, dot.label, trial_name, seed_index
						)

	def single_run_in_subdir(
		self,
		job_index: int,
		cost: float,
		dot_name: str,
		trial_name: str,
		seed_index: int,
	):
		# _logger.info(f"Got job index {job_index}")
		# NOTE This guy runs inside subdirs, obviously. In something like <kalpa>/out/z-10-2/dipoles

		# we had job_index, trial_name, args let's see what we need

		_logger.debug(
			f"run_analysis() being called with ({job_index=}, {cost=}, {dot_name=}, {trial_name=}, {seed_index=})"
		)

		_logger.info(
			f"Have {self.config.generation_config.tantri_configs} as our tantri_configs"
		)
		num_tantri_configs = len(self.config.generation_config.tantri_configs)
		binned_datas = [
			kalpaa.read_dots_and_binned(
				self.config.get_dots_json_path(),
				pathlib.Path("..")
				/ kalpaa.common.tantri_binned_output_name(tantri_index),
			)
			for tantri_index in range(num_tantri_configs)
		]

		dot_names = self._dots_to_include(dot_name)
		_logger.debug(f"Got dot names {dot_names}")

		models = []

		indexes = self.indexifier.indexify(job_index)

		_logger.debug(f"indexes are {indexes}")

		log_magnitude = indexes["magnitudes"]
		avg_filled = indexes["occupancies"]
		orientation = enumify_orientation_string(indexes["orientations"])
		# we are just finding matches given a single seed so don't need to change this
		seed = seed_index

		# TODO find way to store this as a global config file
		occupancies_dict = {
			1: (500, 1000),
			2: (250, 2000),
			3: (250, 2000),
			5: (100, 5000),
			10: (50, 10000),
			16: (50, 10000),
			17: (50, 10000),
			31: (50, 10000),
			56: (25, 20000),
			100: (5, 100000),
		}

		mccount, mccountcycles = occupancies_dict[avg_filled]

		model_params = kalpaa.ReducedModelParams(
			count=avg_filled, log_magnitude=log_magnitude, orientation=orientation
		)

		models.append(kalpaa.get_model(model_params))

		_logger.info(f"have {len(models)} models to look at")
		if len(models) == 1:
			_logger.info(f"only one model, name: {models[0][0]}")

		deepdog_config = deepdog.direct_monte_carlo.DirectMonteCarloConfig(
			monte_carlo_count_per_cycle=mccount,
			monte_carlo_cycles=mccountcycles,
			target_success=self.config.deepdog_config.target_success,
			max_monte_carlo_cycles_steps=self.config.deepdog_config.max_monte_carlo_cycles_steps,
			monte_carlo_seed=seed,
			write_successes_to_file=True,
			tag=trial_name,
			write_bayesrun_file=True,
		)

		_logger.info(f"{deepdog_config=}")

		stdev_cost_function_filters = [
			b.stdev_cost_function_filter(
				dot_names, cost, self.config.deepdog_config.use_log_noise
			)
			for b in binned_datas
		]

		_logger.debug(f"{stdev_cost_function_filters=}")
		combining_filter = deepdog.direct_monte_carlo.compose_filter.ComposedDMCFilter(
			stdev_cost_function_filters
		)

		run = deepdog.direct_monte_carlo.DirectMonteCarloRun(
			model_name_pairs=models,
			filter=combining_filter,
			config=deepdog_config,
		)
		results = run.execute()
		_logger.info(results)

	def run(self):
		"""Going to iterate over every folder in out_dir, and execute the subdir stuff inside dirs like <kalpa>/out/z-10-2/dipoles"""
		out_dir_path = self.config.get_out_dir_path()
		subdirs = [child for child in out_dir_path.iterdir() if child.is_dir]
		# _logger.info(f"Going to execute within each of the directories in {subdirs=}")
		for subdir in subdirs:
			# skip try finally for now just blow up if problem
			_logger.debug(f"Running for {subdir=}")
			dipoles_dir = subdir / "dipoles"
			dipoles_dir.mkdir(exist_ok=True, parents=False)
			self.run_in_subdir(subdir / "dipoles")


def parse_args():

	parser = argparse.ArgumentParser(
		"Stage02 Runner", formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)

	parser.add_argument(
		"--log-file",
		type=str,
		help="A filename for logging to, if not provided will only log to stderr",
		default=None,
	)
	args = parser.parse_args()
	return args


def main():
	args = parse_args()

	tantri_configs = [
		kalpaa.TantriConfig(31415, 100, 5, 100000),
		kalpaa.TantriConfig(314, 100, 0.00005, 100000),
	]
	generation_config = kalpaa.GenerationConfig(tantri_configs=tantri_configs)

	config = kalpaa.Config(generation_config=generation_config)

	kalpaa.common.set_up_logging(config, args.log_file)

	_logger.info("Generating our data, for the following iterations")

	_logger.info(config)

	runner = Stage02Runner(config)
	runner.run()


if __name__ == "__main__":
	main()
