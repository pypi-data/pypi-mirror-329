import re
import numpy
import dataclasses
import typing
import json
import pathlib
import logging
import csv
import deepdog.direct_monte_carlo.dmc_filters
import deepdog.direct_monte_carlo.compose_filter
import deepdog.direct_monte_carlo.cost_function_filter
import tantri.cli

import pdme
import pdme.util.fast_v_calc
import pdme.measurement
import pdme.measurement.input_types

_logger = logging.getLogger(__name__)

X_ELECTRIC_FIELD = "Ex"
POTENTIAL = "V"


@dataclasses.dataclass
class Measurement:
	dot_measurement: pdme.measurement.DotMeasurement
	stdev: float


class CostFunction:
	def __init__(self, measurement_type, dot_inputs_array, actual_measurement_array):
		_logger.info(f"Cost function with measurement type of {measurement_type}")
		self.measurement_type = measurement_type
		self.dot_inputs_array = dot_inputs_array
		self.actual_measurement_array = actual_measurement_array
		self.actual_measurement_array2 = actual_measurement_array**2

	def __call__(self, dipoles_to_test):
		if self.measurement_type == X_ELECTRIC_FIELD:
			vals = pdme.util.fast_v_calc.fast_efieldxs_for_dipoleses(
				self.dot_inputs_array, dipoles_to_test
			)
		elif self.measurement_type == POTENTIAL:
			vals = pdme.util.fast_v_calc.fast_vs_for_dipoleses(
				self.dot_inputs_array, dipoles_to_test
			)
		diffs = (
			vals - self.actual_measurement_array
		) ** 2 / self.actual_measurement_array2
		return numpy.sqrt(diffs.mean(axis=-1))


class StDevUsingCostFunction:
	def __init__(
		self,
		measurement_type,
		dot_inputs_array,
		actual_measurement_array,
		actual_stdev_array,
		log_noise: bool = False,
	):
		_logger.info(f"Cost function with measurement type of {measurement_type}")
		self.measurement_type = measurement_type
		self.dot_inputs_array = dot_inputs_array
		self.actual_measurement_array = actual_measurement_array
		self.actual_measurement_array2 = actual_measurement_array**2
		self.actual_stdev_array = actual_stdev_array
		self.actual_stdev_array2 = actual_stdev_array**2

		self.use_log_noise = log_noise
		self.log_actual = numpy.log(self.actual_measurement_array)
		self.log_denom2 = (
			numpy.log(self.actual_stdev_array + self.actual_measurement_array)
			- numpy.log(self.actual_measurement_array)
		) ** 2
		# if self.use_log_noise:
		# 	_logger.debug("remove these debugs later")
		# 	_logger.debug(self.actual_measurement_array)
		# 	_logger.debug(self.actual_stdev_array)
		# 	_logger.debug(self.log_actual)
		# 	_logger.debug(self.log_denom2)

	def __call__(self, dipoles_to_test):
		if self.measurement_type == X_ELECTRIC_FIELD:
			vals = pdme.util.fast_v_calc.fast_efieldxs_for_dipoleses(
				self.dot_inputs_array, dipoles_to_test
			)
		elif self.measurement_type == POTENTIAL:
			vals = pdme.util.fast_v_calc.fast_vs_for_dipoleses(
				self.dot_inputs_array, dipoles_to_test
			)

		if self.use_log_noise:
			diffs = ((numpy.log(vals) - self.log_actual) ** 2) / self.log_denom2
		else:
			diffs = (
				(vals - self.actual_measurement_array) ** 2
			) / self.actual_stdev_array2

		return numpy.sqrt(diffs.mean(axis=-1))


# the key for frequencies in what we return
RETURNED_FREQUENCIES_KEY = "frequencies"


def read_dots_json(json_file: pathlib.Path) -> typing.Dict:
	try:
		with open(json_file, "r") as file:
			return _reshape_dots_dict(json.load(file))
	except Exception as e:
		_logger.error(
			f"Had a bad time reading the dots file {json_file}, sorry.", exc_info=e
		)
		raise e


