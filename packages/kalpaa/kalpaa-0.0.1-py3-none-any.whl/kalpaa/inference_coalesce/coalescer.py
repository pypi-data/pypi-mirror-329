import logging

_logger = logging.getLogger(__name__)


class Keys:
	def __init__(self, row):
		self.row = row

	def actual_key(self):
		return (self.row["actual_orientation"], self.row["actual_avg_filled"])

	def dot_cost_key(self):
		return (self.row["dot_name"], self.row["target_cost"])

	def model_key(self):
		return (
			self.row["orientation"],
			self.row["avg_filled"],
			self.row["log_magnitude"],
		)

	def replica_key(self):
		return self.row["generation_replica_index"]

	def all_keys(self):
		return (
			self.actual_key(),
			self.dot_cost_key(),
			self.replica_key(),
			self.model_key(),
		)


class Coalescer:
	def __init__(self, rows, num_replicas: int):
		self.rows = rows
		# sort into actuals, then dots, then probs
		self.actual_dict = {}
		for row in self.rows:
			keys = Keys(row).all_keys()
			_logger.debug(keys)
			if keys[0] not in self.actual_dict:
				_logger.debug(f"Creating layer 0 for {keys[0]}")
				self.actual_dict[keys[0]] = {}
			if keys[1] not in self.actual_dict[keys[0]]:
				_logger.debug(f"Creating layer 1 for {keys[0]}, {keys[1]}")
				self.actual_dict[keys[0]][keys[1]] = {}
			if keys[2] not in self.actual_dict[keys[0]][keys[1]]:
				_logger.debug(f"Creating layer 2 for {keys[0]}, {keys[1]}, {keys[2]}")
				self.actual_dict[keys[0]][keys[1]][keys[2]] = {}
			_logger.debug(
				f"Adding to {self.actual_dict[keys[0]][keys[1]][keys[2]]} for {keys[3]}"
			)
			self.actual_dict[keys[0]][keys[1]][keys[2]][keys[3]] = row

		self.num_replicas = num_replicas

	def coalesce_generations(self, actual_key, dot_key):

		_logger.debug(self.actual_dict.keys())
		_logger.debug(self.actual_dict[actual_key].keys())

		subdict = self.actual_dict[actual_key][dot_key]

		_logger.debug(f"subdict keys: {subdict.keys()}")

		# TODO hardcoding 3 generations
		# if self.num_replicas != 3:
		# 	raise ValueError(
		# 		f"num replicas was {self.num_replicas}, but we've hard coded 3"
		# 	)
		# generations_keys = ["0", "1", "2"]

		_logger.info(f"Going through generation {0}")

		# 0th gen is easiest
		for model_key, val in subdict["0"].items():
			val["coalesced_prob"] = val["prob"]

		if self.num_replicas > 1:
			for gen in range(1, self.num_replicas):
				_logger.info(f"Going through generation {gen}")

				generation_weight = sum(
					[
						float(subdict[str(gen - 1)][key]["coalesced_prob"])
						* float(subdict[str(gen)][key]["prob"])
						for key in subdict[str(gen)].keys()
					]
				)
				_logger.debug(generation_weight)
				for model_key, val in subdict[str(gen)].items():
					val["coalesced_prob"] = (
						float(val["prob"])
						* float(subdict[str(gen - 1)][model_key]["coalesced_prob"])
						/ generation_weight
					)

	def coalesce_all(self):
		for actual_key in self.actual_dict.keys():
			for dot_key in self.actual_dict[actual_key].keys():
				self.coalesce_generations(actual_key, dot_key)
		return self.actual_dict
