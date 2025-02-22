import typing
import logging
import argparse
import csv
import kalpaa
import kalpaa.common
import kalpaa.inference_coalesce
import tantri.dipoles.types

_logger = logging.getLogger(__name__)


ORIENTATION_DICT = {
	"XY": "fixedxy",
	"RANDOM": "free",
	"Z": "fixedz",
}

# could be detected but why not just hardcode
MERGED_OUT_FIELDNAMES = [
	"subdir_name",
	"actual_orientation",
	"actual_avg_filled",
	"generation_replica_index",
	"is_row_actual",
	# old fields
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

INFERENCED_OUT_FIELDNAMES = [
	"subdir_name",
	"actual_orientation",
	"actual_avg_filled",
	"generation_replica_index",
	"is_row_actual",
	# old fields
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
	"coalesced_prob",
]


def is_actual(row, actual_normal_orientation, actual_count):
	_logger.debug(f"Check orientations")
	row_or = row["orientation"]
	_logger.debug(f"row: {row_or}, actual: {actual_normal_orientation}")
	is_or = row_or == actual_normal_orientation

	_logger.debug(f"Check counts")
	row_count = row["avg_filled"]
	_logger.debug(f"row: {row_count}, actual: {actual_count}")
	is_count = int(row_count) == int(actual_count)

	_logger.debug(f"Check magnitude")
	row_logmag = row["log_magnitude"]
	# TODO hardcoding
	is_mag = int(row_logmag) == 2

	_logger.debug(f"{is_or=} and {is_count=}and {is_mag=}")
	if is_or and is_count and is_mag:
		_logger.debug("Returning 1")
		return 1
	else:
		_logger.debug("Returning 0")
		return 0


class Stage04Runner:
	def __init__(self, config: kalpaa.Config):
		self.config = config
		_logger.info(f"Initialising Stage04 runner with {config=}")

		self.indexifier = self.config.indexifier()

	def read_merged_coalesced_csv(self, orientation, count, replica) -> typing.Sequence:
		subdir_name = f"{orientation.lower()}-{count}-{replica}"
		subdir_path = self.config.get_out_dir_path() / subdir_name
		csv_path = (
			subdir_path
			/ kalpaa.common.sorted_bayesruns_name()
			/ kalpaa.common.merged_coalesced_name()
		)
		_logger.debug(f"Reading {csv_path=}")
		with csv_path.open(mode="r", newline="") as csvfile:
			reader = csv.DictReader(csvfile)
			out_list = []
			for row in reader:
				normal_orientation = ORIENTATION_DICT[orientation]
				row["subdir_name"] = subdir_name
				row["actual_orientation"] = ORIENTATION_DICT[orientation]
				row["actual_avg_filled"] = count
				row["generation_replica_index"] = replica
				row["is_row_actual"] = is_actual(row, normal_orientation, count)
				out_list.append(row)
			return out_list

	def read_merged_coalesced_csv_override(self, override_name: str) -> typing.Sequence:
		subdir_name = override_name
		subdir_path = self.config.get_out_dir_path() / subdir_name
		csv_path = (
			subdir_path
			/ kalpaa.common.sorted_bayesruns_name()
			/ kalpaa.common.merged_coalesced_name()
		)
		_logger.debug(f"Reading {csv_path=}")
		with csv_path.open(mode="r", newline="") as csvfile:
			reader = csv.DictReader(csvfile)
			out_list = []
			for row in reader:
				# We can't put any of the actual info in because it's totally arbitrary, but that's fine!

				# normal_orientation = ORIENTATION_DICT[orientation]
				row["subdir_name"] = subdir_name
				# row["actual_orientation"] = ORIENTATION_DICT[orientation]
				# row["actual_avg_filled"] = count
				# row["generation_replica_index"] = replica
				# row["is_row_actual"] = is_actual(row, normal_orientation, count)
				out_list.append(row)
			return out_list

	def run(self):
		megamerged_path = (
			self.config.get_out_dir_path() / self.config.general_config.mega_merged_name
		)

		# normal merged
		with megamerged_path.open(mode="w", newline="") as outfile:
			writer = csv.DictWriter(outfile, MERGED_OUT_FIELDNAMES)
			writer.writeheader()

			if self.config.generation_config.override_dipole_configs is None:

				for count in self.config.generation_config.counts:
					for orientation in self.config.generation_config.orientations:
						for replica in range(
							self.config.generation_config.num_replicas
						):
							_logger.info(f"Reading {count=} {orientation=} {replica=}")
							rows = self.read_merged_coalesced_csv(
								orientation, count, replica
							)
							for row in rows:
								writer.writerow(row)

			else:
				_logger.debug(
					f"We had overridden dipole config, using override {self.config.generation_config.override_dipole_configs}"
				)
				for (
					override_name
				) in self.config.generation_config.override_dipole_configs.keys():
					_logger.info(f"Working for subdir {override_name}")
					rows = self.read_merged_coalesced_csv_override(override_name)
					for row in rows:
						writer.writerow(row)

		# merge with inference

		if self.config.generation_config.override_dipole_configs is None:

			with megamerged_path.open(mode="r", newline="") as infile:
				# Note that if you pass in fieldnames to a DictReader it doesn't skip. So this is bad:
				# 	megamerged_reader = csv.DictReader(infile, fieldnames=MERGED_OUT_FIELDNAMES)
				megamerged_reader = csv.DictReader(infile)
				rows = [row for row in megamerged_reader]
				_logger.debug(rows[0])
				coalescer = kalpaa.inference_coalesce.Coalescer(
					rows, num_replicas=self.config.generation_config.num_replicas
				)
				_logger.info(coalescer.actual_dict.keys())

				# coalescer.coalesce_generations(("fixedxy", "1"), "dot1")

				coalesced = coalescer.coalesce_all()

				inferenced_path = (
					self.config.get_out_dir_path()
					/ self.config.general_config.mega_merged_inferenced_name
				)
				with inferenced_path.open(mode="w", newline="") as outfile:
					writer = csv.DictWriter(
						outfile, fieldnames=INFERENCED_OUT_FIELDNAMES
					)
					writer.writeheader()
					for val in coalesced.values():
						for dots in val.values():
							for generation in dots.values():
								for row in generation.values():
									writer.writerow(row)
		else:
			_logger.info(
				"skipping inference metamerge, overridden dipole config specified"
			)


def parse_args():

	parser = argparse.ArgumentParser(
		"put files in directory", formatter_class=argparse.ArgumentDefaultsHelpFormatter
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

	runner = Stage04Runner(config)
	runner.run()


if __name__ == "__main__":
	main()