def _reshape_dots_dict(dots_dict: typing.Sequence[typing.Dict]) -> typing.Dict:
	ret = {}
	for dot in dots_dict:
		ret[dot["label"]] = dot["r"]
	return ret


BINNED_HEADER_REGEX = r"\s*APSD_(?P<measurement_type>\w+)_(?P<dot_name>\w+)_(?P<summary_stat>mean|stdev)\s*"


@dataclasses.dataclass
class ParsedBinHeader:
	original_field: str
	measurement_type: str
	dot_name: str
	summary_stat: str


def read_bin_csv(
	csv_file: pathlib.Path,
) -> typing.Tuple[str, typing.Dict[str, typing.Any]]:

	measurement_type = None
	_logger.info(f"Assuming measurement type is {measurement_type} for now")
	try:
		with open(csv_file, "r", newline="") as file:
			reader = csv.DictReader(file)
			fields = reader.fieldnames

			if fields is None:
				raise ValueError(
					f"Really wanted our fields for fiel {file=} to be non-None, but they're None"
				)
			freq_field = fields[0]

			remaining_fields = fields[1:]
			_logger.debug(f"Going to read frequencies from {freq_field=}")

			parsed_headers = {}
			aggregated_dict: typing.Dict[str, typing.Any] = {
				RETURNED_FREQUENCIES_KEY: []
			}

			for field in remaining_fields:
				match = re.match(BINNED_HEADER_REGEX, field)
				if match is None:
					_logger.warning(f"Could not parse {field=}")
					continue
				match_groups = match.groupdict()
				parsed_header = ParsedBinHeader(
					field,
					match_groups["measurement_type"],
					match_groups["dot_name"],
					match_groups["summary_stat"],
				)
				parsed_headers[field] = parsed_header

				if parsed_header.dot_name not in aggregated_dict:
					aggregated_dict[parsed_header.dot_name] = {}

				if (
					parsed_header.summary_stat
					not in aggregated_dict[parsed_header.dot_name]
				):
					aggregated_dict[parsed_header.dot_name][
						parsed_header.summary_stat
					] = []

				if measurement_type is not None:
					if measurement_type != parsed_header.measurement_type:
						_logger.warning(
							f"Attempted to set already set measurement type {measurement_type}. Allowing the switch to {parsed_header.measurement_type}, but it's problematic"
						)
				measurement_type = parsed_header.measurement_type

			_logger.debug("finished parsing headers")
			_logger.debug("throwing away the measurement type for now")

			for row in reader:
				# _logger.debug(f"Got {row=}")
				aggregated_dict[RETURNED_FREQUENCIES_KEY].append(
					float(row[freq_field].strip())
				)
				for field, parsed_header in parsed_headers.items():
					value = float(row[field].strip())
					aggregated_dict[parsed_header.dot_name][
						parsed_header.summary_stat
					].append(value)

			if measurement_type is None:
				raise ValueError(
					f"For some reason {measurement_type=} is None? We want to know our measurement type."
				)
			return measurement_type, aggregated_dict
	except Exception as e:
		_logger.error(
			f"Had a bad time reading the binned data {csv_file}, sorry.", exc_info=e
		)
		raise e


