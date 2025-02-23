import pathlib
import logging

import dataclasses

import kalpaa.stages.stage01
import kalpaa.stages.stage02
import kalpaa.stages.stage03
import kalpaa.stages.stage04
import kalpaa.common
import kalpaa.config

import argparse

# try not to use this out side of main or when defining config stuff pls
# import numpy

_logger = logging.getLogger(__name__)


class Runner:
	def __init__(self, config: kalpaa.Config):
		self.config = config
		_logger.info(f"Initialising runner with {config=}")

	def run(self):

		if self.config.general_config.skip_to_stage is not None:

			stage01 = kalpaa.stages.stage01.Stage01Runner(self.config)
			stage02 = kalpaa.stages.stage02.Stage02Runner(self.config)
			stage03 = kalpaa.stages.stage03.Stage03Runner(self.config)
			stage04 = kalpaa.stages.stage04.Stage04Runner(self.config)

			stages = [stage01, stage02, stage03, stage04]

			start = int(self.config.general_config.skip_to_stage)
			_logger.info(f"Received instruction to start at stage {start + 1}")
			for i, stage in enumerate(stages[start:4]):
				_logger.info(f"*** Running stage {i + start + 1}")
				stage.run()

		else:
			# standard run, can keep old

			_logger.info("*** Beginning Stage 01 ***")
			stage01 = kalpaa.stages.stage01.Stage01Runner(self.config)
			stage01.run()

			_logger.info("*** Beginning Stage 02 ***")
			stage02 = kalpaa.stages.stage02.Stage02Runner(self.config)
			stage02.run()

			_logger.info("*** Beginning Stage 03 ***")
			stage03 = kalpaa.stages.stage03.Stage03Runner(self.config)
			stage03.run()

			_logger.info("*** Beginning Stage 04 ***")
			stage04 = kalpaa.stages.stage04.Stage04Runner(self.config)
			stage04.run()


def parse_args():

	parser = argparse.ArgumentParser(
		"Multistage Runner", formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)

	parser.add_argument(
		"--override-root",
		type=str,
		help="If provided, override the root dir.",
		default=None,
	)

	parser.add_argument(
		"-d",
		"--directory-label",
		type=str,
		help="Label for directory to put files in within root",
		default="output1",
	)

	parser.add_argument(
		"--config-file",
		type=str,
		help="kalpaa.toml file to use for configuration",
		default="kalpaa.toml",
	)

	parser.add_argument(
		"-s",
		"--skip-to-stage",
		type=int,
		help="Skip to stage, if provided. 1 means stages 1-4 will run, 4 means only stage 4 will run.",
		default=None,
	)
	args = parser.parse_args()
	return args


def main():
	args = parse_args()

	config = kalpaa.config.read_config(pathlib.Path(args.config_file))
	label = args.directory_label

	if args.override_root is None:
		_logger.info("root dir not given")
		# root = pathlib.Path("hardcodedoutplace")
		root = config.general_config.root_directory / label
	else:
		root = pathlib.Path(args.override_root) / label

	if args.skip_to_stage is not None:
		if args.skip_to_stage not in [1, 2, 3, 4]:
			raise ValueError(f"There is no stage {args.skip_to_stage}")
		else:
			skip = kalpaa.config.SkipToStage(args.skip_to_stage - 1)
	else:
		skip = None

	_logger.info(skip)

	kalpaa.common.set_up_logging(config, str(root / f"logs/kalpaa_{label}.log"))

	_logger.info(
		f"Root dir is {root}, copying over {config.general_config.indexes_json_name}, {config.general_config.dots_json_name} and {args.config_file}"
	)
	for file in [
		config.general_config.indexes_json_name,
		config.general_config.dots_json_name,
		args.config_file,
	]:
		_logger.info(f"Copying {file} to {root}")
		(root / file).write_text((pathlib.Path.cwd() / file).read_text())

	overridden_config = dataclasses.replace(
		config,
		general_config=dataclasses.replace(
			config.general_config, root_directory=root.resolve(), skip_to_stage=skip
		),
	)

	_logger.info(f"Got {config=}")
	runner = Runner(overridden_config)
	runner.run()


if __name__ == "__main__":
	main()
