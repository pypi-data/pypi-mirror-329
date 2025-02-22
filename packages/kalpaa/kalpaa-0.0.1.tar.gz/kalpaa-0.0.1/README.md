# kalpaa

Need to have a dots.json, indexes.json, the other jsons get generated.


# sources of truth
dots.json
indexes.json

costs
10.0 5.0 1.0 0.5 0.1 0.06
02-run_gen.sh



# Ideas
- can calculate some calibration curves for successes? and maybe some brier scores? but probably not 

# Variables to change
- count: 1 or 10, also use that for ddog
- Frequency range?
	- We may require some additional work to get automatic merging of multiple time series a la Connors paper
- Measurement type?
	- Let's do Ex field for now and maybe try potential later in a sd4 run

# Procedure
- `run.sh`
- `clean.sh` to clean things