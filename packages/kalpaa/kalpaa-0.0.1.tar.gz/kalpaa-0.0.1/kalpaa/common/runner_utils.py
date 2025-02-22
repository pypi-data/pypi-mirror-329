import logging
import contextlib
import os
import typing

_logger = logging.getLogger(__name__)


@contextlib.contextmanager
def new_cd(x: typing.Union[str, bytes, os.PathLike]):
	d = os.getcwd()

	_logger.debug(f"Attempting to change dir from {d=} to {x=}")

	# This could raise an exception, but it's probably
	# best to let it propagate and let the caller
	# deal with it, since they requested x
	os.chdir(x)

	try:
		yield

	finally:
		# This could also raise an exception, but you *really*
		# aren't equipped to figure out what went wrong if the
		# old working directory can't be restored.
		os.chdir(d)


def tantri_full_output_name(tantri_index: int) -> str:
	return f"apsd_{tantri_index}.csv"


def tantri_binned_output_name(tantri_index: int) -> str:
	return f"binned_apsd_{tantri_index}.csv"


def sorted_bayesruns_name() -> str:
	return "sorted-bayesruns"


def merged_coalesced_name() -> str:
	return "merged_coalesced.csv"