@dataclasses.dataclass
class BinnedData:
	dots_dict: typing.Dict
	csv_dict: typing.Dict[str, typing.Any]
	measurement_type: str

	# we're ignoring stdevs for the current moment, as in the calculator single_dipole_matches.py script.
	def _dot_to_measurement(self, dot_name: str) -> typing.Sequence[Measurement]:
		if dot_name not in self.dots_dict:
			raise KeyError(f"Could not find {dot_name=} in {self.dots_dict=}")
		if dot_name not in self.csv_dict:
			raise KeyError(f"Could not find {dot_name=} in {self.csv_dict=}")

		dot_r = self.dots_dict[dot_name]
		freqs = self.csv_dict[RETURNED_FREQUENCIES_KEY]
		vs = self.csv_dict[dot_name]["mean"]
		stdevs = self.csv_dict[dot_name]["stdev"]

		return [
			Measurement(
				dot_measurement=pdme.measurement.DotMeasurement(f=f, v=v, r=dot_r),
				stdev=stdev,
			)
			for f, v, stdev in zip(freqs, vs, stdevs)
		]

	def _dot_to_stdev(self, dot_name: str) -> typing.Sequence[float]:
		if dot_name not in self.dots_dict:
			raise KeyError(f"Could not find {dot_name=} in {self.dots_dict=}")
		if dot_name not in self.csv_dict:
			raise KeyError(f"Could not find {dot_name=} in {self.csv_dict=}")

		stdevs = self.csv_dict[dot_name]["stdev"]

		return stdevs

	def measurements(
		self, dot_names: typing.Sequence[str]
	) -> typing.Sequence[Measurement]:
		_logger.debug(f"Constructing measurements for dots {dot_names=}")
		ret = []
		for dot_name in dot_names:
			ret.extend(self._dot_to_measurement(dot_name))
		return ret

	def _cost_function(self, measurements: typing.Sequence[Measurement]):
		dot_measurements = [m.dot_measurement for m in measurements]
		meas_array = numpy.array([m.v for m in dot_measurements])

		_logger.debug(f"Obtained {meas_array=}")

		inputs = [(m.dot_measurement.r, m.dot_measurement.f) for m in measurements]
		input_array = pdme.measurement.input_types.dot_inputs_to_array(inputs)
		_logger.debug(f"Obtained {input_array=}")

		return CostFunction(self.measurement_type, input_array, meas_array)

	def _stdev_cost_function(
		self,
		measurements: typing.Sequence[Measurement],
		use_log_noise: bool = False,
	):
		meas_array = numpy.array([m.dot_measurement.v for m in measurements])
		stdev_array = numpy.array([m.stdev for m in measurements])

		_logger.debug(f"Obtained {meas_array=}")

		inputs = [(m.dot_measurement.r, m.dot_measurement.f) for m in measurements]
		input_array = pdme.measurement.input_types.dot_inputs_to_array(inputs)
		_logger.debug(f"Obtained {input_array=}")

		return StDevUsingCostFunction(
			self.measurement_type, input_array, meas_array, stdev_array, use_log_noise
		)

	def cost_function_filter(self, dot_names: typing.Sequence[str], target_cost: float):
		measurements = self.measurements(dot_names)
		cost_function = self._cost_function(measurements)
		return deepdog.direct_monte_carlo.cost_function_filter.CostFunctionTargetFilter(
			cost_function, target_cost
		)

	def stdev_cost_function_filter(
		self,
		dot_names: typing.Sequence[str],
		target_cost: float,
		use_log_noise: bool = False,
	):
		measurements = self.measurements(dot_names)
		cost_function = self._stdev_cost_function(measurements, use_log_noise)
		return deepdog.direct_monte_carlo.cost_function_filter.CostFunctionTargetFilter(
			cost_function, target_cost
		)


def read_dots_and_binned(json_file: pathlib.Path, csv_file: pathlib.Path) -> BinnedData:
	dots = read_dots_json(json_file)
	measurement_type, binned = read_bin_csv(csv_file)
	return BinnedData(
		measurement_type=measurement_type, dots_dict=dots, csv_dict=binned
	)


if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)

	print(read_dots_json(pathlib.Path("dots.json")))
	# print(read_bin_csv(pathlib.Path("binned-0.01-10000-50-12345.csv")))
	binned_data = read_dots_and_binned(
		pathlib.Path("dots.json"), pathlib.Path("binned-0.01-10000-50-12345.csv")
	)
	_logger.info(binned_data)
	for entry in binned_data.measurements(["uprise1", "dot1"]):
		_logger.info(entry)
	filter = binned_data.cost_function_filter(["uprise1", "dot1"], 0.5)
	_logger.info(filter)
