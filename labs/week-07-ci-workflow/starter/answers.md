CI run: [URL of the green CI run](https://github.com/laci-loczi/mlops-course/actions/runs/41450185842)

CT run: [URL of the manual CT run](https://github.com/laci-loczi/mlops-course/actions/runs/41451408682)

Exercise 1:
1. What is `autograde.yml` for? Which commands does it run, and in which folders?

It is the course autograder: on every push, pull request or manual dispatch it checks that each lab's uv.lock is up to date (`uv lock --check`) and then runs each lab's tests. It runs `uv sync --locked --all-groups && uv run --frozen pytest -q` in every folder under `labs/*/starter` (or a flat `labs/*`) that has a pyproject.toml.

Exercise 5:
1. What differs between `ci.yml` and `ct.yml`, and what is the same? What does the difference change: who waits for the run, is there a diff to read, and who approved the input?

The same: both install with uv, rebuild the dataset, run the pipeline and the gate through the Makefile, and publish the verdict and the evidence the same way; the difference is that CI runs on a push or PR with lint and the test layers, while CT runs on a clock or by hand, with only retrain and gate. CI has a developer waiting for it and a code diff a reviewer approved, whereas a scheduled CT run has nobody waiting, no diff to read (only the data or time changed), and nobody approved its input.

2. `ct.yml` stops at the gate: it does not register, promote or deploy. Give a reason that is not about credentials. Is a GO enough to release a model?

The gate only checks the criteria written down in advance, and it lets skipped checks (for example the 50+ and under_normal slices) through, so a human should read the report and decide before a model reaches patients. A GO is necessary but not enough: it says the model passed the known checks, not that it is safe for the cases nobody measured.

3. Name one way a `schedule:` trigger can run late, or not at all, without anyone being told.

GitHub delays scheduled runs under high load and can drop them, and it disables scheduled workflows in a repository with no activity for 60 days, all without notifying anyone.
