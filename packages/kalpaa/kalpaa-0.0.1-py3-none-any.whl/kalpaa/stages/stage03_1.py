import kalpaa.common
import os
import logging
import argparse
import deepdog.results
import pathlib
from dataclasses import dataclass


_logger = logging.getLogger(__name__)


@dataclass
class BFile:
	file: pathlib.Path
	target_dirname: str


def target_dir(filename) -> BFile:
	fileresult = deepdog.results._parse_output_filename(
		pathlib.Path("dipoles") / filename
	)
	_logger.debug(f"Parsed {filename=} to {fileresult=}")
	parsed_slug = deepdog.results.parse_file_slug(fileresult.filename_slug)
	_logger.debug(f"{parsed_slug=}")
	if parsed_slug is None:
		raise ValueError(f"Could not parse {filename=}")
	tag = parsed_slug["tag"]
	cost = parsed_slug["target_cost"]
	target_dirname = f"{kalpaa.common.sorted_bayesruns_name()}/{tag}-{cost}"
	file = fileresult.path

	bfile = BFile(file=file, target_dirname=target_dirname)

	_logger.info(f"For {filename=} got {bfile=}")

	return bfile


def move_file(bfile: BFile):
	name = bfile.file.name
	_logger.debug(f"Moving {bfile=}")
	target_dirpath = pathlib.Path(bfile.target_dirname)
	target_dirpath.mkdir(parents=True, exist_ok=True)
	bfile.file.rename(target_dirpath / name)


def move_all_in_dipoles(dipoles_path: pathlib.Path):

	_logger.info(f"Going to try to move files in {dipoles_path=}")

	sorted_dir = pathlib.Path(kalpaa.common.sorted_bayesruns_name())
	sorted_dir.mkdir(exist_ok=True, parents=True)

	bayesruns = [
		target_dir(f) for f in dipoles_path.iterdir() if f.name.endswith("bayesrun.csv")
	]
	_logger.debug([f.name for f in dipoles_path.iterdir()])
	_logger.debug(f"{bayesruns=}")
	for bfile in bayesruns:
		_logger.debug(f"Moving {bfile=}")
		move_file(bfile)
