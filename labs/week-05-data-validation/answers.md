# Week 5

## Exercise 2

**The `notes` column:** I would add it to the contract as an optional text column that never reaches the model, and keep rejecting batches until the clinic's data engineer and the ML team agree on the change.

**The four faults:** row 3 `glucose` = `unknown`, row 7 `age` = `250`, row 23 `bmi` = `280.0`, and the extra `notes` column. The `unknown` glucose caused 4 lines: it can't be converted to a number, so the type checks fail and the range checks then fail on text.

## Exercise 4

**Without the gate:** the age 250 row reached `data/processed/train.csv` (md5 `d9eba76c…` → `267b4f5e…`), `models/model.pkl` and `metrics/metrics.json`, which the MLflow run, the model registry and the serving API would use next. With the gate, `dvc repro` stopped at `validate` and `train.csv` stayed `d9eba76c…`.

**Running `prepare` by hand:** it stops with `ValidationFailed` ("The last validation failed…") because of the `_require_validated(settings)` line at the top of `prepare`. The edge in `dvc.yaml` only orders stages inside `dvc repro`, so a hand-run command skips DVC completely.

**`MAX_AGE` 120 → 125:** `validate` ran because `schemas.py` is one of its deps, but its report did not change, so `prepare` was skipped. `train` and `evaluate` ran because `schemas.py` is also one of their deps, but the model did not need retraining: the data and params were the same and the metrics did not change.
