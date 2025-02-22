import argparse
import pathlib

# import csv
import numpy
import csv
import deepdog
import deepdog.cli.probs
import deepdog.cli.probs.main
import deepdog.direct_monte_carlo.compose_filter
import deepdog.indexify
import deepdog.direct_monte_carlo
import logging

# # import itertools
import pdme

import kalpaa.stages
import kalpaa.stages.stage03_1
import tantri.cli
import tantri.cli.file_importer
import tantri.dipoles.types

# # from dataclasses import dataclass
#
#
# folder in curr dir
import kalpaa
import kalpaa.common


_logger = logging.getLogger(__name__)


OUT_FIELDNAMES = [
	"dot_name",
	"target_cost",
	"xmin",
	"xmax",
	"ymin",
	"ymax",
	"zmin",
	"zmax",
	"orientation",
	"avg_filled",
	"log_magnitude",
	"calculations_coalesced",
	"success",
	"count",
	"prob",
]


def coalesced_filename(dot_name, target_cost) -> str:
	return f"coalesced-{dot_name}-{target_cost}.csv"


def read_coalesced_csv(parent_path: pathlib.Path, dot_name: str, target_cost):
	# csv_name = f"coalesced-{dot_name}-{target_cost}.csv"
	csv_path = parent_path / coalesced_filename(dot_name, target_cost)
	_logger.debug(f"{csv_path=}")
	with csv_path.open("r", newline="") as csvfile:
		reader = csv.DictReader(csvfile)
		out_list = []
		for row in reader:
			row["dot_name"] = dot_name
			row["target_cost"] = target_cost
			out_list.append(row)
		return out_list


class Stage03Runner:
	def __init__(self, config: kalpaa.Config):
		self.config = config
		_logger.info(f"Initialising Stage03 runner with {config=}")

		self.indexifier = self.config.indexifier()

		self.dots = [
			d.label
			for d in tantri.cli.file_importer.read_dots_json_file(
				self.config.absify(self.config.general_config.dots_json_name)
			)
		]
		_logger.info(f"Got dots {self.dots=}")

	def merge_coalesceds(self, sorted_dir: pathlib.Path):
		out_path = sorted_dir / kalpaa.common.merged_coalesced_name()
		with out_path.open("w", newline="") as outfile:
			writer = csv.DictWriter(outfile, OUT_FIELDNAMES)
			writer.writeheader()
			for dot in self.dots:
				for cost in self.config.deepdog_config.costs_to_try:
					_logger.info(f"Reading {dot=} {cost=}")
					rows = read_coalesced_csv(sorted_dir, dot, cost)
					for row in rows:
						writer.writerow(row)

	def run_in_subdir(self, subdir: pathlib.Path):
		"""
		Subdir passed in should be e.g. <>/out/z-10-1/
		"""
		with kalpaa.common.new_cd(subdir):

			_logger.debug(f"Running inside {subdir=}")

			kalpaa.stages.stage03_1.move_all_in_dipoles(subdir / "dipoles")

			seed_index = 0

			sorted_dir = pathlib.Path(kalpaa.common.sorted_bayesruns_name())
			_logger.info(f"{sorted_dir.resolve()}")

			for cost in self.config.deepdog_config.costs_to_try:
				for dot in self.dots:

					seed_index += 1
					# TODO pull out
					sorted_subdir = sorted_dir / f"{dot}-{cost}"

					# TODO need to refactor deepdog probs method so I don't have to dump into args like this
					probs_args = argparse.Namespace()
					probs_args.bayesrun_directory = sorted_subdir
					probs_args.indexify_json = self.config.absify(
						self.config.general_config.indexes_json_name
					)
					probs_args.coalesced_keys = ""
					probs_args.uncoalesced_outfile = None
					probs_args.coalesced_outfile = sorted_dir / coalesced_filename(
						dot, cost
					)

					deepdog.cli.probs.main.main(probs_args)

			self.merge_coalesceds(sorted_dir)

	# def run_in_subdir(self, subdir: pathlib.Path):
	#

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
			self.run_in_subdir(subdir)


def parse_args():

	parser = argparse.ArgumentParser(
		"Stage03 Runner", formatter_class=argparse.ArgumentDefaultsHelpFormatter
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

	runner = Stage03Runner(config)
	runner.run()


if __name__ == "__main__":
	main()
