import dataclasses
import typing
import logging
from tantri.dipoles.types import Orientation
import kalpaa.config

_logger = logging.getLogger(__name__)

from pdme.model import (
	LogSpacedRandomCountMultipleDipoleFixedMagnitudeModel,
	LogSpacedRandomCountMultipleDipoleFixedMagnitudeXYModel,
	LogSpacedRandomCountMultipleDipoleFixedMagnitudeFixedOrientationModel,
)


def long_orientation_name(orientation: Orientation) -> str:
	return {
		Orientation.RANDOM: "free",
		Orientation.XY: "fixedxy",
		Orientation.Z: "fixedz",
	}[orientation]


def _fixed_z_model_func(
	xmin,
	xmax,
	ymin,
	ymax,
	zmin,
	zmax,
	wexp_min,
	wexp_max,
	pfixed,
	n_max,
	prob_occupancy,
):
	return LogSpacedRandomCountMultipleDipoleFixedMagnitudeFixedOrientationModel(
		xmin,
		xmax,
		ymin,
		ymax,
		zmin,
		zmax,
		wexp_min,
		wexp_max,
		pfixed,
		0,
		0,
		n_max,
		prob_occupancy,
	)


def get_model(params: kalpaa.config.ReducedModelParams):
	model_funcs = {
		Orientation.Z: _fixed_z_model_func,
		Orientation.RANDOM: LogSpacedRandomCountMultipleDipoleFixedMagnitudeModel,
		Orientation.XY: LogSpacedRandomCountMultipleDipoleFixedMagnitudeXYModel,
	}
	_logger.info(f"Got params that look like {params=}")
	_logger.info(f"Got params that look like {params=}")
	model = model_funcs[params.orientation](
		params.x_min,
		params.x_max,
		params.y_min,
		params.y_max,
		params.z_min,
		params.z_max,
		params.w_log_min,
		params.w_log_max,
		10**params.log_magnitude,
		params.count,
		0.99999999,
	)
	return (
		f"geom_{model.xmin}_{model.xmax}_{model.ymin}_{model.ymax}_{model.zmin}_{model.zmax}-magnitude_{params.log_magnitude}-orientation_{long_orientation_name(params.orientation)}-dipole_count_{params.count}",
		model,
	)
