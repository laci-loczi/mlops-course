**Scheduled run (Exercise 5):** `hospitable-firefly` (flow `diabetes-training-with-pull`,
deployment `weekly-retrain`): **Completed**

## Exercise 2 — DVC and Prefect responsibilities

### Prefect provides DVC doesnt

1. **Run history.** Prefect stores every run with task states, durations and logs, failed runs
   included. This shows where an unattended run stopped.
2. **Retries with backoff and jitter.** Network steps (`dvc pull`/`push`) survive transient
   failures without a manual re-run.
3. **Scheduling and failure handling.** Runs can start from a cron, the UI or the API, and
   `notify` runs on failure too. This makes regular unattended training possible, and someone
   finds out when it breaks.

### DVC provides Prefect doesnt

**Content-based staleness and data versioning.** DVC hashes deps, params and outputs, reruns only
the stages that changed, and pins data and parameters to a commit. This makes results
reproducible and avoids rerunning stages whose inputs did not change.

### One task per DVC stage?

You would lose DVC as the single owner of the graph. Either every stage reruns every time, or
the stage order has to be duplicated in `dvc.yaml` and in the flow, where the two copies can
drift apart. Splitting is useful when stages need different treatment: different
infrastructure (a GPU for `train`), different timeouts or retries, parallel stages, or
per-stage monitoring of long-running steps.

## Exercise 5 — Scheduling

1. **Is the gate enough?** No. The gate is a necessary condition, not a sufficient one. Before
   release I would also require:
   - a comparison against the current production model on recent data
   - a check that the training data was the expected new batch, not stale or partial
   - a human review and approval of the new version
   - a staged rollout (shadow or canary) with a rollback path
2. **What to notify, and to whom.** Every run's outcome and parameters go to a log or channel
   the team reads. Failures and NO-GO verdicts go to the model owner or on-call person, with the
   failing task and the error. A GO becomes a "candidate ready for review" message to whoever
   approves releases.
3. **The second failure in a row.** Escalate: page the owner instead of just logging it, and
   pause the schedule so it does not keep failing (or keep retraining on bad data) until someone
   investigates. A single failure may be transient; a repeated one is not.
4. **What these still miss.** A run that **never happens**: the serve process or scheduler is
   down, or the cron stops firing. No run means no failure and no notification. Catching it
   needs an external "no successful run in N hours" check. These checks also miss a run that
   "succeeds" on silently wrong data, which passes the gate.
