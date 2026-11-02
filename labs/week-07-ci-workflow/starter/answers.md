CI run: <URL of the green CI run>
CT run: <URL of the manual CT run>

Exercise 1:
1. What is `autograde.yml` for? Which commands does it run, and in which folders?

It is the course autograder: on every push, pull request or manual dispatch it checks that each lab's uv.lock is up to date (`uv lock --check`) and then runs each lab's tests. It runs `uv sync --locked --all-groups && uv run --frozen pytest -q` in every folder under `labs/*/starter` (or a flat `labs/*`) that has a pyproject.toml.
