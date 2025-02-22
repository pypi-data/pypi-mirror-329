import pathlib
import logging

import kalpaa.stages.stage01
import kalpaa.stages.stage02
import kalpaa.stages.stage03
import kalpaa.stages.stage04
import kalpaa.common
import tantri.dipoles.types
import kalpaa.config

import argparse

# try not to use this out side of main or when defining config stuff pls
import numpy

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

	tantri_configs = [
		kalpaa.TantriConfig(123456, 50, 0.5, 100000),
		# kalpa.TantriConfig(1234, 50, 0.0005, 10000),
	]

	override_config = {
		# "test1": [
		# 	tantri.dipoles.types.DipoleTO(
		# 		numpy.array([0, 0, 100]),
		# 		numpy.array([-2, -2, 2.9]),
		# 		0.0005
		# 	)
		# ],
		"two_dipole_connors_geom": [
			tantri.dipoles.types.DipoleTO(
				numpy.array([0, 0, 100]), numpy.array([-2, -2, 5.75]), 0.0005
			),
			tantri.dipoles.types.DipoleTO(
				numpy.array([0, 0, 100]), numpy.array([6, 2, 5.75]), 0.05
			),
		],
		"two_dipole_connors_geom_omegaswap": [
			tantri.dipoles.types.DipoleTO(
				numpy.array([0, 0, 100]), numpy.array([-2, -2, 5.75]), 0.05
			),
			tantri.dipoles.types.DipoleTO(
				numpy.array([0, 0, 100]), numpy.array([6, 2, 5.75]), 0.0005
			),
		],
	}

	generation_config = kalpaa.GenerationConfig(
		tantri_configs=tantri_configs,
		counts=[3, 31],
		num_replicas=5,
		# let's test this out
		# override_dipole_configs=override_config,
		orientations=[tantri.dipoles.types.Orientation.Z],
		num_bin_time_series=25,
	)

	if args.override_root is None:
		_logger.info("root dir not given")
		root = pathlib.Path("plots0")
	else:
		root = pathlib.Path(args.override_root)

	if args.skip_to_stage is not None:
		if args.skip_to_stage not in [1, 2, 3, 4]:
			raise ValueError(f"There is no stage {args.skip_to_stage}")
		else:
			skip = kalpaa.config.SkipToStage(args.skip_to_stage - 1)
	else:
		skip = None

	general_config = kalpaa.GeneralConfig(
		measurement_type=kalpaa.MeasurementTypeEnum.POTENTIAL,
		out_dir_name=str(root / "out"),
		skip_to_stage=skip,
	)

	# kalpa.GeneralConfig

	deepdog_config = kalpaa.DeepdogConfig(
		costs_to_try=[2, 1],
		max_monte_carlo_cycles_steps=20,
		target_success=200,
		use_log_noise=True,
	)

	config = kalpaa.Config(
		generation_config=generation_config,
		general_config=general_config,
		deepdog_config=deepdog_config,
	)

	kalpaa.common.set_up_logging(config, str(root / f"logs/{root}.log"))

	_logger.info(f"Got {config=}")
	runner = Runner(config)
	runner.run()


if __name__ == "__main__":
	main()
